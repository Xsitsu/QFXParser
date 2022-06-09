import re

pattern_general = "\<.*?>[^\<]*"
pattern_tag = "\<.*?>"

class Transaction:
    def __init__(self):
        self.type = ""
        self.date_posted = ""
        self.amount = float(0)
        self.fitid = 0
        self.name = "_NA"
        self.memo = ""

    def _build_dictionary(self, text):
        dct = {}
        matches = re.findall(pattern_general, text)
        for mat in matches:
            tag_list = re.findall(pattern_tag, mat)
            if len(tag_list) > 0:
                tag = tag_list[0]
                tag = tag.replace("<", "")
                tag = tag.replace(">", "")
                dat = re.sub(pattern_tag, "", mat)
                if dat != "":
                    dct[tag] = dat
        
        return dct

    def _try_assign_str(self, dct, dk, sk):
        try:
            if dk in dct.keys() and hasattr(self, sk):
                setattr(self, sk, str(dct[dk]))
        except:
            setattr(self, sk, "_BAD_VAL_")

    def _try_assign_float(self, dct, dk, sk):
        try:
            if dk in dct.keys() and hasattr(self, sk):
                setattr(self, sk, float(dct[dk]))
        except:
            setattr(self, sk, -0.010101)

    def parse_statement(self, text):
        dct = self._build_dictionary(text)
        self._try_assign_str(dct, "TRNTYPE", "type")
        self._try_assign_str(dct, "DTPOSTED", "date_posted")
        self._try_assign_float(dct, "TRNAMT", "amount")
        self._try_assign_str(dct, "FITID", "fitid")
        self._try_assign_str(dct, "NAME", "name")
        self._try_assign_str(dct, "MEMO", "memo")

    def format_out(self):
        out = "[" + self.type + "] " + str(self.amount) + " \'" + self.memo + "\'"
        return out




