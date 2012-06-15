import anydbm
from argparse import ArgumentParser
from os import walk
from os.path import relpath, join

parser = ArgumentParser(description= 'get necessary root of sys to be indexed')

parser.add_argument("path", help = "the path to what you want indexed")

args = parser.parse_args()

for root, dirs, files in walk(args.path):
	index = anydbm.open(join(root, "fsys.idx"), 'n')
	for filename in files:
		index[filename]='f'
	for dirname in dirs:
		index[dirname]='d'
	index.close()
