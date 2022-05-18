#!/usr/bin/python3

import argparse
import re
import os


######################
### declares
######################
pattern_statement = "\<STMTTRN\>.*?\<\/STMTTRN\>"

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

######################
### main
######################
parser = argparse.ArgumentParser()
parser.add_argument("file_name", type=str)
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

args = parser.parse_args()

if args.verbose:
    print("verbosity turned on")


file_name = os.path.realpath(args.file_name)
statements = build_statement_list(file_name, pattern_statement)
i = 0
for statement in statements:
    print("[" + str(i) + "] : " + statement)
    i += 1

