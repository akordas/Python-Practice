from os import walk
from os.path import relpath, join
from argparse import ArgumentParser
from glob import glob
from re import compile, match
from sys import exit
from fnmatch import filter, fnmatch

parser = ArgumentParser(description='Process commandline options')

parser.add_argument("path", help="the path that you wish to search")

parser.add_argument("-regex", help="using regular expressions")

parser.add_argument("-name", help="search for an exact name")

parser.add_argument("-type", help="searching for a specific type of file")

args = parser.parse_args()

if args.name and args.regex:
	print "Please pass in only a globbed name or a regex expression"
	exit()

if not args.name and not args.regex:
	print "Please provide either a globbed name or a regex expression"
	exit()

if args.name:
	"""	
	###this chunk of code works for the directory that args.path points to
	wheretolook = args.path + relpath(args.name)
	for blah in glob(wheretolook):
		print blah
	"""
	###this is the code (in development) for recursive globbing
	for root, dirs, files in walk(args.path):
		for filename in files:
			if fnmatch(filename, args.name):
				print join(root,filename)
		for dirname in dirs:
			if fnmatch(dirname, args.name):
				print join(root, dirname)

	"""	
	###this is the code for searching for the exact filename
	for (root, dirs, filenames) in walk(args.path):
		for filename in filenames:
			if args.name == filename:
				#if we find the key in the filename
				print join(root, filename)
		for dirname in dirs:
			if args.name == dirname:
				print join(root, dirname)
	"""

if args.regex:
	pattern = compile(args.regex)
	for (root, dirs, filenames) in walk(args.path):
		for filename in filenames:
			if match(pattern, filename):
				print join(root, filename)
		for dirname in dirs:
			if match(pattern, dirname):
				print join(root, dirname)
