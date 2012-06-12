import os
import argparse
import glob
import re

parser = argparse.ArgumentParser(description='Process commandline options')

parser.add_argument("path", help="the path that you wish to search")

parser.add_argument("name", help="the term that you're searching for")

parser.add_argument("-regex")

parser.add_argument("-name")

parser.add_argument("-type")

args = parser.parse_args()

##print args.path, '\n' ##dummy line- show what directory we're starting the search from

##print os.listdir(args.path)  ##dummy line- show what files are in the directory

for filename in os.listdir(args.path):
	if args.name in filename:
		print os.path.abspath(filename)
