class CampaignNotes:
    def __init__(self):
        self.world_overview = {
            "main_lore": "-",
            "geography_and_climate": "-",
        }
        self.cities = {}
        self.factions = {}
        self.main_storylines = {}
        self.sidequests = {}
        self.npcs = {}
        self.endings = {}

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
            "[MAIN_LORE]: " + self.world_overview["main_lore"] + "\n"
            "[GEOGRAPHY_AND_CLIMATE]: " + self.world_overview["geography_and_climate"] + "\n"
            "[CITIES]:" + ("\n" if self.cities else " ") + self._get_descriptions(self.cities) + "\n"
            "[FACTIONS]:" + ("\n" if self.factions else " ") + self._get_descriptions(self.factions) + "\n"
            "[MAIN_STORYLINES]:" + ("\n" if self.main_storylines else " ") + self._get_descriptions(self.main_storylines) + "\n"
            "[SIDEQUESTS]:" + ("\n" if self.sidequests else " ") + self._get_descriptions(self.sidequests) + "\n"
            "[NPCS]:" + ("\n" if self.npcs else " ") + self._get_descriptions(self.npcs) + "\n"
            "[POSSIBLE_ENDINGS]:" + ("\n" if self.endings else " ") + self._get_descriptions(self.endings) + "\n"
        )
        return campaign_notes_prompt

    def add_named_data(self, data_name, data_key, data_description):
        try:
            data = getattr(self, data_name)
        except AttributeError:
            return f"Invalid data name {data_name}."
        #error if already exists
        if data_key in data:
            return f"Tried to add new data to {data_name} but {data_key} already exists."
        data[data_key] = data_description
        return f"Added new data to {data_name}: {data_key}."
    
    def update_named_data(self, data_name, data_key, new_data_description):
        try:
            data = getattr(self, data_name)
        except AttributeError:
            return f"Invalid data name {data_name}."
        #error if not exists
        if data_key not in data:
            return f"Tried to update {data_key} in {data_name} but it does not exist."
        data[data_key] = new_data_description
        return f"Updated data {data_key}."
    
    def get_named_data_names(self, data_name):
        try:
            data = getattr(self, data_name)
        except AttributeError:
            print(f"Invalid data name {data_name}.")
        return [data_key for data_key in data]


