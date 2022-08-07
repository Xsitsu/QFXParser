

class Logger:
    def __init__(self):
        self._indent = 0
        self.output_group_sources = False
        self.output_source_transactions = False

    def ipp(self):
        self._indent += 1

    def imm(self):
        self._indent -= 1

    def _tag(self, i):
        return "[" + str(i) + "]"

    def output(self, text):
        print("\t" * self._indent + text)

    def line_break(self):
        self.output("-" * 80)

    def output_transaction_list(self, trans_list):
        i = 0
        for t in trans_list:
            output(self._tag(i) + " " + t.format_out())
            i += 1

    def _do_output_source(self, i, src, trans_list):
        self.output(self._tag(i) + " " + src.format_out())
        if trans_list != None:
            self.ipp()
            output_transaction_list(trans_list)
            self.imm()

    def output_source_dict(self, source_dict, t_income, t_expense):
        if t_income > 0:
            i = 0
            self.output("{Income} " + str(t_income))
            self.line_break()
            for k in sorted(source_dict.keys()):
                src = source_dict[k]
                if src.total > 0:
                    tl = None
                    if self.output_source_transactions:
                        tl = src.income_trans
                    self._do_output_source(i, src, tl)
                    i += 1
            self.output("")

        if t_expense > 0:
            i = 0
            self.output("{Expenses} " + str(t_expense))
            self.line_break()
            for k in sorted(source_dict.keys()):
                src = source_dict[k]
                if src.total < 0:
                    tl = None
                    if self.output_source_transactions:
                        tl = src.expense_trans
                    self._do_output_source(i, src, tl)
                    i += 1
            self.output("")
    
    def output_groups(self, group_list):
        self.output("{Groups}")
        self.line_break()
        i = 0
        for gp in group_list.groups:
            src = gp["ssrc"]
            self.output(self._tag(i) + " " + src.format_out())
            i += 1

            if self.output_group_sources:
                self.ipp()
                self.output_source_dict(gp["source_dict"], src.income_total, src.expense_total)
                self.imm()

        self.output("")












