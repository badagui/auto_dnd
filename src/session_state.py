from src.campaign_notes import CampaignNotes
from src.player_char_sheet import PlayerCharSheet
from src.prompts import get_campaign_introduction_msgs, get_new_geography_and_climate_prompts, get_new_main_storyline_prompts, get_new_starting_city_prompts, get_new_world_lore_prompts, get_gm_response_prompts
from src.GPTController import GPTController, count_messages_tokens
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
        self.messages_resumes = []
        self.user_turn = user_turn
    
    def set_char_sheet(self, name, background, strength, dexterity, constitution, intelligence, wisdom, charisma):
        self.player_char_sheet.set_character(name, background, strength, dexterity, constitution, intelligence, wisdom, charisma)

    async def tick_session(self, content: str, gpt_controller: GPTController):
        # ignore user message if not his turn
        if self.user_turn:
            self.messages.append({"role": "user", "content": content})
        
        # reset turn flag
        self.user_turn = True

        # BETA LIMIT (TO BE REMOVED AFTER WE IMPLEMENT MSG REDUCTION)
        if self.count_msgs_from(["assistant", "user"]) >= 20:
            limit_msg = {"role": "assistant", "content": "Alpha version limit reached (20+ messages). Start a new campaign to try it out again."}
            self.messages.append(limit_msg)
            return
        
        # MSG REDUCTION TEST
        self.resume_transcript()

        print(len(self.messages), 'msgs')
        if len(self.messages) == 3:
            print('creating geography and climate...')
            msgs, tools, tool_choice = get_new_geography_and_climate_prompts()
            response_msg = await gpt_controller.send_query(msgs, tools, tool_choice)
        elif len(self.messages) == 5:
            print('creating world lore...')
            msgs, tools, tool_choice = get_new_world_lore_prompts(self.campaign_notes)
            response_msg = await gpt_controller.send_query(msgs, tools, tool_choice)
        elif len(self.messages) == 7:
            print('creating main storyline...')
            msgs, tools, tool_choice = get_new_main_storyline_prompts(self.campaign_notes)
            response_msg = await gpt_controller.send_query(msgs, tools, tool_choice)
        elif len(self.messages) == 9:
            print('creating starting city...')
            msgs, tools, tool_choice = get_new_starting_city_prompts(self.campaign_notes)
            response_msg = await gpt_controller.send_query(msgs, tools, tool_choice)
        elif len(self.messages) == 11:
            print('starting campaign...')
            msgs = get_campaign_introduction_msgs(self.campaign_notes, self.player_char_sheet)
            response_msg = await gpt_controller.send_query(msgs, None)
        else:
            # add response from LLM
            system_prompt, tools = get_gm_response_prompts(self.campaign_notes, self.player_char_sheet)
            self.messages[0]["content"] = system_prompt
            response_msg = await gpt_controller.send_query(self.messages, tools)
        
        # converting from openai response object to a dict for better control
        response_msg = dict(response_msg) 
        
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
        
        return response_msg
    
    def count_msgs_from(self, who):
        # limit campaign to 20 messages in beta

        # msg_count (ignoring tools)
        msg_count = 0
        for n in range(1, len(self.messages)):
            if self.messages[n]['role'] in who:
                msg_count += 1
        return msg_count

    def resume_transcript(self):
        # if there are >=8 GM messages, mark gm_msg_5+1 as the new start_index. Next messages will be msg[0] (system) + msg[start_index:]
        # use llm to resume messages
        # add the resume to resumes list
        # resumes are added to the system message (in future, when this list grow, these resumes could be resumed too)

        print(f'there are {len(self.messages)} messages, they are:')
        for n in range(0, len(self.messages)):
            print('index: ', n, ' msg: ', self.messages[n])
        
        print('we are currently considering messages with index >= ', self.messages_start_index)

        token_count = count_messages_tokens(self.messages[self.messages_start_index:])
        print(f'messages window tokens: {token_count}')
        if token_count < 8000:
            print('token count less than 8000, all good')
            return
        
        token_counter = 0
        for end_index in range(self.messages_start_index+1, len(self.messages)):
            token_counter = count_messages_tokens(self.messages[self.messages_start_index:end_index])
            if token_counter >= 4500:
                print(f'found {token_counter} tokens, from {self.messages_start_index} to {end_index}')
                to_be_resumed = ''
                for n in range(self.messages_start_index, end_index):
                    to_be_resumed += f"{self.messages[n]['role']}: {self.messages[n]['content']} \n" 
                print('to_be_resumed: ', to_be_resumed)
                print(f'advancing messages_start_index from {self.messages_start_index} to {end_index}')
                self.messages_start_index = end_index
                break

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

    f_result = f_data['function'](**tool_args)
    return f_result