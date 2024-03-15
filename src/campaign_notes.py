class CampaignNotes:
    def __init__(self):
        self.campaign_name = "-"
        self.geography_and_climate = "-"
        self.world_lore = "-"
        self.main_storyline = "-"
        self.cities = {}
        self.factions = {}
        self.sidequests = {}
        self.npcs = {}

        # self.cities = {
        #     "Pendleton": ("Nestled in a gentle valley at the crossroads of ancient trade routes lies Pendleton, a bustling",
        #         "medium-sized city known for its rich merchant guilds and vibrant markets. A high stone wall encircles Pendleton, "
        #         "with four massive gates facing the cardinal directions, each leading to a well-trodden path that disappears into "
        #         "the horizon. Pendleton's unique skyline is marked by elegant spires and sturdy warehouses, evidencing its "
        #         "commercial prosperity. The heart of the city is the Grand Plaza, where traders from distant lands exchange exotic "
        #         "wares, and local craftsmen peddle their fine goods. Governed by a council of influential merchants and nobles, "
        #         "Pendleton has managed to stay politically neutral, becoming a safe haven for adventurers, traders, and diplomats alike."),
        # }

    def _get_descriptions(self, items_dict):
        if not items_dict:
            return "-"
        return "\n".join([f"{key}: {desc}" for key, desc in items_dict.items()])

    def get_prompt(self):
        campaign_notes_prompt = (
            "GM CAMPAIGN NOTES:\n"
            "[CAMPAIGN_NAME]: " + self.campaign_name + "\n"
            "[GEOGRAPHY_AND_CLIMATE]: " + self.geography_and_climate + "\n"
            "[WORLD_LORE]: " + self.world_lore + "\n"
            "[MAIN_STORYLINE]: " + self.main_storyline + "\n"
            "[CITIES]:" + ("\n" if self.cities else " ") + self._get_descriptions(self.cities) + "\n"
            "[FACTIONS]:" + ("\n" if self.factions else " ") + self._get_descriptions(self.factions) + "\n"
            "[SIDEQUESTS]:" + ("\n" if self.sidequests else " ") + self._get_descriptions(self.sidequests) + "\n"
            "[NPCS]:" + ("\n" if self.npcs else " ") + self._get_descriptions(self.npcs) + "\n"
        )
        return campaign_notes_prompt

    def create_new_geography_and_climate(self, name, description):
        self.campaign_name = name
        self.geography_and_climate = description
        return f"Created geography and climate."

    def create_new_world_lore(self, description):
        self.world_lore = description
        return f"Created new world lore."

    def create_new_main_storyline(self, description):
        self.main_storyline = description
        return f"Created new main storyline."
    
    def create_starting_city(self, name, description):
        self.cities[name] = description
        return f"Created new starting city: {name}."
    
    def add_city(self, name, description):
        self.cities[name] = description
        return f"Added city: {name}."

    def add_faction(self, name, description):
        self.factions[name] = description
        return f"Added faction: {name}."

    def add_sidequest(self, name, description):
        self.sidequests[name] = description
        return f"Added sidequest: {name}."

    def add_npc(self, name, description):
        self.npcs[name] = description
        return f"Added NPC {name}."
