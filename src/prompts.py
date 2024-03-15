from src.campaign_notes import CampaignNotes
from src.player_char_sheet import PlayerCharSheet

def get_new_geography_and_climate_prompts():
    prompt = ("Create a description for the GEOGRAPHY AND CLIMATE section of a new Dungeons & Dragons world. "
              "This should be 40 words max. "
              "Be creative, but balance innovation with tradition. "
              "Don't overuse magical elements.")
    messages = [
        {'role': 'system', 'content': 'You are a very experienced GM creating a D&D 3.5 campaign.'},
        {'role': 'user', 'content': prompt}
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "create_new_geography_and_climate",
                "description": ("Create a new Dungeons & Dragons campaign notes entry for the GEOGRAPHY AND CLIMATE section."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": f"Simple campaign name based on the world and its environment. Ex. Realms of X, Lands of Y, The World of Z, etc.",
                        },
                        "description": {
                            "type": "string",
                            "description": f"Geography and climate description. 50 words max.",
                        }
                    },
                    "required": ["name", "description"],
                },
            }
        },
    ]
    tool_choice = {"type": "function", "function": {"name": "create_new_geography_and_climate"}}
    return messages, tools, tool_choice

def get_new_world_lore_prompts(campaign_notes: CampaignNotes):
    prompt = ("Create a description for the WORLD LORE section of our new Dungeons & Dragons world. "
              "This could include history, mythology, cultural dynamics or other relevant information about the game world. "
              "Make sure it makes sense with your campaign notes and does not contradict it. "
              "This should be 50 words max. "
              "Be creative, but balance innovation with tradition. "
              "Don't overuse magical elements.")
    prompt += campaign_notes.get_prompt()
    messages = [
        {'role': 'system', 'content': 'You are a very experienced GM creating a D&D 3.5 campaign.'},
        {'role': 'user', 'content': prompt}
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "create_new_world_lore",
                "description": ("Create a new Dungeons & Dragons campaign notes entry for the WORLD LORE section. "),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "description": {
                            "type": "string",
                            "description": f"World lore description. 50 words max.",
                        }
                    },
                    "required": ["description"],
                },
            }
        },
    ]
    tool_choice = {"type": "function", "function": {"name": "create_new_world_lore"}}
    return messages, tools, tool_choice

def get_new_main_storyline_prompts(campaign_notes: CampaignNotes):
    prompt = ("Create a description for the MAIN STORYLINE section of a new Dungeons & Dragons world. "
              "This is a main story arch, with world level impact. "
              "This should be awesome and epic, with potential to converge to many possible endings. "
              "Make sure it makes sense with your campaign notes and does not contradict it. "
              "This should be 2 paragraphs, 80 words max. "
              "The first paragraph should focus on the storyline origins and current settings. "
              "The second paragraph should focus on the possible developments and resolutions, especially if the player does not act on it. "
              "Be creative, but balance innovation with tradition.")
    prompt += campaign_notes.get_prompt()
    messages = [
        {'role': 'system', 'content': 'You are a very experienced GM creating a D&D 3.5 campaign.'},
        {'role': 'user', 'content': prompt}
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "create_new_main_storyline",
                "description": ("Create a new Dungeons & Dragons campaign notes entry for the MAIN STORYLINE section. "),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "description": {
                            "type": "string",
                            "description": f"Main storyline description. 80 words max.",
                        }
                    },
                    "required": ["description"],
                },
            }
        },
    ]
    tool_choice = {"type": "function", "function": {"name": "create_new_main_storyline"}}
    return messages, tools, tool_choice

def get_new_starting_city_prompts(campaign_notes: CampaignNotes):
    prompt = ("Create the starting city for a Dungeons & Dragons campaign. "
              "Describe this city location, size, main exits, architecture and culture. "
              "Outline its economic activities, political structure, notable landmarks, and any unique characteristics. "
              "Detail how this city interacts with the surrounding environment and other factions or cities. "
              "This city should enrich the game world, offering opportunities for exploration and interaction. "
              "Make sure it makes sense with your campaign notes and does not contradict it. "
              "This should be 60 words max. "
              "Be creative, but balance innovation with tradition.\n")
    prompt += campaign_notes.get_prompt()
    messages = [
        {'role': 'system', 'content': 'You are a very experienced GM creating a D&D 3.5 campaign.'},
        {'role': 'user', 'content': prompt}
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "create_starting_city",
                "description": ("Creates a new starting city for a Dungeons & Dragons campaign. "),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": f"City name.",
                        },
                        "description": {
                            "type": "string",
                            "description": f"City description. 60 words max.",
                        }
                    },
                    "required": ["name", "description"],
                },
            }
        },
    ]
    tool_choice = {"type": "function", "function": {"name": "create_starting_city"}}
    return messages, tools, tool_choice

