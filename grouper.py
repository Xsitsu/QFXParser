from group import Group


class Grouper:
    def __init__(self):
        self.groups = []

    def load_mapping(self, mappings):
        for mp in mappings:
            self.groups.append(self._init_group(mp))

    def _init_group(self, group_dat):
        g_name = group_dat["name"] if "name" in group_dat else "NO_NAME"
        g_patterns = group_dat["patterns"] if "patterns" in group_dat else []
        g_groups = group_dat["groups"] if "groups" in group_dat else []

        group = Group()
        group.name = g_name
        group.match_patterns = g_patterns

        for gp in g_groups:
            group.entries.append(self._init_group(gp))

        return group

    def filter_source(self, src):
        for group in self.groups:
            if group.filter_source(src):
                return

    def _is_all(self, trn):
        return True


