

class Transaction:
    def __init__(self):
        self.type = ""
        self.date_posted = ""
        self.amount = float(0)
        self.fitid = 0
        self.name = "_NA"
        self.memo = ""

    def format_out(self):
        out = "[" + self.type + "] " + str(self.amount) + " \'" + self.memo + "\'"
        return out




