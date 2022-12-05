

class Entry:
    def __init__(self):
        self.name = ""

    def format_out(self):
        t = self.get_total()
        it = self.get_income_total()
        et = self.get_expense_total()

        out = "{" + self.name + "} " + str(t)
        if it > 0 and et > 0:
            out += " (" + str(it) + " / -" + str(et) + ")"
        return out

    def get_total(self):
        raise Exception("NotImplementedException")

    def get_income_total(self):
        raise Exception("NotImplementedException")

    def get_expense_total(self):
        raise Exception("NotImplementedException")

