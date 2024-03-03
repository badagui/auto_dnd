# def get_gm_assistant_registerer_prompt(campaign_notes: CampaignNotes, player_char_sheet: PlayerCharSheet):
#     base_prompt = (
#         "You are a GM assistant in a professional D&D 3.5 campaign.\n"
#         "You will analyze what the GM said and update the player character sheet and the gm campaign notes accordingly. "
#         "It's your job to keep track of the campaign and the player character sheet, making sure they are always up to date. "
#         "If the GM says something that changes the campaign notes or the player character sheet, you will register it. "
#         "You must judge the best time to register something, and if something is worth registering. "
#         "For example, if the players are interacting with an existing NPC and and they start a fight, you can wait until the scene is over to register the NPC's new status. "
#         "For example, if the GM introduces a new NPC, you can wait to see if the players are going to interact with it, and if it will be worth of registering. "
#         # "It's also your job to warn the GM if he says something that contradicts the campaign notes or the player character sheet. " --> auto reflection loop?
#     )
#     return base_prompt + campaign_notes.get_prompt() + player_char_sheet.get_prompt()

# UPDATE MAIN LORE
# {
#     "type": "function",
#     "function": {
#         "name": "update_main_lore",
#         "description": ("Updates the main lore of the game to reflect new developments, discoveries, or player actions that have impacted the game world's history, mythology, or cultural dynamics. "
#                         "This could include the revelation of ancient secrets, shifts in the balance of power, or changes in the perception of key historical events. "
#                         "Consider how these changes might affect existing quests, NPCs, and the overall narrative arc of the game. " 
#                         "Remember that the whole [MAIN_LORE] section of the campaign notes will be replaced, so include all the relevant information, not just the new information. "
#                         "You usually repeat what was written and append the new information at the end."),
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "new_main_lore": {
#                     "type": "string",
#                     "description": f"New [MAIN_LORE] description to be replaced in the campaign notes.",
#                 }
#             },
#             "required": ["new_main_lore"],
#         },
#     }
# },
# UPDATE GEOGRAPHY AND CLIMATE
# {
#     "type": "function",
#     "function": {
#         "name": "update_geography_and_climate",
#         "description": ("Update the game's geography and climate to add new information or incorporate changes that have occurred due to in-game events or player actions. "
#                         "This can include alterations in the landscape, changes in climate patterns, and the impact of these changes on the flora, fauna, and inhabitants of the game world. "
#                         "Explain how these geographical and climatic changes can influence game mechanics, travel, resource availability, and player strategies. "
#                         "Ensure that the updated description maintains consistency with what was already written and the ongoing narrative of the game. "
#                         "Remember that the whole [GEOGRAPHY_AND_CLIMATE] section of the campaign notes will be replaced, so include all the relevant information, not just the new information. "
#                         "You usually repeat what was written and append the new information at the end."),
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "new_geography_and_climate": {
#                     "type": "string",
#                     "description": f"New [GEOGRAPHY_AND_CLIMATE] description to be replaced in the campaign notes.",
#                 }
#             },
#             "required": ["new_geography_and_climate"],
#         },
#     }
# },
# # UPDATE CITY OR VILLAGE
# {
#     "type": "function",
#     "function": {
#         "name": "update_city",
#         "description": ("Updates an existing city, village or settlement, adding new information or annotating changes. "
#                         "Changes could be due to world events, player actions, or natural progression. "
#                         "This could include changes in leadership, shifts in economic or political conditions, alterations in population, cultural aspects, or physical transformations. "
#                         "Ensure that the updated description maintains consistency with what was already written and the ongoing narrative of the game. "
#                         "Remember that the whole section under this city name in the campaign notes will be replaced, so include all the relevant information, not just the new information. "
#                         "You usually repeat what was written and append the new information at the end."),
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "city_name": {
#                     "type": "string",
#                     "description": f"Name of the city, village or settlement that will be edited.",
#                     "enum": campaign_notes.get_named_data_names('cities')
#                 },
#                 "new_city_description": {
#                     "type": "string",
#                     "description": f"New description for this city, village or settlement.",
#                 }
#             },
#             "required": ["city_name", "new_city_description"],
#         },
#     }
# },
# UPDATE FACTION
# {
#     "type": "function",
#     "function": {
#         "name": "update_faction",
#         "description": ("Update an existant faction, group, guild, clan or tribe, adding information about important changes that might have happened since its inception, due to player actions, world events, or internal dynamics. "
#                         "This update should detail shifts in the faction's leadership, goals, alliances, or conflicts. "
#                         "Explain how these changes impact the faction's relationship with the players and other entities in the game world. "
#                         "Ensure that the updated description maintains consistency with what was already written and the ongoing narrative of the game."
#                         "Remember that the whole section under this faction name in the campaign notes will be replaced, so include all the relevant information, not just the new information. "
#                         "You usually repeat what was written and append the new information at the end."),
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "faction_name": {
#                     "type": "string",
#                     "description": f"The name of the faction to be updated.",
#                     "enum": campaign_notes.get_named_data_names('factions')
#                 },
#                 "new_faction_description": {
#                     "type": "string",
#                     "description": f"New faction description.",
#                 }
#             },
#             "required": ["faction_name", "new_faction_description"],
#         },
#     }
# },
# ADD MAIN STORYLINE
# {
#     "type": "function",
#     "function": {
#         "name": "add_main_storyline",
#         "description": ("Add a new main storyline to the game. "
#                         "These are the big story archs with world level impact, usually converging to one of the possible endings. "
#                         "In no more than two paragraphs, describe the nature of this storyline, including its origin, involved parties and potential impacts on the game world. "
#                         "Outline the key elements, such as clues, locations, and NPCs connected to it. "
#                         "Indicate how it might unfold and affect the players' journey, but leave enough ambiguity to allow for player-driven exploration and resolution. "
#                         "Try to integrate this storyline with existing elements for a more immersive experience. "
#                         "Try to make it unique. Be creative!"),
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "storyline_name": {
#                     "type": "string",
#                     "description": f"A name for this storyline.",
#                 },
#                 "storyline_description": {
#                     "type": "string",
#                     "description": f"Storyline description.",
#                 }
#             },
#             "required": ["storyline_name", "storyline_description"],
#         },
#     }
# },
# UPDATE MAIN STORYLINE
# {
#     "type": "function",
#     "function": {
#         "name": "update_main_storyline",
#         "description": ("Update an existing main storyline in the game, detailing significant developments or resolutions that have occurred. "
#                         "This should include changes in the involved parties, new clues or revelations, shifts in the conflict's impact on the world, and how these developments could alter the players' interaction with this narrative element. "
#                         "Ensure the update is consistent with the game's ongoing story and player actions. "
#                         "Remember to advance the main storylines as the campaign advances."
#                         "Remember that the whole section under this storyline name in the campaign notes will be replaced, so include all the relevant information, not just the update. "
#                         "You usually repeat what was written and append the new information at the end."),
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "storyline_name": {
#                     "type": "string",
#                     "description": f"The name of the storyline to be updated.",
#                     "enum": campaign_notes.get_named_data_names('main_storylines')
#                 },
#                 "new_storyline_description": {
#                     "type": "string",
#                     "description": f"New storyline description.",
#                 }
#             },
#             "required": ["storyline_name", "new_storyline_description"],
#         },
#     }
# },
# UPDATE SIDEQUEST
# {
#     "type": "function",
#     "function": {
#         "name": "update_sidequest",
#         "description": ("Updates an existing sidequest, reflecting changes based on player actions, world events or time passing. "
#                         "This could include alterations in quest objectives, the introduction of new challenges or rewards, or changes in the quest's scope"
#                         "Ensure the update is consistent with the game's ongoing story and player actions. "
#                         "Remember that the whole section under this sidequest name in the campaign notes will be replaced, so include all the relevant information, not just the update. "
#                         "You usually repeat what was written and append the new information at the end."),
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "sidequest_name": {
#                     "type": "string",
#                     "description": f"The name of the sidequest to be updated.",
#                     "enum": campaign_notes.get_named_data_names('sidequests')
#                 },
#                 "new_sidequest_description": {
#                     "type": "string",
#                     "description": f"New sidequest description.",
#                 }
#             },
#             "required": ["sidequest_name", "new_sidequest_description"],
#         },
#     }
# },
# UPDATE NPC
# {
#     "type": "function",
#     "function": {
#         "name": "update_npc",
#         "description": ("Update an existing NPC, adding extra information. "
#                         "You can use this to add a stat needed for an interaction, or to log changes in their character. "
#                         "Remember to log any changes in their role, available quests, information, or services, as well as their demeanor towards the players. "
#                         "Ensure the update is consistent with the game's ongoing story and player actions. "
#                         "Remember that the whole section under this npc name in the campaign notes will be replaced, so include all the relevant information, not just the update. "
#                         "You usually repeat what was written and append the new information at the end."),
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "npc_name": {
#                     "type": "string",
#                     "description": f"The name of the NPC to be updated.",
#                     "enum": campaign_notes.get_named_data_names('npcs')
#                 },
#                 "new_npc_description": {
#                     "type": "string",
#                     "description": f"New NPC description.",
#                 }

#             },
#             "required": ["npc_name", "new_npc_description"],
#         },
#     }
# },
# ADD POSSIBLE ENDING
# {
#     "type": "function",
#     "function": {
#         "name": "add_ending",
#         "description": ("Introduce a new possible ending to the game. "
#                         "Describe the conditions required to achieve this ending, the key events leading up to it, and its impact on the game world and characters. "
#                         "Endings are usually the results of the main storylines, but can also be connected to sidequests or player actions. "
#                         "Ensure the ending is coherent with the game's narrative and offers a satisfying conclusion to the players' journey, whether it be triumphant, tragic, or ambiguous. "
#                         "This ending is only a narrative reference, it is not guaranteed to occur and could be changed or only partially fulfilled. "
#                         "Try to make each ending unique. Be creative! "),
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "ending_name": {
#                     "type": "string",
#                     "description": f"A name for the ending.",
#                 },
#                 "ending_description": {
#                     "type": "string",
#                     "description": f"Ending description.",
#                 }
#             },
#             "required": ["ending_name", "ending_description"],
#         },
#     }
# },
# UPDATE POSSIBLE ENDING
# {
#     "type": "function",
#     "function": {
#         "name": "update_ending",
#         "description": ("Update an existing possible ending to account for new developments in the game's story or player actions. "
#                         "This could involve changing the conditions to achieve the ending, the events leading up to it, or the nature of the ending itself. "
#                         "Ensure the updated ending remains a plausible and rewarding conclusion to the game's narrative. "
#                         "Ensure the new description is consistent with the game's ongoing story and player actions. "
#                         "Remember that the whole ending notes will be replaced, so include all the relevant information, not just the update. "
#                         "You usually repeat what was written and append the new information at the end to reflect the changes. "),
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "ending_name": {
#                     "type": "string",
#                     "description": f"The name of the ending to be updated.",
#                     "enum": campaign_notes.get_named_data_names('endings')
#                 },
#                 "new_ending_description": {
#                     "type": "string",
#                     "description": f"New ending description.",
#                 }
#             },
#             "required": ["ending_name", "new_ending_description"],
#         },
#     }
# },
