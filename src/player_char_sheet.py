class PlayerCharSheet:
    def __init__(self):
        self.name = "Josh"
        self.race = "human"
        self.class_ = "fighter"
        self.alignment = "neutral"
        self.background = "noble"
        self.level = "1"
        self.experience = "0"
        self.strength = "10"
        self.dexterity = "10"
        self.constitution = "10"
        self.intelligence = "10"
        self.wisdom = "10"
        self.charisma = "10"
        self.health = "10"
        self.ac = "10"
        self.speed = "30"
        self.skills = {}
        self.items = {}
    
    def set_character(self, name, background, strength, dexterity, constitution, intelligence, wisdom, charisma):
        self.name = name
        self.background = background
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma

        # TEMP: defalt starting gear for testing purposes
        self.items = {
            "Gold Pieces": {
                "quantity": 15,
            },
            "Longsword": {
                "quantity": 1,
                "description": "a simple longsword",
            },
            "Chainmail": {
                "quantity": 1,
                "description": "a simple chainmail armor",
            },
            "Shield": {
                "quantity": 1,
                "description": "a simple shield",
            },
            "Standard Adventuring Gear": {
                "quantity": 1,
                "description": "backpack, bedroll, torches, rations, waterskin, etc.",
            },
        }
        ac_chainmail_mod = 5
        ac_shield_mod = 2
        ac_dex_mod = (int(dexterity) - 10) // 2
        self.ac = str(10 + ac_chainmail_mod + ac_shield_mod + ac_dex_mod)

    def _get_skills_desc(self):
        if not self.skills:
            return "-"
        return "\n".join([f"{skill}: level {desc}" for skill, desc in self.skills.items()])

    def _get_items_desc(self):
        if not self.items:
            return "-"
        items_display = []
        for item, details in self.items.items():
            line = f"{details['quantity']} {item}"
            if 'description' in details: # description is not mandatory
                line += f" ({details['description']})"
            items_display.append(line)
        return "\n".join(items_display)
    
    def get_items_names(self):
        return [item for item in self.items]

    def get_prompt(self):
        player_char_sheet_prompt = (
            "PLAYER CHARACTER SHEET:\n"
            "name: " + self.name + "\n"
            "level: " + self.level + "\n"
            "experience: " + self.experience + "\n"
            "race: " + self.race + "\n"
            "class: " + self.class_ + "\n"
            "alignment: " + self.alignment + "\n"
            "background: " + self.background + "\n"
            "strength: " + self.strength + "\n"
            "dexterity: " + self.dexterity + "\n"
            "constitution: " + self.constitution + "\n"
            "intelligence: " + self.intelligence + "\n"
            "wisdom: " + self.wisdom + "\n"
            "charisma: " + self.charisma + "\n"
            "health: " + self.health + "\n"
            "ac: " + self.ac + "\n"
            "speed: " + self.speed + "\n"
            "skills:"  + ("\n" if self.skills else " ") + self._get_skills_desc() + "\n"
            "items:" + ("\n" if self.items else " ") + self._get_items_desc() + "\n"
        )
        return player_char_sheet_prompt

    def set_player_stat(self, name, value):
        # [level, experience, strength, dexterity, constitution, intelligence, wisdom, charisma, health, ac, speed]
        try:
            old_value = getattr(self, name)
            setattr(self, name, str(value))
            return f"Player stat [{name}] changed from {old_value} to {value}."
        except AttributeError:
            return f"Stat [{name}] not found."
    
    def set_player_skill(self, name, level):
        skills = ["Appraise", "Balance", "Bluff", "Climb", "Concentration", "Craft", "Decipher Script", "Diplomacy", "Disable Device", "Disguise", "Escape Artist", "Forgery", "Gather Information", "Handle Animal", "Heal", "Hide", "Intimidate", "Jump", "Knowledge", "Listen", "Move Silently", "Open Lock", "Perform", "Profession", "Ride", "Search", "Sense Motive", "Sleight Of Hand", "Speak Language", "Spellcraft", "Spot", "Survival", "Swim", "Tumble", "Use Magic Device", "Use Rope"]
        if name not in skills:
            return f"Tried to set skill {name} but it is not a valid option. Please use one of the following: {skills}"

        self.skills[name] = level
        return f"Player skill [{name}] set to level [{level}]."
    
    def set_player_item(self, name, quantity, description=""):
        if quantity < 0:
            return f"Tried to set {name} quantity to {quantity} which is invalid."
        if name in self.items:
            old_qty = self.items[name]["quantity"]
            if (quantity == 0):
                del self.items[name]
                return f"Player {name} x{old_qty} removed from inventory."
            self.items[name]["quantity"] = quantity
            return f"Player {name} quantity changed from {old_qty} to {quantity}."
        else:
            if (quantity == 0):
                return f"Tried to remove {name} from inventory but it was not found."
            self.items[name] = {
                "quantity": quantity,
                "description": description,
            }
            return f"Added {name} x{quantity} to player inventory."
