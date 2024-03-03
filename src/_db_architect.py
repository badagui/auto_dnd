users = {
    'user_id': TABLE_ID,
    'uid': "",
    'name': "",
    'email': "", 
    'credits': 10000
}

campaigns = {
    'campaign_id': TABLE_ID,
    'owner': fk_user_id,
    'name': "",
    'world_geography': "",
    'world_lore': "",
    'main_storyline': "",
    'messages_start_index': 1
}

cities = {
    'city_id': TABLE_ID,
    'campaign_id': fk_campaign_id,
    'name': "",
    'description': ""
}

factions = {
    'faction_id': TABLE_ID,
    'campaign_id': fk_campaign_id,
    'name': "",
    'description': ""
}

sidequests = {
    'sidequest_id': TABLE_ID,
    'campaign_id': fk_campaign_id,
    'name': "",
    'description': ""
}

npcs = {
    'npc_id': TABLE_ID,
    'campaign_id': fk_campaign_id,
    'name': "",
    'description': ""
}

char_sheets = {
    'char_sheet_id': TABLE_ID,
    'campaign_id': fk_campaign_id,
    'name': "Josh",
    'race': "human",
    'class_': "fighter",
    'alignment': "neutral",
    'background': "noble",
    'level': 1,
    'experience': 0,
    'strength': 10,
    'dexterity': 10,
    'constitution': 10,
    'intelligence': 10,
    'wisdom': 10,
    'charisma': 10,
    'health': 10,
    'ac': 10,
    'speed': 30,
}

char_items = {
    'char_item_id': TABLE_ID,
    'char_sheet_id': fk_char_sheet_id,
    'item_name': "",
    'quantity': 1,
    'description': ""
}

char_skills = {
    'char_skill_id': TABLE_ID,
    'char_sheet_id': fk_char_sheet_id,
    'skill_name': "",
    'level': 1
}

messages = {
    'message_id': TABLE_ID,
    'campaign_id': fk_campaign_id,
    'timestamp': "",
    'role': "",
    'content': "",
    'tool_call_id': "",
    'function_json': "",
}

messages_resumes = {
    'message_resume_id': TABLE_ID,
    'campaign_id': fk_campaign_id,
    'start_message_ind': 0,
    'end_message_ind': 0,
    'content': "",
}
