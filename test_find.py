import find_packaged
import unittest
import os

class testFind(unittest.TestCase):
	"""
	A test class for the module-ified version of find
	"""
	def setUp(self):
		#creates a test directory structure in /tmp
		os.mkdir("/tmp/foodir")
		os.mkdir("/tmp/notok")
		mk_file("/tmp/foodir/foobar_file")
		mk_file("/tmp/foodir/not_valid")
		os.mkdir("/tmp/foodir/nested_dir")
		mk_file("/tmp/notok/foobar_file")
		mk_file("/tmp/foodir/nested_dir/foo")
		mk_file("/tmp/foodir/nested_dir/foobar_file")
		os.mkdir("/tmp/foodir/nested_dir/nested_foodir")

	def mk_file(name):
		myfile = open(name, 'w')
		myfile.write('')
		myfile.close()

	def tearDown(self):
		#breaks down the test directory structure in /tmp
		os.removedirs("/tmp/foodir")
		os.removedirs("/tmp/notok")

if __name__ == '__main__':
	unittest.main()
