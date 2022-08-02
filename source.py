

class Source:
    def __init__(self):
        self.name = ""
        self.income_trans = []
        self.expense_trans = []
        self.income_total = float(0)
        self.expense_total = float(0)
        self.total = float(0)

    def add_transaction(self, trn):
        amt = trn.amount
        self.total += amt
        if amt > 0:
            self.income_total += amt
            self.income_trans.append(trn)
        else:
            self.expense_total -= amt
            self.expense_trans.append(trn)

    def add_source(self, src):
        for trn in src.income_trans:
            self.add_transaction(trn)
        for trn in src.expense_trans:
            self.add_transaction(trn)

    def format_out(self):
        out = "{" + self.name + "} " + str(self.total)
        if self.income_total > 0 and self.expense_total > 0:
            out += " (+" + str(self.income_total) + " / -" + str(self.expense_total) + ")"
        return out
