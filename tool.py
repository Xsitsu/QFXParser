#!/usr/bin/python3

import argparse
import re
import os
import json

import logger
import parser
import transaction
import source
import grouper

######################
### declares
######################


######################
### functions
######################
def read_all_text(file_name):
    text = ""
    with open(file_name, "r") as file:
        text = file.read()
    return text

def load_json(file_name):
    text = read_all_text(file_name)
    data = json.loads(text)
    return data

def _filter_trans_name(name, filters):
    for entry in filters:
        for pattern in entry["patterns"]:
            if name.find(pattern) != -1:
                return entry["name"]
    return name

def build_source_dict(transaction_list, filters):
    sources = {}
    for tran in transaction_list:
        use_name = _filter_trans_name(tran.name, filters)
        if use_name not in sources.keys():
            src = source.Source()
            src.name = use_name
            sources[use_name] = src

        sources[use_name].add_transaction(tran)

    return sources

def build_groups(source_dict, group_filters):
    group = grouper.Grouper()
    group.load_mapping(group_filters)

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


def main(file_name_list):
    group_filters = load_json("groupings.json")
    trans_filters = load_json("filters.json")

    par = parser.Parser()
    if args.verbose:
        par.verbose = True

    for fname in file_name_list:
        file_name = os.path.realpath(fname)
        if args.verbose:
            print("Parsing: " + file_name)
        if file_name.find(".qfx") != -1:
            par.parse_qfx(read_all_text(file_name))
        elif file_name.find(".csv") != -1:
            par.parse_venmo(file_name)
        else:
            print("ERROR: bad file [" + file_name + "]")

    sources = build_source_dict(par.transactions, trans_filters)
    groups = build_groups(sources, group_filters)
    total = sum_transactions(sources)

    lg = logger.Logger()
    lg.output_group_sources = args.group_sources
    lg.output_source_transactions = args.source_transactions

    ## Header
    lg.output("Results for: " + file_name)
    if args.total:
        lg.output(total.format_out())
    lg.line_break()
    lg.output("")

    ## Groups
    if args.group:
        lg.output_groups(groups)

    if args.sources:
        lg.output_source_dict(sources, total.income_total, total.expense_total)

    lg.output("")
    lg.output("")




######################
### main
######################
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("file_list", type=str, nargs="+")
arg_parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
arg_parser.add_argument("-s", "--sources", help="output list of sources", action="store_true")
arg_parser.add_argument("-t", "--total", help="output total", action="store_true")
arg_parser.add_argument("-g", "--group", help="group sources together", action="store_true")


arg_parser.add_argument("-st", "--source_transactions", help="output transactions under sources", action="store_true")
arg_parser.add_argument("-gs", "--group_sources", help="output sources under groups", action="store_true")

args = arg_parser.parse_args()

if args.verbose:
    print("verbosity turned on")

main(args.file_list)

