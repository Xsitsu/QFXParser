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
            "ssrc": src,
            "source_dict": {}
        })


    def filter_source(self, src):
        for group in self.groups:
            for term in group["mapping"]:
                if src.name.find(term) != -1 or term == "*":
                    group["ssrc"].add_source(src)
                    group["source_dict"][src.name] = src
                    return

    def _is_all(self, trn):
        return True


