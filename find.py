from os import walk
from os.path import relpath, join, exists
from argparse import ArgumentParser
from re import compile, match
from sys import exit
from fnmatch import filter, fnmatch
import anydbm

parser = ArgumentParser(description='Process commandline options')

parser.add_argument("path", help="the path that you wish to search")

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("-r", "-regex", help="using regular expressions")

group.add_argument("-n", "-name", help="search for an fnmatching  name")

parser.add_argument("-t", "-type", help="limit search to dirs or files",
			type=str)

group.add_argument("-e", "-exact", help="search for the exact file/dirname")

args = parser.parse_args()

if args.n:
	###this is the code for recursive globbing
	for root, dirs, files in walk(args.path):
		for filename in files:
			if fnmatch(filename, args.n):
				if not args.t:
					print join(root,filename)
				else:
					if args.t == 'f':
						print join(root, filename)
		for dirname in dirs:
			if fnmatch(dirname, args.n):
				if not args.t:
					print join(root, dirname)
				else:
					if args.t == 'd':
						print join(root, dirname)

if args.e:
	###this is the code for searching for the exact filename
	for (root, dirs, filenames) in walk(args.path):
		if exists(join(root, "fsys.idx")):
			index = anydbm.open(join(root, "fsys.idx"), 'r')
			try:
				if  index[args.e]:
					if not args.t:
						print join(root, args.e)
					elif args.t == 'd' and index[args.e]=='d':
						print join(root, args.e)
					elif args.t == 'f' and index[args.e]=='f':
						print join(root, args.e)
			except:
				pass
			index.close()
		else:
			for filename in filenames:
				if args.n == filename:
					#if we find the key in the filename
					if not args.t:
						print join(root, filename)
					else:
						if args.t == 'f':
							print join(root, filename)
			for dirname in dirs:
				if args.n == dirname:
					if not args.t:
						print join(root, dirname)
					else:
						if args.t == 'd':
							print join(root, dirname)

if args.r:
	pattern = compile(args.r)
	for (root, dirs, filenames) in walk(args.path):
		for filename in filenames:
			if match(pattern, filename):
				if not args.t:
					print join(root, filename)
				else:
					if args.t == 'f':
						print join(root, filename)
		for dirname in dirs:
			if match(pattern, dirname):
				if not args.t:
					print join(root, dirname)
				else:
					if args.t == 'd':
						print join(root, dirname)
