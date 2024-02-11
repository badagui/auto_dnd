from src.campaign_notes import CampaignNotes
from src.player_char_sheet import PlayerCharSheet

def get_system_prompt(campaign_notes: CampaignNotes, player_char_sheet: PlayerCharSheet):
    # returns a system prompt, including base prompt, char sheet and campaign notes
    base_prompt = (
            "You are a very experienced GM managing a D&D 3.5 session.\n"

            "You will tell the player what is happening and give a few options on what to do. "
            "The player can choose one of your suggested actions or describe something different. "
            "If the player describes an impossible or forbidden action (because of the player character sheet, the world, rules, etc), you will explain why that action is invalid. "
            "You are very creative and will evolve the story to give the player an awesome, balanced and challenging experience. "
            "You manage the campaign by having main storylines that guide the story, and side quests that you create as needed. "
            "Side quests usuallly connect or reference the main storylines somehow, but it is ultimately the players decision on what to do. "
            "You will expand on the world lore as you see fit to grow the story as needed to make it epic and awesome. "
            "You have tools to create new cities, sidequests, NPCs, or anything else you need to make your campaign feel vibrant, alive, interconnected, and full of possibilities. "
            "You have tools to edit your notes about the campaign, keeping them up to date with the narrative. "
            "You have tools to edit the player character sheet, including changing stats, skills and items. "
            "You use the available tools as needed to keep track of the story and expand on it. "
            "You will ALWAYS use a tool to register important information BEFORE using it in the story."
            "Your tool use requests and results will appear in the transcription of the session. "
            "You always review your notes and the transcription before answering to make sure your answer is correct and makes sense in the conversation.\n"
        )
    return base_prompt + campaign_notes.get_prompt() + player_char_sheet.get_prompt()

