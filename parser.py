import re

import transaction

PATTERN_STATEMENT = "\<STMTTRN\>.*?\<\/STMTTRN\>"
PATTERN_GENERAL = "\<.*?>[^\<]*"
PATTERN_TAG = "\<.*?>"

class Parser:
    def __init__(self):
        self.transactions = []

    def _build_qfx_dict(self, text):
        dct = {}
        matches = re.findall(PATTERN_GENERAL, text)
        for mat in matches:
            tag_list = re.findall(PATTERN_TAG, mat)
            if len(tag_list) > 0:
                tag = tag_list[0]
                tag = tag.replace("<", "")
                tag = tag.replace(">", "")
                dat = re.sub(PATTERN_TAG, "", mat)
                if dat != "":
                    dct[tag] = dat

        return dct

    def _try_assign(self, type_func, trn, dct, dk, tk):
        try:
            if dk in dct.keys() and hasattr(trn, tk):
                setattr(trn, tk, type_func(dct[dk]))
        except:
            print("ERROR with assignment!")

    def parse_qfx(self, text_data):
        statements = re.findall(PATTERN_STATEMENT, text_data)
        for stat in statements:
            trn = transaction.Transaction()
            self.transactions.append(trn)

            dct = self._build_qfx_dict(stat)
            self._try_assign(str, trn, dct, "TRNTYPE", "type")
            self._try_assign(str, trn, dct, "DTPOSTED", "date_posted")
            self._try_assign(float, trn, dct, "TRNAMT", "amount")
            self._try_assign(str, trn, dct, "FITID", "fitid")
            self._try_assign(str, trn, dct, "NAME", "name")
            self._try_assign(str, trn, dct, "MEMO", "memo")


