import source


mapping = [
    {
        "name": "Food Delivery",
        "patterns": [
            "DOORDASH",
            "GRUBHUB"
        ]
    },
    {
        "name": "Fitness",
        "patterns": [
            "MUV FITNESS"
        ]
    },
    {
        "name": "Games",
        "patterns": [
            "EVE ONLINE CCP",
            "Blizzard Ent",
            "STEAMGAMES",
            "Chess.com"
        ]
    },


    {
        "name": "Etc",
        "patterns": ["*"]
    }
]

class Grouper:
    def __init__(self):
        self.groups = []
        self.load_mapping(mapping)

    def load_mapping(self, mappings):
        for mp in mappings:
            self._init_group(mp["name"], mp["patterns"])

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


