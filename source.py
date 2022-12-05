from entry import Entry

class Source(Entry):
    def __init__(self):
        self.income_trans = []
        self.expense_trans = []
        self.income_total = float(0)
        self.expense_total = float(0)
        self.total = float(0)

    def get_total(self):
        return self.total

    def get_income_total(self):
        return self.income_total

    def get_expense_total(self):
        return self.expense_total

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

