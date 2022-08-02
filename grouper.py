import source


mapping = {
    "food_deliv": [
        "DOORDASH",
        "GRUBHUB"
    ],
    "fitness": [
        "MUV FITNESS"
    ],
    "games": [
        "EVE ONLINE CCP",
        "Blizzard Ent",
        "STEAMGAMES",
        "Chess.com"
    ],

    "all": ["*"]
}

class Grouper:
    def __init__(self):
        self.groups = []

        self._init_group("Food Delivery", mapping["food_deliv"])
        self._init_group("Fitness", mapping["fitness"])
        self._init_group("Games", mapping["games"])
        self._init_group("Etc", mapping["all"])

    def _init_group(self, key, mappings):
        src = source.Source()
        src.name = key

        self.groups.append({
            "name": key,
            "mapping": mappings,
            "ssrc": src
        })


    def filter_transaction(self, trn):
        for group in self.groups:
            for term in group["mapping"]:
                if trn.name.find(term) != -1 or term == "*":
                    group["ssrc"].add_transaction(trn)
                    return

    def _is_all(self, trn):
        return True