def get_campaign_introduction_prompt(campaign_notes: CampaignNotes, player_char_sheet: PlayerCharSheet):
    # returns a system prompt, including base prompt, char sheet and campaign notes
    prompt = (
        "You are a very experienced GM about to start a D&D 3.5 campaign and you will give the player an awesome introduction in 150 words max.\n"
        "Tailor the introduction to the player character and campaign notes. "
        "The player starts in the city contained in the campaign notes. "
        "After the introduction you will write an extra very small paragraph, telling the player where he is and suggesting some courses of action. Do not make a list, just say it casually, leaving openness for the player to describe something else."
    )
    prompt += campaign_notes.get_prompt() + player_char_sheet.get_prompt()
    messages = [
        {'role': 'system', 'content': prompt},
    ]
    return messages

def get_gm_response_prompts(campaign_notes: CampaignNotes, player_char_sheet: PlayerCharSheet, summaries_prompt: str):
    # returns a system prompt, including base prompt, char sheet and campaign notes
    system_prompt = (
        "You are a very experienced GM managing a Dungeons & Dragons 3.5 campaign.\n"

        "Follow the D&D 3.5 rules and never simplify rules or game mechanics. "
        "Never assume the player did something without the player describing it. "
        "Write short responses and leave space for the player to act. "
        "If the player describes a forbidden or impossible action, you will explain why that action is invalid. "
        "Manage the campaign by having a main storyline that guide the story, and side quests that you create as needed. "
        "It is ultimately the players decision on what to do. "
        "You have tools to edit your notes about the campaign, keeping them up to date with the narrative. "
        "You have tools to edit the player character sheet, including changing stats, skills and items. "
        "You use the available tools as needed to keep track of the story and expand on it. "
        "You will ALWAYS use a tool to register important information as soon as possible. "
        "You always review your notes and the transcription before answering to make sure your answer is correct and makes sense. "
        "Don't make make a list or suggest the player on what to do. Just describe the world around and leave the player free to take his action. "
    )
    
    system_prompt += campaign_notes.get_prompt() + player_char_sheet.get_prompt() + summaries_prompt
    tools = _get_gm_tools()
    return system_prompt, tools

