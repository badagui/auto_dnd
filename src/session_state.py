from PIL import Image
import base64
import io
from src.campaign_notes import CampaignNotes
from src.player_char_sheet import PlayerCharSheet
from src.prompts import get_campaign_introduction_prompt, get_image_world_creation_prompt, get_summarizer_prompt, get_new_geography_and_climate_prompts, get_new_main_storyline_prompts, get_new_starting_city_prompts, get_new_world_lore_prompts, get_gm_response_prompts, get_world_description_summary_prompt
from src.gpt_controller import GPTController, count_messages_tokens
import json
import src.gm_tools as gm_tools
from typing import List

class SessionState():
    def __init__(self,
                 owner: str, 
                 player_char_sheet: PlayerCharSheet, 
                 campaign_notes: CampaignNotes, 
                 messages: List[dict], 
                 user_turn: bool):
        self.owner = owner
        self.player_char_sheet = player_char_sheet
        self.campaign_notes = campaign_notes
        self.messages = messages
        self.messages_start_index = 1 # 0 is always included (system prompt)
        self.msgs_summaries = []
        self.user_turn = user_turn
        self.campaign_intro_img_b64str = None
    
    def get_msgs_summaries_prompt(self):
        summaries_prompt = "EARLIER CAMPAIGN SUMMARIES:\n"
        for summary in self.msgs_summaries:
            summaries_prompt += summary + "\n"
        return summaries_prompt

    def set_char_sheet(self, name, background, strength, dexterity, constitution, intelligence, wisdom, charisma):
        self.player_char_sheet.set_character(name, background, strength, dexterity, constitution, intelligence, wisdom, charisma)

    # UPDATE STATE WITH USR_MSG -> RESUME TRANSCRIPT -> SEND MSG TO LLM (CUSTOM PROMPTS BASED ON MSG NUMBER) -> UPDATE STATE WITH LLM MSG + TOOL MSGS -> RETURN LLM MSG
    async def tick_session(self, content: str, gpt_controller: GPTController):
        # ignore user message if not his turn
        if self.user_turn:
            self.messages.append({"role": "user", "content": content})
        
        # reset turn flag
        self.user_turn = True

        # summarize transcript if needed
        summary_resp = await self.summarize_transcript(gpt_controller)
        summary_cost = 0
        if summary_resp is not None:
            summary_cost = summary_resp['summary_cost']
            self.msgs_summaries.append(summary_resp['summary_result'])

        img_cost = 0

        # get the correct prompt
        if len(self.messages) == 3:
            print('creating geography and climate...')
            msgs, tools, tool_choice = get_new_geography_and_climate_prompts()
            query_response = await gpt_controller.send_query(msgs, tools, tool_choice)
        elif len(self.messages) == 5:
            print('creating world lore...')
            msgs, tools, tool_choice = get_new_world_lore_prompts(self.campaign_notes)
            query_response = await gpt_controller.send_query(msgs, tools, tool_choice)
        elif len(self.messages) == 7:
            print('creating main storyline...')
            msgs, tools, tool_choice = get_new_main_storyline_prompts(self.campaign_notes)
            query_response = await gpt_controller.send_query(msgs, tools, tool_choice)
        elif len(self.messages) == 9:
            print('creating world description...')
            msgs = get_world_description_summary_prompt(self.campaign_notes)
            query_response = await gpt_controller.send_query(msgs, None)
            self.user_turn = False # next turn is LLM again
            print('creating world image...')
            img_prompt = get_image_world_creation_prompt(self.campaign_notes)
            img_response = await gpt_controller.send_img_query(img_prompt)
            print('img prompt:', img_prompt)
            print('revised_prompt', img_response['revised_prompt'])
            image_data = base64.b64decode(img_response['b64_json'])
            image_buffer = io.BytesIO(image_data) # file-like object
            optimized_buffer = io.BytesIO()
            image = Image.open(image_buffer)
            image.save(optimized_buffer, format='PNG', optimize=True)
            self.campaign_intro_img_b64str = base64.b64encode(optimized_buffer.getvalue()).decode('utf-8')
            img_cost = img_response['cost']
        elif len(self.messages) == 10:
            print('creating starting city...')
            msgs, tools, tool_choice = get_new_starting_city_prompts(self.campaign_notes)
            query_response = await gpt_controller.send_query(msgs, tools, tool_choice)
        elif len(self.messages) == 12:
            print('starting campaign...')
            msgs = get_campaign_introduction_prompt(self.campaign_notes, self.player_char_sheet)
            query_response = await gpt_controller.send_query(msgs, None)
        else:
            # default gm prompt
            system_prompt, tools = get_gm_response_prompts(self.campaign_notes, self.player_char_sheet, self.get_msgs_summaries_prompt())
            self.messages[0]["content"] = system_prompt
            query_response = await gpt_controller.send_query(self.messages, tools)
        
        # converting from openai response object to a dict for better control
        response_msg = dict(query_response['message']) 
        
        # openai api expects only function_call or tool_calls, not both.
        # this is done automatically when using the response object, but we're managing it manually
        response_msg.pop('function_call', '')
        if 'tool_calls' in response_msg and response_msg['tool_calls'] is None:
            response_msg.pop('tool_calls')

        print('received message: ', response_msg)
        self.messages.append(response_msg)
        
        # add tool result messages if any
        if 'tool_calls' in response_msg:
            for tool_call in response_msg['tool_calls']:
                function_result = exec_tool_function(tool_call.function, self.campaign_notes, self.player_char_sheet)
                self.messages.append({"role": "tool", "content": function_result, "tool_call_id": tool_call.id})
            self.user_turn = False # next turn is LLM again
        
        total_cost = query_response['cost'] + summary_cost + img_cost
        return {'response_msg': response_msg, 'cost': total_cost}
    
    def count_content_msgs_from(self, who, start_index=1):
        # msg_count (ignoring tools)
        msg_count = 0
        for n in range(start_index, len(self.messages)):
            if self.messages[n]['role'] in who and self.messages[n]['content'] is not None :
                msg_count += 1
        return msg_count

    async def summarize_transcript(self, gpt_controller: GPTController):
        # if there are >=8 GM messages, mark gm_msg_5+1 as the new start_index. Next messages will be msg[0] (system) + msg[start_index:]
        # use llm to resume messages
        # add the resume to resumes list
        # resumes are added to the system message (in future, when this list grow, these resumes could be resumed too)
        GM_MSGS_THRESHOLD = 8 # TEST: original is 8
        GM_MSGS_TO_SUMMIRIZE = 5 # TEST: original is 5
        assert GM_MSGS_TO_SUMMIRIZE < GM_MSGS_THRESHOLD, "GM_MSGS_TO_SUMMIRIZE must be less than GM_MSGS_THRESHOLD"

        # print('=========== RESUME_TRANSCRIPT =============')
        # print(f'there are {len(self.messages)} messages, they are:')
        for ind in range(0, len(self.messages)):
            print('index: ', ind, ' msg: ', self.messages[ind])
        
        # print('we are currently sending to the llm messages with index >= ', self.messages_start_index)
        gm_msgs = self.count_content_msgs_from(["assistant"], self.messages_start_index)
        # print('there are ', gm_msgs, ' gm messages')
        if gm_msgs >= GM_MSGS_THRESHOLD:
            print(f'gm_msgs >= {GM_MSGS_THRESHOLD}, resuming transcript...')
            # print(f'finding index of the {GM_MSGS_TO_SUMMIRIZE}th gm message starting from self.messages_start_index')
            gm_msg_counter = 0
            start_resume_index = self.messages_start_index
            end_resume_index = None
            for ind in range(self.messages_start_index, len(self.messages)):
                if self.messages[ind]['role'] == "assistant" and self.messages[ind]['content'] is not None:
                    gm_msg_counter += 1
                    if gm_msg_counter == GM_MSGS_TO_SUMMIRIZE:
                        # print(f'found {GM_MSGS_TO_SUMMIRIZE}th gm message, setting messages_start_index to ', ind+1)
                        end_resume_index = ind
                        self.messages_start_index = ind+1
                        print(f'summarization from: {start_resume_index} to: {end_resume_index}')
                        break
            # print('preparing content for summarization...')
            resume_content = ''
            for ind in range(start_resume_index, end_resume_index+1):
                role = self.messages[ind]['role']
                content = self.messages[ind]['content']
                if role == 'assistant' and content is not None:
                    resume_content += f'GM: {content}\n'
                elif role == 'user':
                    resume_content += f'Player: {content}\n'
                elif role == 'tool':
                    resume_content += f'Tool: {content}\n'
            # print('resume content: ', resume_content)
            summarizer_prompt_msgs = get_summarizer_prompt(resume_content)
            query_response = await gpt_controller.send_query(summarizer_prompt_msgs, None)
            summary_msg_content = query_response['message'].content + '\n'
            summary_cost = query_response['cost']
            # print('summary result: ', summary_msg_content, 'summary cost: ', summary_cost)
            # print('=========== END RESUME_TRANSCRIPT =============')
            return {'summary_result': summary_msg_content, 'summary_cost': summary_cost}
        print('no need to resume transcript, returning None')
        return None
        

