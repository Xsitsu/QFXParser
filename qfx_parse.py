#!/usr/bin/python3

import argparse
import re
import os

import transaction
import source
import grouper

######################
### declares
######################
line_break = "-" * 80
pattern = {
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

def build_transaction_list(statement_list):
    transactions = []
    for statement in statement_list:
        trn = transaction.Transaction()
        trn.parse_statement(statement)
        transactions.append(trn)

    return transactions

def build_source_dict(transaction_list):
    sources = {}
    for tran in transaction_list:
        k = tran.name
        if k not in sources.keys():
            src = source.Source()
            src.name = tran.name
            sources[k] = src

        sources[k].add_transaction(tran)

    return sources

def build_groups(transaction_list):
    group = grouper.Grouper()

    for tran in transaction_list:
        group.filter_transaction(tran)

    return group

def sum_transactions(source_dict):
    src = source.Source()
    src.name = "TOTAL"

    for k, v in source_dict.items():
        src.income_total += v.income_total
        src.expense_total += v.expense_total
        src.total += v.total

    return src






def main(file_name):
    statements = build_statement_list(file_name, pattern["statement"])
    transactions = build_transaction_list(statements)
    sources = build_source_dict(transactions)
    groups = build_groups(transactions)
    total = sum_transactions(sources)


    ## Header
    print("Results for: " + file_name)
    if args.total:
        print(total.format_out())
    print(line_break)
    print("")

    ## Groups
    if args.group:
        print("{Groups}")
        print(line_break)
        i = 0
        for gp in groups.groups:
            print("[" + str(i) + "] " + gp["ssrc"].format_out())
            i += 1
        print("")


    ## Income
    print("{Income} " + str(total.income_total))
    print(line_break)
    i = 0
    for k in sorted(sources.keys()):
        src = sources[k]
        if src.total > 0:
            print("[" + str(i) + "] " + src.format_out())
            if args.statement:
                ii = 0
                for tran in src.income_trans:
                    print("\t" + tran.format_out())
                    ii += 1
            i += 1
    print("")

    ## Expenses
    print("{Expenses} " + str(total.expense_total))
    print(line_break)
    i = 0
    for k in sorted(sources.keys()):
        src = sources[k]
        if src.total < 0:
            print("[" + str(i) + "] " + src.format_out())
            if args.statement:
                ii = 0
                for tran in src.expense_trans:
                    print("\t" + tran.format_out())
                    ii += 1
            i += 1
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
parser.add_argument("-g", "--group", help="group sources together", action="store_true")

args = parser.parse_args()

if args.verbose:
    print("verbosity turned on")


file_name = os.path.realpath(args.file_name)
main(file_name)

