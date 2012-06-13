import os
import argparse
import glob
import re

parser = argparse.ArgumentParser(description='Process commandline options')

parser.add_argument("path", help="the path that you wish to search")

parser.add_argument("-regex", help="using regular expressions",
			action="store_true")

parser.add_argument("-name", help="search for an exact name")

parser.add_argument("-type", help="searching for a specific type of file")

args = parser.parse_args()

for (root, dirs, filenames) in os.walk(args.path):
	for filename in filenames:
		if args.name == filename:
			#if we find the key in the filename
			print os.path.join(root, filename)
	for dirname in dirs:
		if args.name == dirname:
			print os.path.join(root, dirname)
