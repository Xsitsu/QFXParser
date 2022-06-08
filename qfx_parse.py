#!/usr/bin/python3

import argparse
import re
import os


import transaction

######################
### declares
######################
line_break = "-" * 80
pattern = {
    "general": "\<.*?>[^\<]*",
    "tag": "\<.*?>",
    "statement": "\<STMTTRN\>.*?\<\/STMTTRN\>"
}



######################
### functions
######################
def read_all_text(file_name):
    text = ""
    with open(file_name, "r") as file:
        text = file.read()
    return text

def build_statement_list(file_name, pattern):
    text = read_all_text(file_name)
    matches = re.findall(pattern, text)
    return matches

def build_match_list(statement, pattern):
    matches = re.findall(pattern, statement)
    return matches

def build_dictionary(statement):
    gen_pattern = pattern["general"]
    tag_pattern = pattern["tag"]

    dct = {}
    matches = build_match_list(statement, gen_pattern)
    for mat in matches:
        tag_list = re.findall(tag_pattern, mat)
        if len(tag_list) > 0:
            tag = tag_list[0]
            tag = tag.replace("<", "")
            tag = tag.replace(">", "")
            dat = re.sub(tag_pattern, "", mat)
            if dat != "":
                dct[tag] = dat

    return dct

def build_dictionary_list(statement_list):
    dict_list = []
    for statement in statement_list:
        dct = build_dictionary(statement)
        dict_list.append(dct)

    return dict_list

def aggregate_general(dict_list, key):
    aggreg_dict = {}
    for dct in dict_list:
        if key not in dct.keys():
            continue
        k = dct[key]
        if k not in aggreg_dict.keys():
            aggreg_dict[k] = {
                "name": "N/A",
                "add": float(0),
                "sub": float(0),
                "net": float(0)
            }
            if "NAME" in dct.keys():
                aggreg_dict[k]["name"] = dct["NAME"]

        val = float(dct["TRNAMT"])
        aggreg_dict[k]["net"] += val
        if val > 0:
            aggreg_dict[k]["add"] += val
        else:
            aggreg_dict[k]["sub"] -= val

    return aggreg_dict

def sum_transactions(aggreg):
    result = {
        "add": float(0),
        "sub": float(0),
        "net": float(0)
    }

    for k, v in aggreg.items():
        result["add"] += v["add"]
        result["sub"] += v["sub"]
        result["net"] += v["net"]

    return result


def DBG_print_statement(i, statement):
	print("[" + str(i) + "] : " + statement)

def DBG_print_match_list(i, matches):
    use_text = ""
    for mat in matches:
        if use_text != "":
            use_text += " : "
        use_text += mat

    DBG_print_statement(i, use_text)

def DBG_print_statement_list(statements):
    i = 0
    for statement in statements:
        DBG_print_statement(i, statement)
        i += 1

def DBG_print_statement_list_2(statements, pattern):
    i = 0
    for statement in statements:
        matches = re.findall(pattern, statement)
        DBG_print_match_list(i, matches)
        i += 1

def DBG_format_entry(k, v):
    statement = "{" + str(k) + "} " + str(v["net"])
    if v["add"] > 0 and v["sub"] > 0:
        statement += " (+" + str(v["add"]) + " : -" + str(v["sub"]) + ")"
    return statement

def DBG_print_aggreg_base(aggreg):
    i = 0
    for k in sorted(aggreg.keys()):
        v = aggreg[k]
        statement = DBG_format_entry(k, v)
        DBG_print_statement(i, statement)
        i += 1

def DBG_print_aggreg(aggreg):
    income = {}
    expenses = {}

    income_total = float(0)
    expense_total = float(0)

    for k in aggreg.keys():
        v = aggreg[k]
        if v["add"] > 0:
            income[k] = v
            income_total += v["add"]
        else:
            expenses[k] = v
            expense_total += v["sub"]

    print("")
    print("{Income} " + str(income_total))
    print(line_break)
    DBG_print_aggreg_base(income)

    print("")
    print("{Expenses} " + str(expense_total))
    print(line_break)
    DBG_print_aggreg_base(expenses)



def main(file_name):
    statements = build_statement_list(file_name, pattern["statement"])
    dict_list = build_dictionary_list(statements)
    aggreg = aggregate_general(dict_list, "NAME")

    print("Results for: " + file_name)

    if args.total:
        total = sum_transactions(aggreg)
        text = DBG_format_entry("TOTAL", total)
        print(text)

    print(line_break)

    if args.statement:
        DBG_print_statement_list_2(statements, pattern["general"])
    else:
        DBG_print_aggreg(aggreg)
    print("")
    print("")
    print("")



######################
### main
######################
parser = argparse.ArgumentParser()
parser.add_argument("file_name", type=str)
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-s", "--statement", help="output list of statements", action="store_true")
parser.add_argument("-t", "--total", help="output total", action="store_true")

args = parser.parse_args()

if args.verbose:
    print("verbosity turned on")


file_name = os.path.realpath(args.file_name)
#main(file_name)

statements = build_statement_list(file_name, pattern["statement"])
DBG_print_statement(1, statements[0])