def get_tools_prompt(campaign_notes: CampaignNotes):
    gpt_tools = [
        # UPDATE MAIN LORE
        {
            "type": "function",
            "function": {
                "name": "update_main_lore",
                "description": ("Updates the main lore of the game to reflect new developments, discoveries, or player actions that have impacted the game world's history, mythology, or cultural dynamics. "
                                "This could include the revelation of ancient secrets, shifts in the balance of power, or changes in the perception of key historical events. "
                                "Consider how these changes might affect existing quests, NPCs, and the overall narrative arc of the game. " 
                                "Remember that the whole [MAIN_LORE] section of the campaign notes will be replaced, so include all the relevant information, not just the new information. "
                                "You usually repeat what was written and append the new information at the end."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "new_main_lore": {
                            "type": "string",
                            "description": f"New [MAIN_LORE] description to be replaced in the campaign notes.",
                        }
                    },
                    "required": ["new_main_lore"],
                },
            }
        },
        # UPDATE GEOGRAPHY AND CLIMATE
        {
            "type": "function",
            "function": {
                "name": "update_geography_and_climate",
                "description": ("Update the game's geography and climate to add new information or incorporate changes that have occurred due to in-game events or player actions. "
                                "This can include alterations in the landscape, changes in climate patterns, and the impact of these changes on the flora, fauna, and inhabitants of the game world. "
                                "Explain how these geographical and climatic changes can influence game mechanics, travel, resource availability, and player strategies. "
                                "Ensure that the updated description maintains consistency with what was already written and the ongoing narrative of the game. "
                                "Remember that the whole [GEOGRAPHY_AND_CLIMATE] section of the campaign notes will be replaced, so include all the relevant information, not just the new information. "
                                "You usually repeat what was written and append the new information at the end."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "new_geography_and_climate": {
                            "type": "string",
                            "description": f"New [GEOGRAPHY_AND_CLIMATE] description to be replaced in the campaign notes.",
                        }
                    },
                    "required": ["new_geography_and_climate"],
                },
            }
        },
        # ADD CITY OR VILLAGE
        {
            "type": "function",
            "function": {
                "name": "add_city",
                "description": ("Add a new city, village or settlement into the game world. "
                                "Describe this settlement in no more than two paragraphs, including a general description, location, size, main exits, architecture and culture. "
                                "Outline its economic activities, political structure, notable landmarks, and any unique characteristics. "
                                "Detail how this settlement interacts with the surrounding environment and other factions or settlements. "
                                "Describe how players can interact with this new setting, including potential quests, challenges, mysteries, and characters they may encounter. "
                                "This addition should enrich the game world, offering new opportunities for exploration and interaction."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city_name": {
                            "type": "string",
                            "description": f"Name of the city, village or settlement.",
                        },
                        "city_description": {
                            "type": "string",
                            "description": f"Description of the city, village or settlement.",
                        }
                    },
                    "required": ["city_name", "city_description"],
                },
            }
        },
        # UPDATE CITY OR VILLAGE
        {
            "type": "function",
            "function": {
                "name": "update_city",
                "description": ("Updates an existing city, village or settlement, adding new information or annotating changes. "
                                "Changes could be due to world events, player actions, or natural progression. "
                                "This could include changes in leadership, shifts in economic or political conditions, alterations in population, cultural aspects, or physical transformations. "
                                "Ensure that the updated description maintains consistency with what was already written and the ongoing narrative of the game. "
                                "Remember that the whole section under this city name in the campaign notes will be replaced, so include all the relevant information, not just the new information. "
                                "You usually repeat what was written and append the new information at the end."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city_name": {
                            "type": "string",
                            "description": f"Name of the city, village or settlement that will be edited.",
                            "enum": campaign_notes.get_named_data_names('cities')
                        },
                        "new_city_description": {
                            "type": "string",
                            "description": f"New description for this city, village or settlement.",
                        }
                    },
                    "required": ["city_name", "new_city_description"],
                },
            }
        },
        # ADD FACTION
        {
            "type": "function",
            "function": {
                "name": "add_faction",
                "description": ("Add a new faction, group, guild, clan or tribe to the game. "
                                "You should describe it in no more than two paragraphs, including its name, general description, goals, values, influence, size, enemies, loyalties and key members. "
                                "Explain how this group interacts with other groups, cities, and the players. "
                                "Include potential conflicts, alliances, and impacts on the game's broader narrative. "
                                "This group should offer new avenues for player involvement, whether through quests, diplomacy, or conflict, and add depth to the political and social landscape of the game world. "
                                "Try to make each faction unique somehow. Be creative!"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "faction_name": {
                            "type": "string",
                            "description": f"Faction name.",
                        },
                        "faction_description": {
                            "type": "string",
                            "description": f"Faction description.",
                        }
                    },
                    "required": ["faction_name", "faction_description"],
                },
            }
        },
        # UPDATE FACTION
        {
            "type": "function",
            "function": {
                "name": "update_faction",
                "description": ("Update an existant faction, group, guild, clan or tribe, adding information about important changes that might have happened since its inception, due to player actions, world events, or internal dynamics. "
                                "This update should detail shifts in the faction's leadership, goals, alliances, or conflicts. "
                                "Explain how these changes impact the faction's relationship with the players and other entities in the game world. "
                                "Ensure that the updated description maintains consistency with what was already written and the ongoing narrative of the game."
                                "Remember that the whole section under this faction name in the campaign notes will be replaced, so include all the relevant information, not just the new information. "
                                "You usually repeat what was written and append the new information at the end."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "faction_name": {
                            "type": "string",
                            "description": f"The name of the faction to be updated.",
                            "enum": campaign_notes.get_named_data_names('factions')
                        },
                        "new_faction_description": {
                            "type": "string",
                            "description": f"New faction description.",
                        }
                    },
                    "required": ["faction_name", "new_faction_description"],
                },
            }
        },
        # ADD MAIN STORYLINE
        {
            "type": "function",
            "function": {
                "name": "add_main_storyline",
                "description": ("Add a new main storyline to the game. "
                                "These are the big story archs with world level impact, usually converging to one of the possible endings. "
                                "In no more than two paragraphs, describe the nature of this storyline, including its origin, involved parties and potential impacts on the game world. "
                                "Outline the key elements, such as clues, locations, and NPCs connected to it. "
                                "Indicate how it might unfold and affect the players' journey, but leave enough ambiguity to allow for player-driven exploration and resolution. "
                                "Try to integrate this storyline with existing elements for a more immersive experience. "
                                "Try to make it unique. Be creative!"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "storyline_name": {
                            "type": "string",
                            "description": f"A name for this storyline.",
                        },
                        "storyline_description": {
                            "type": "string",
                            "description": f"Storyline description.",
                        }
                    },
                    "required": ["storyline_name", "storyline_description"],
                },
            }
        },
        # UPDATE MAIN STORYLINE
        {
            "type": "function",
            "function": {
                "name": "update_main_storyline",
                "description": ("Update an existing main storyline in the game, detailing significant developments or resolutions that have occurred. "
                                "This should include changes in the involved parties, new clues or revelations, shifts in the conflict's impact on the world, and how these developments could alter the players' interaction with this narrative element. "
                                "Ensure the update is consistent with the game's ongoing story and player actions. "
                                "Remember to advance the main storylines as the campaign advances."
                                "Remember that the whole section under this storyline name in the campaign notes will be replaced, so include all the relevant information, not just the update. "
                                "You usually repeat what was written and append the new information at the end."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "storyline_name": {
                            "type": "string",
                            "description": f"The name of the storyline to be updated.",
                            "enum": campaign_notes.get_named_data_names('main_storylines')
                        },
                        "new_storyline_description": {
                            "type": "string",
                            "description": f"New storyline description.",
                        }
                    },
                    "required": ["storyline_name", "new_storyline_description"],
                },
            }
        },
        # ADD SIDEQUEST
        {
            "type": "function",
            "function": {
                "name": "add_sidequest",
                "description": ("Add a new game sidequest." 
                                "Describe it in two paragraphs maximum, including the quest's nature, objectives, rewards, and other relevant info."
                                "Design it to be varied, incorporating puzzles, combat, exploration, or diplomacy, and ensure it enhances the game world, encouraging exploration and interaction. "
                                "Sidequests may be independent or linked to larger story arcs, potentially influencing the narrative with powerful items, connecting to other quests, or intertwining with the main storyline. "
                                "Emphasize creativity and uniqueness."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sidequest_name": {
                            "type": "string",
                            "description": f"A name for this sidequest.",
                        },
                        "sidequest_description": {
                            "type": "string",
                            "description": f"Sidequest description.",
                        }
                    },
                    "required": ["sidequest_name", "sidequest_description"],
                },
            }
        },
        # UPDATE SIDEQUEST
        {
            "type": "function",
            "function": {
                "name": "update_sidequest",
                "description": ("Updates an existing sidequest, reflecting changes based on player actions, world events or time passing. "
                                "This could include alterations in quest objectives, the introduction of new challenges or rewards, or changes in the quest's scope"
                                "Ensure the update is consistent with the game's ongoing story and player actions. "
                                "Remember that the whole section under this sidequest name in the campaign notes will be replaced, so include all the relevant information, not just the update. "
                                "You usually repeat what was written and append the new information at the end."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sidequest_name": {
                            "type": "string",
                            "description": f"The name of the sidequest to be updated.",
                            "enum": campaign_notes.get_named_data_names('sidequests')
                        },
                        "new_sidequest_description": {
                            "type": "string",
                            "description": f"New sidequest description.",
                        }
                    },
                    "required": ["sidequest_name", "new_sidequest_description"],
                },
            }
        },
        # ADD NPC
        {
            "type": "function",
            "function": {
                "name": "add_npc",
                "description": ("Create a new NPC for the game. "
                                "Describe the NPC in detail, including their appearance, personality, background, and role in the game world. "
                                "You can outline the NPC relationships with factions, cities, other NPCs, and how they can interact with the players. "
                                "Include potential quests, information, or services they might offer, and how they might change or evolve throughout the game. "
                                "Try to make it unique. Be creative!"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "npc_name": {
                            "type": "string",
                            "description": f"Name of the NPC.",
                        },
                        "npc_description": {
                            "type": "string",
                            "description": f"Description of the NPC.",
                        }
                    },
                    "required": ["npc_name", "npc_description"],
                },
            }
        },
        # UPDATE NPC
        {
            "type": "function",
            "function": {
                "name": "update_npc",
                "description": ("Update an existing NPC, adding extra information. "
                                "You can use this to add a stat needed for an interaction, or to log changes in their character. "
                                "Remember to log any changes in their role, available quests, information, or services, as well as their demeanor towards the players. "
                                "Ensure the update is consistent with the game's ongoing story and player actions. "
                                "Remember that the whole section under this npc name in the campaign notes will be replaced, so include all the relevant information, not just the update. "
                                "You usually repeat what was written and append the new information at the end."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "npc_name": {
                            "type": "string",
                            "description": f"The name of the NPC to be updated.",
                            "enum": campaign_notes.get_named_data_names('npcs')
                        },
                        "new_npc_description": {
                            "type": "string",
                            "description": f"New NPC description.",
                        }

                    },
                    "required": ["npc_name", "new_npc_description"],
                },
            }
        },
        # ADD POSSIBLE ENDING
        {
            "type": "function",
            "function": {
                "name": "add_ending",
                "description": ("Introduce a new possible ending to the game. "
                                "Describe the conditions required to achieve this ending, the key events leading up to it, and its impact on the game world and characters. "
                                "Endings are usually the results of the main storylines, but can also be connected to sidequests or player actions. "
                                "Ensure the ending is coherent with the game's narrative and offers a satisfying conclusion to the players' journey, whether it be triumphant, tragic, or ambiguous. "
                                "This ending is only a narrative reference, it is not guaranteed to occur and could be changed or only partially fulfilled. "
                                "Try to make each ending unique. Be creative! "),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ending_name": {
                            "type": "string",
                            "description": f"A name for the ending.",
                        },
                        "ending_description": {
                            "type": "string",
                            "description": f"Ending description.",
                        }
                    },
                    "required": ["ending_name", "ending_description"],
                },
            }
        },
        # UPDATE POSSIBLE ENDING
        {
            "type": "function",
            "function": {
                "name": "update_ending",
                "description": ("Update an existing possible ending to account for new developments in the game's story or player actions. "
                                "This could involve changing the conditions to achieve the ending, the events leading up to it, or the nature of the ending itself. "
                                "Ensure the updated ending remains a plausible and rewarding conclusion to the game's narrative. "
                                "Ensure the new description is consistent with the game's ongoing story and player actions. "
                                "Remember that the whole ending notes will be replaced, so include all the relevant information, not just the update. "
                                "You usually repeat what was written and append the new information at the end to reflect the changes. "),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ending_name": {
                            "type": "string",
                            "description": f"The name of the ending to be updated.",
                            "enum": campaign_notes.get_named_data_names('endings')
                        },
                        "new_ending_description": {
                            "type": "string",
                            "description": f"New ending description.",
                        }
                    },
                    "required": ["ending_name", "new_ending_description"],
                },
            }
        },
        # CHAR SHEET
        {
            "type": "function",
            "function": {
                "name": "set_player_stat",
                "description": ("Set a stat value in the player character sheet, tracking character progression and changes due to gameplay, leveling up, or equipment modifications, etc."
                                "ALWAYS use this tool to update stats BEFORE describing the stat change to the player."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name":{
                            "type": "string",
                            "description": f"The name of the stat to be set.",
                            "enum": ["level", "experience", "strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma", "health", "ac", "initiative", "speed"]
                        },
                        "value":{
                            "type": "integer",
                            "description": f"The new value of the stat.",
                        }
                    },
                    "required": ["name", "value"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "set_player_skill",
                "description": ("Set a skill in the player character sheet. "
                                "Use this this tool to update skill levels reflecting character development, training, or temporary effects."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": f"The name of the skill to be changed.",
                            "enum": ["Appraise", "Balance", "Bluff", "Climb", "Concentration", "Craft", "Decipher Script", "Diplomacy", "Disable Device", "Disguise", "Escape Artist", "Forgery", "Gather Information", "Handle Animal", "Heal", "Hide", "Intimidate", "Jump", "Knowledge", "Listen", "Move Silently", "Open Lock", "Perform", "Profession", "Ride", "Search", "Sense Motive", "Sleight Of Hand", "Speak Language", "Spellcraft", "Spot", "Survival", "Swim", "Tumble", "Use Magic Device", "Use Rope"]
                        },
                        "level": {
                            "type": "integer",
                            "description": f"The new level of the skill.",
                        }
                    },
                    "required": ["name", "level"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "set_player_item",
                "description": ("Set an item quantity in the player's inventory. "
                                "If the item does not exist, it will be added to the inventory. "
                                "If the item already exists, its quantity will be updated. "
                                "If the quantity is set to zero, the item will be removed from the inventory. "
                                "When removing an item, ensure that its ongoing effects or uses are no longer accessible to the player by updating its character sheet. "
                                "Provide the item's name, quantity and a description such as its appearance, function, and any unique characteristics. "
                                "The description is not needed for common items (consumables, equipments, utilities, etc) and 1 sentence maximum for more complex items (quest items, magical items, lore items, etc). "
                                "ALWAYS use this tool to add/remove items BEFORE saying to the player they got/lost items."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": f"Item name.",
                        },
                        "quantity": {
                            "type": "integer",
                            "description": f"Item quantity.",
                        },
                        "description": {
                            "type": "string",
                            "description": f"optional: item description. Only used when adding a new item.",
                        }
                    },
                    "required": ["name", "quantity"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "roll_dices",
                "description": ("Roll [count] dices, each with [sides] sides. "
                                "Use this tool for determining outcomes in gameplay, such as combat events, ability checks, random events, etc. "
                                "You can call this function multiple times to roll different sided dices."
                                "Consider rolling different events separately for clarity."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "count": {
                            "type": "integer",
                            "description": f"Number of dices to be rolled.",
                        },
                        "sides": {
                            "type": "integer",
                            "description": f"Number of sides of each dice.",
                        }
                    },
                    "required": ["count", "sides"],
                },
            }
        },
    ]
    return gpt_tools