def _get_gm_tools():
    tools = [
        # ADD CITY OR VILLAGE
        {
            "type": "function",
            "function": {
                "name": "add_city",
                "description": ("Add a new city, village or settlement into the game world. "
                                "Describe this settlement in 60 words max., including a general description, location, size, main exits, architecture, etc. "
                                "Detail how this settlement interacts with the surrounding environment and other factions or settlements. "
                                "This addition should enrich the game world, offering new opportunities for exploration and interaction."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": f"name of the city, village or settlement",
                        },
                        "description": {
                            "type": "string",
                            "description": f"description of the city, village or settlement. 60 words max.",
                        }
                    },
                    "required": ["name", "description"],
                },
            }
        },
        # ADD FACTION
        {
            "type": "function",
            "function": {
                "name": "add_faction",
                "description": ("Add a new faction, group, guild, clan or tribe to the game. "
                                "You should describe it in 60 words max., including its name, general description, goals, etc. "
                                "Explain how this group interacts with others and the player. "
                                "This addition should offer new avenues for player involvement, whether through quests, diplomacy, or conflict, and add depth to the game world. "
                                "Make it unique somehow. Be creative!"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": f"faction name",
                        },
                        "description": {
                            "type": "string",
                            "description": f"faction description",
                        }
                    },
                    "required": ["name", "description"],
                },
            }
        },
        # ADD SIDEQUEST
        {
            "type": "function",
            "function": {
                "name": "add_sidequest",
                "description": ("Add a new sidequest." 
                                "Describe it in 60 words max., including the quest nature, objectives, rewards, and other relevant info. "
                                "Design it to be varied, incorporating puzzles, combat, exploration, or diplomacy, and ensure it enhances the game world, encouraging exploration and interaction. "
                                "Sidequests may be independent or linked to larger story arcs, potentially influencing the narrative with powerful items, connecting to other quests, or intertwining with the main storyline. "
                                "Emphasize creativity and uniqueness. Be creative!"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": f"sidequest name",
                        },
                        "description": {
                            "type": "string",
                            "description": f"sidequest description",
                        }
                    },
                    "required": ["name", "description"],
                },
            }
        },
        # ADD NPC
        {
            "type": "function",
            "function": {
                "name": "add_npc",
                "description": ("Create a new NPC for the game. "
                                "Describe the NPC in 50 words max. "
                                "Consider including things like their appearance, personality, background, and role in the game world. "
                                "Try to make it unique. Be creative!"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": f"NPC name",
                        },
                        "description": {
                            "type": "string",
                            "description": f"NPC description",
                        }
                    },
                    "required": ["name", "description"],
                },
            }
        },
        # SET CHAR SHEET
        {
            "type": "function",
            "function": {
                "name": "set_player_stat",
                "description": ("Set a stat value in the player character sheet, tracking character progression and changes due to gameplay, leveling up, equipment modifications, etc."
                                "ALWAYS use this tool to update stats BEFORE or IMMEDIATELY AFTER describing the stat change to the player."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name":{
                            "type": "string",
                            "description": "stat name",
                            "enum": ["level", "experience", "strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma", "health", "ac", "initiative", "speed"]
                        },
                        "value":{
                            "type": "integer",
                            "description": "new stat value",
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
                            "description": "skill name",
                            "enum": ["Appraise", "Balance", "Bluff", "Climb", "Concentration", "Craft", "Decipher Script", "Diplomacy", "Disable Device", "Disguise", "Escape Artist", "Forgery", "Gather Information", "Handle Animal", "Heal", "Hide", "Intimidate", "Jump", "Knowledge", "Listen", "Move Silently", "Open Lock", "Perform", "Profession", "Ride", "Search", "Sense Motive", "Sleight Of Hand", "Speak Language", "Spellcraft", "Spot", "Survival", "Swim", "Tumble", "Use Magic Device", "Use Rope"]
                        },
                        "level": {
                            "type": "integer",
                            "description": "new skill value",
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
                "description": ("Set an item quantity in the player's inventory, adding if it doesn't exist. "
                                "When removing an item, ensure that its ongoing effects or uses are no longer accessible to the player by updating its character sheet. "
                                "A short description is only needed for more complex items (quest items, magical items, lore items, etc). "
                                "ALWAYS use this tool to add / remove items BEFORE or IMMEDIATELY AFTER saying to the player they got / lost / used an item."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "item name",
                        },
                        "quantity": {
                            "type": "integer",
                            "description": f"item quantity",
                        },
                        "description": {
                            "type": "string",
                            "description": f"item short description (optional)",
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
                                "Use this tool for determining outcomes in gameplay, such as initiative, attacks, ability checks, random events, etc. "
                                "You can call this function multiple times to roll different sided dices. "
                                "Roll different events separately for clarity."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "count": {
                            "type": "integer",
                            "description": f"number of dices to be rolled",
                        },
                        "sides": {
                            "type": "integer",
                            "description": f"number of sides of each dice",
                        }
                    },
                    "required": ["count", "sides"],
                },
            }
        },
    ]
    return tools

def get_summarizer_prompt(resume_msg: str):
    prompt = (
        "You are an experienced tabletop RPG GM assistant and it's your job to summarize parts of the session based on its transcription. \n"
        "Summarize the given transcription in a short paragraph, without losing any important detail. "
        "Don't use embelishments, just state the facts. This is not a creative writing task. "
        "Write only the summary, nothing else. No commentaries or explanations. "
    )
    messages = [
        {'role': 'system', 'content': prompt},
        {'role': 'user', 'content': 'Transcription: ' + resume_msg}
    ]
    return messages

def get_world_description_summary_prompt(campaign_notes: CampaignNotes):
    prompt = (
        "Summarize the given tabletop RPG world description in a very short paragraph. "
        "Start by saying a greeting using the world name, ie: 'Welcome to the world of [WORLD_NAME].' or something similar. "
        "Then, in a new line, write the short summary. "
        "Write only what was asked, nothing else. No extra commentaries or explanations. "
    )
    messages = [
        {'role': 'system', 'content': prompt},
        {'role': 'user', 'content': 'World name: ' + campaign_notes.campaign_name + ' \nDescription: ' + campaign_notes.geography_and_climate + ' ' + campaign_notes.world_lore + ' ' + campaign_notes.main_storyline}
    ]
    return messages

def get_image_world_creation_prompt(campaign_notes: CampaignNotes):
    prompt = 'An wallpaper for a new dungeons and dragons world. Only the image, no titles, no texts, no characters. World description: ' + campaign_notes.geography_and_climate + ' ' + campaign_notes.world_lore
    print('image prompt:\n', prompt)
    return prompt