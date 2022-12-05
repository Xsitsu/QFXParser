from entry import Entry
from source import Source
from group import Group


class Logger:
    def __init__(self):
        self._indent = 0
        self._tag_counter = []

        self._tag_counter.append(0)

    def ipp(self):
        self._indent += 1
        self._tag_counter.append(0)

    def imm(self):
        self._indent -= 1
        self._tag_counter.pop()

    def _tag(self):
        tci = len(self._tag_counter) - 1
        i = self._tag_counter[tci]
        self._tag_counter[tci] += 1
        return "[" + str(i) + "]"

    def output(self, text):
        print("\t" * self._indent + text)

    def line_break(self):
        self.output("-" * 80)

    def output_entry(self, entry):
        if type(entry) is Group:
            self.output_group(entry)
        elif type(entry) is Source:
            self.output_source(entry)
        else:
            raise Exception("BAD ENTRY TYPE!")

    def _output_entry_dict(self, entry_dict):
        for k in sorted(entry_dict.keys()):
            entry = entry_dict[k]
            self.output_entry(entry)

    def output_group(self, group):
        self.output(self._tag() + " " + group.format_out())
        entry_dict_income = {}
        entry_dict_expense = {}
        for entry in group.entries:
            if entry.get_total() > 0:
                entry_dict_income[entry.name] = entry
            else:
                entry_dict_expense[entry.name] = entry

        it = group.get_income_total()
        et = group.get_expense_total()

        self.ipp()

        if it > 0:
            self.output("{Income} " + str(group.get_income_total()))
            self.line_break()
            self._output_entry_dict(entry_dict_income)
            self.output("")

        if et > 0:
            self.output("{Expenses} " + str(group.get_expense_total()))
            self.line_break()
            self._output_entry_dict(entry_dict_expense)
            self.output("")

        self.imm()


    def output_source(self, source):
        self.output(self._tag() + " " + source.format_out())










