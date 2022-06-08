import re

class Transaction:
    pattern_general = "\<.*?>[^\<]"
    pattern_tag = "\<.*?>"

    def __init__(self):
        self.type = ""
        self.date_posted = ""
        self.amount = float(0)
        self.fitid = 0
        self.name = ""
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
                dat = re.sub(tag_pattern, "", mat)
                if dat != "":
                    dct[tag] = dat
        
        return dct

    def parse_statement(self, text):
        dct = _build_dictionary(text)
        if dct["TRNTYPE"] != None:
            self.type = str(dct["TRNTYPE"])
        if dct["DTPOSTED"] != None:
            self.date_posted = str(dct["DTPOSTED"])
        if dct["TRNAMT"] != None:
            self.amount = float(dct["TRNAMT"])
        if dct["FITID"] != None:
            self.fitid = str(dct["FITID"])
        if dct["NAME"] != None:
            self.name = str(dct["NAME"])
        if dct["MEMO"] != None:
            self.memo = str(dct["MEMO"])

    def format_output(self):
        out = ""
        return out




