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

output_indent = 0


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

def build_groups(source_dict):
    group = grouper.Grouper()

    for k, v in source_dict.items():
        group.filter_source(v)

    return group

def sum_transactions(source_dict):
    src = source.Source()
    src.name = "TOTAL"

    for k, v in source_dict.items():
        src.income_total += v.income_total
        src.expense_total += v.expense_total
        src.total += v.total

    return src



def tag(i):
    return "[" + str(i) + "]"


def oi_pp():
    global output_indent
    output_indent += 1

def oi_mm():
    global output_indent
    output_indent -= 1

def output(text):
    global output_indent
    print("\t" * output_indent + text)


def output_transactions(trans):
    i = 0
    for t in trans:
        output(tag(i) + " " + t.format_out())
        i += 1

def _do_output_source(i, src, trans):
    output(tag(i) + " " + src.format_out())
    if args.source_transactions:
        oi_pp()
        output_transactions(trans)
        oi_mm()

def output_source_dict(source_dict, total_income, total_expense):
    if total_income > 0:
        i = 0
        output("{Income} " + str(total_income))
        output(line_break)
        for k in sorted(source_dict.keys()):
            src = source_dict[k]
            if src.total > 0:
                _do_output_source(i, src, src.income_trans)
                i += 1
        output("")

    if total_expense > 0:
        i = 0
        output("{Expenses} " + str(total_expense))
        output(line_break)
        for k in sorted(source_dict.keys()):
            src = source_dict[k]
            if src.total < 0:
                _do_output_source(i, src, src.expense_trans)
                i += 1
        output("")

def output_groups(groups):
    output("{Groups}")
    output(line_break)
    i = 0
    for gp in groups.groups:
        src = gp["ssrc"]
        output(tag(i) + " " + src.format_out())
        i += 1

        if args.group_sources:
            oi_pp()
            output_source_dict(gp["source_dict"], src.income_total, src.expense_total)
            oi_mm()

    print("")


def main(file_name):
    statements = build_statement_list(file_name, pattern["statement"])
    transactions = build_transaction_list(statements)
    sources = build_source_dict(transactions)
    groups = build_groups(sources)
    total = sum_transactions(sources)


    ## Header
    print("Results for: " + file_name)
    if args.total:
        print(total.format_out())
    print(line_break)
    print("")

    ## Groups
    if args.group:
        output_groups(groups)

    if args.sources:
        output_source_dict(sources, total.income_total, total.expense_total)

    print("")
    print("")





######################
### main
######################
parser = argparse.ArgumentParser()
parser.add_argument("file_name", type=str)
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-s", "--sources", help="output list of sources", action="store_true")
parser.add_argument("-t", "--total", help="output total", action="store_true")
parser.add_argument("-g", "--group", help="group sources together", action="store_true")


parser.add_argument("-st", "--source_transactions", help="output transactions under sources", action="store_true")
parser.add_argument("-gs", "--group_sources", help="output sources under groups", action="store_true")

args = parser.parse_args()

if args.verbose:
    print("verbosity turned on")


file_name = os.path.realpath(args.file_name)
main(file_name)