def exec_tool_function(function_call_data, campaign_notes: CampaignNotes, player_char_sheet: PlayerCharSheet):
    function_name = function_call_data.name
    
    # json argument checking
    try:
        tool_args = json.loads(function_call_data.arguments)
    except json.JSONDecodeError:
        return f'Error: invalid argument formatting for tool {function_name}.\n'

    # map tool names to their function data (function object and required args (optional args are not checked))
    tool_functions = {
        'create_new_geography_and_climate':     {'arg_ref': {'name': str, 'description': str}, 
                                                 'function': campaign_notes.create_new_geography_and_climate},
        'create_new_world_lore':                {'arg_ref': {'description': str}, 
                                                 'function': campaign_notes.create_new_world_lore},
        'create_new_main_storyline':            {'arg_ref': {'description': str}, 
                                                 'function': campaign_notes.create_new_main_storyline},
        'create_starting_city':                 {'arg_ref': {'name': str, 'description': str}, 
                                                 'function': campaign_notes.create_starting_city},
        'add_city':                             {'arg_ref': {'name': str, 'description': str}, 
                                                 'function': campaign_notes.add_city},
        'add_faction':                          {'arg_ref': {'name': str, 'description': str}, 
                                                 'function': campaign_notes.add_faction},
        'add_sidequest':                        {'arg_ref': {'name': str, 'description': str}, 
                                                 'function': campaign_notes.add_sidequest},
        'add_npc':                              {'arg_ref': {'name': str, 'description': str}, 
                                                 'function': campaign_notes.add_npc},
        'set_player_stat':                      {'arg_ref': {'name': str, 'value': int}, 
                                                 'function': player_char_sheet.set_player_stat},
        'set_player_skill':                     {'arg_ref': {'name': str, 'level': int}, 
                                                 'function': player_char_sheet.set_player_skill},
        'set_player_item':                      {'arg_ref': {'name': str, 'quantity': int},  # optional: description: str
                                                 'function': player_char_sheet.set_player_item},
        'roll_dices':                           {'arg_ref': {'count': int, 'sides': int}, 
                                                 'function': gm_tools.roll_dices},
    }

    if function_name not in tool_functions:
        return f'Error: no tool named {function_name} found.\n'
    
    f_data = tool_functions.get(function_name)

    for arg_name, arg_type in f_data['arg_ref'].items():
        if arg_name not in tool_args:
            return f'Error: missing required argument {arg_name} for tool {function_name}.\n'
        if type(tool_args[arg_name]) != arg_type:
            return f'Error: invalid type for argument {arg_name} in tool {function_name}.\n'
    ##### debugging
    # exception process_input CampaignNotes.create_new_main_storyline() got an unexpected keyword argument 'possible_developments'
    # waiting for another unexpected keyword argument
    print('tool args: ', tool_args)
    print('f_data[arg_ref].items()', f_data['arg_ref'].items())
    ######
    f_result = f_data['function'](**tool_args)
    return f_result