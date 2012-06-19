from os import walk, getcwd
from os.path import relpath, join, exists, isdir
from re import compile, match
from fnmatch import filter, fnmatch
import anydbm
import sys
import argparse
import cStringIO

def process_args(argslist):

	parser = argparse.ArgumentParser(description='Process commandline options',
				argument_default = argparse.SUPPRESS)

	parser.add_argument("path", help="the path that you wish to search")

	group = parser.add_mutually_exclusive_group(required=True)

	group.add_argument("-r", "-regex", help="using regular expressions")

	group.add_argument("-n", "-name", help="search for an fnmatching  name")

	parser.add_argument("-t", "-type", help="limit search to dirs or files",
                type=str)

	group.add_argument("-e", "-exact", help="search for the exact file/dirname")

	args = parser.parse_args(argslist)
	result = ""

	if not isdir(args.path):
		print "no search path provided, using cwd"
		path = getcwd()

	if hasattr(args, 'n'):
		#run the recursive globbing code
		if hasattr(args, 't'):
			result = fnmatch_it(args.path, args.n, args.t)
		else:
			result = fnmatch_it(args.path, args.n, None)
	elif hasattr(args, 'e'):
		#run the exact match code
		if hasattr(args, 't'):
			result = exact_it(args.path, args.e, args.t)
		else:
			result = exact_it(args.path, args.e, None)
	else:
		if hasattr(args, 't'):
			result = regex_it(args.path, args.r, args.t)
		else:
			result = regex_it(args.path, args.r, None)

	return result

def fnmatch_it(path, name, typ):
        ###this is the code for recursive globbing
	output = cStringIO.StringIO()
        for root, dirs, files in walk(path):
                for filename in files:
                        if fnmatch(filename, name):
                                if not typ:
                                        output.write(join(root,filename)+'\n')
                                else:
                                        if typ == 'f':
                                                output.write(join(root, filename)+'\n')
                for dirname in dirs:
                        if fnmatch(dirname, name):
                                if not typ:
                                        output.write(join(root, dirname)+'\n')
                                else:
                                        if typ == 'd':
                                                output.write(join(root, dirname)+'\n')
	return output

def exact_it(path, exact, typ):
        ###this is the code for searching for the exact filename
	output = cStringIO.StringIO()
        for (root, dirs, filenames) in walk(path):
                if exists(join(root, "fsys.idx")):
                        index = anydbm.open(join(root, "fsys.idx"), 'r')
                        try:
                                if  index[exact]:
                                        if not typ:
                                                output.write(join(root, exact)+'\n')
                                        elif typ == 'd' and index[exact]=='d':
                                                output.write(join(root, exact)+'\n')
                                        elif typ == 'f' and index[exact]=='f':
                                                output.write(join(root, exact)+'\n')
                        except:
                                pass
                        index.close()
                else:
                        for filename in filenames:
                                if exact == filename:
                                        #if we find the key in the filename
                                        if not typ:
                                                output.write(join(root, filename)+'\n')
                                        else:
                                                if typ == 'f':
                                                        output.write(join(root, filename)+'\n')
                        for dirname in dirs:
                                if exact == dirname:
                                        if not typ:
                                                output.write(join(root, dirname)+'\n')
                                        else:
                                                if typ == 'd':
                                                        output.write(join(root, dirname)+'\n')
	return output

def regex_it(path, exp, typ):
	output = cStringIO.StringIO()
        try:
		pattern = compile(exp)
	except:
		sys.exit("sorry, that regex was illegal")
        for (root, dirs, filenames) in walk(path):
                for filename in filenames:
                        if match(pattern, filename):
                                if not typ:
                                        output.write(join(root, filename)+'\n')
                                else:
                                        if typ == 'f':
                                                output.write(join(root, filename)+'\n')
                for dirname in dirs:
                        if match(pattern, dirname):
                                if not typ:
                                        output.write(join(root, dirname)+'\n')
                                else:
                                        if typ == 'd':
                                                output.write(join(root, dirname)+'\n')
	return output

if __name__ == '__main__':
	process_args()
