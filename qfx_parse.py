#!/usr/bin/python3

import argparse
import re
import os







parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

args = parser.parse_args()

if args.verbose:
    print("verbosity turned on")
