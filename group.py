from entry import Entry

class Group(Entry):
    def __init__(self):
        self.entries = []
        self.match_patterns = []

    def get_total(self):
        t = float(0)
        for entry in self.entries:
            t += entry.get_total()
        return t

    def get_income_total(self):
        t = float(0)
        for entry in self.entries:
            t += entry.get_income_total()
        return t

    def get_expense_total(self):
        t = float(0)
        for entry in self.entries:
            t += entry.get_expense_total()
        return t

    def filter_source(self, src):
        for pattern in self.match_patterns:
            if src.name.find(pattern) != -1 or pattern == "*":
                self.entries.append(src)
                return True

        for entry in self.entries:
            if type(entry) is Group:
                if entry.filter_source(src):
                    return True

        return False

