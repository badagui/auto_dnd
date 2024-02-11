
from src.GPTController import GPTController, count_messages_tokens
from src.campaign_notes import CampaignNotes
from src.player_char_sheet import PlayerCharSheet
from src.prompts import get_tools_prompt, get_system_prompt
import src.gm_tools as gm_tools
import json
from typing import List, Dict

class SessionState():
    def __init__(self, 
                 player_char_sheet: PlayerCharSheet, 
                 campaign_notes: CampaignNotes, 
                 messages: List[dict], 
                 user_turn: bool):
        self.player_char_sheet = player_char_sheet
        self.campaign_notes = campaign_notes
        self.messages = messages
        self.messages_start_index = 1 # 0 is always included (system prompt)
        self.messages_resumes = []
        self.user_turn = user_turn
    
    def set_char_sheet(self, name, background, strength, dexterity, constitution, intelligence, wisdom, charisma):
        self.player_char_sheet.set_character(name, background, strength, dexterity, constitution, intelligence, wisdom, charisma)

    async def get_gm_response(self, content: str, gpt_controller: GPTController):
        # ignore user message if not his turn
        if self.user_turn:
            self.messages.append({"role": "user", "content": content})
        
        # reset turn flag
        self.user_turn = True
        
        # update system prompt
        self.messages[0]["content"] = get_system_prompt(self.campaign_notes, self.player_char_sheet)

        self.resume_transcript()

        # add response from LLM
        response_msg = await gpt_controller.send_query(self.messages, get_tools_prompt(self.campaign_notes))
        print('received this msg: ', response_msg)
        # converting from openai response object to a dict for better control
        response_msg = dict(response_msg) 
        # openai api expects only function_call or tool_calls, not both.
        # this is done automatically when using the response object, but we're managing it manually
        response_msg.pop('function_call', '')
        if 'tool_calls' in response_msg and response_msg['tool_calls'] is None:
            response_msg.pop('tool_calls')

        print('converted to dict and removed function call: ', response_msg)
        self.messages.append(response_msg)
        
        # add tool result messages if any
        if 'tool_calls' in response_msg:
            for tool_call in response_msg['tool_calls']:
                function_result = exec_tool_function(tool_call.function, self.campaign_notes, self.player_char_sheet)
                self.messages.append({"role": "tool", "content": function_result, "tool_call_id": tool_call.id})
            self.user_turn = False # next turn is LLM again
        
        return response_msg
    
    def get_session_data(self):
        return {
            "response": {
                "messages": [msg for msg in self.messages if dict(msg)["role"] != "system"],
                "char_sheet": self.player_char_sheet.get_prompt(),
                "campaign_notes": self.campaign_notes.get_prompt(),
                "is_user_turn": self.user_turn,
            }
        }
    
    def resume_transcript(self):
        # if there are >=8 GM messages, mark gm_msg_5+1 as the new start_index. Next messages will be msg[0] (system) + msg[start_index:]
        # use llm to resume messages
        # add the resume to resumes list
        # resumes are added to the system message (in future, when this list grown, these resumes could be resumed too)

        print(f'there are {len(self.messages)} messages, they are:')
        for n in range(1, len(self.messages)):
            print('index: ', n, ' msg: ', self.messages[n])
        
        print('we are currently considering messages with index >= ', self.messages_start_index)

        token_count = count_messages_tokens(self.messages[self.messages_start_index:])
        print(f'messages window tokens: {token_count}')
        if token_count < 8000:
            print('token countless than 8000, all good')
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
    
    # argument checking
    try:
        tool_args = json.loads(function_call_data.arguments)
    except json.JSONDecodeError:
        return f'Error: invalid argument formatting for tool {function_name}.\n'

    # map tools to their corresponding function calls
    tool_functions = {
        'update_main_lore': lambda:                 campaign_notes.update_named_data('world_overview', 'main_lore', tool_args.get('new_main_lore')),
        'update_geography_and_climate': lambda:     campaign_notes.update_named_data('world_overview', 'geography_and_climate', tool_args.get('new_geography_and_climate')),
        'add_city': lambda:                         campaign_notes.add_named_data('cities', tool_args.get('city_name'), tool_args.get('city_description')),
        'update_city': lambda:                      campaign_notes.update_named_data('cities', tool_args.get('city_name'), tool_args.get('new_city_description')),
        'add_faction': lambda:                      campaign_notes.add_named_data('factions', tool_args.get('faction_name'), tool_args.get('faction_description')),
        'update_faction': lambda:                   campaign_notes.update_named_data('factions', tool_args.get('faction_name'), tool_args.get('new_faction_description')),
        'add_main_storyline': lambda:               campaign_notes.add_named_data('main_storylines', tool_args.get('storyline_name'), tool_args.get('storyline_description')),
        'update_main_storyline': lambda:            campaign_notes.update_named_data('main_storylines', tool_args.get('storyline_name'), tool_args.get('new_storyline_description')),
        'add_sidequest': lambda:                    campaign_notes.add_named_data('sidequests', tool_args.get('sidequest_name'), tool_args.get('sidequest_description')),
        'update_sidequest': lambda:                 campaign_notes.update_named_data('sidequests', tool_args.get('sidequest_name'), tool_args.get('new_sidequest_description')),
        'add_npc': lambda:                          campaign_notes.add_named_data('npcs', tool_args.get('npc_name'), tool_args.get('npc_description')),
        'update_npc': lambda:                       campaign_notes.update_named_data('npcs', tool_args.get('npc_name'), tool_args.get('new_npc_description')),
        'add_ending': lambda:                       campaign_notes.add_named_data('endings', tool_args.get('ending_name'), tool_args.get('ending_description')),
        'update_ending': lambda:                    campaign_notes.update_named_data('endings', tool_args.get('ending_name'), tool_args.get('new_ending_description')),
        'set_player_stat': lambda:                  player_char_sheet.set_player_stat(**tool_args),
        'set_player_skill': lambda:                 player_char_sheet.set_player_skill(**tool_args),
        'set_player_item': lambda:                  player_char_sheet.set_player_item(**tool_args),
        'roll_dices': lambda:                       gm_tools.roll_dices(**tool_args)
    }

    f_found = tool_functions.get(function_name)
    if not f_found:
        return f'Error: no tool named {function_name} found.\n'
    
    f_result = f_found()
    return f_result

class SessionManager():
    def __init__(self):
        self.sessions: Dict[str, SessionState] = {}

    def get_or_create_session(self, session_id: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionState(
                player_char_sheet=PlayerCharSheet(),
                campaign_notes=CampaignNotes(),
                messages=[
                    {"role": "system", "content": ""},
                    {"role": "assistant", "content": "Welcome to our D&D 3.5 session. I'm here to help you with your campaign. Are we all set to embark on this extraordinary journey?"}
                ],
                user_turn=True
            )
        return self.sessions[session_id]

    def check_session_exists(self, session_id: str):
        return session_id in self.sessions