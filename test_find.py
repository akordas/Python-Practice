import find_packaged
import unittest
import os

class testFind(unittest.TestCase):
	"""
	A test class for the module-ified version of find
	"""
	def setUp(self):
		#creates a test directory structure in /tmp
		if not os.path.isdir("/tmp/foodir"):	
			os.mkdir("/tmp/foodir")
		if not os.path.isdir("/tmp/notok"):
			os.mkdir("/tmp/notok")
		if not os.path.exists("/tmp/foodir/foobar_file"):
			self.mk_file("/tmp/foodir/foobar_file")
		if not os.path.exists("/tmp/foodir/not_valid"):		
			self.mk_file("/tmp/foodir/not_valid")
		if not os.path.isdir("/tmp/foodir/nested_dir"):
			os.mkdir("/tmp/foodir/nested_dir")
		if not os.path.exists("/tmp/notok/foobar_file"):
			self.mk_file("/tmp/notok/foobar_file")
		if not os.path.exists("/tmp/foodir/nested_dir/foo"):
			self.mk_file("/tmp/foodir/nested_dir/foo")
		if not os.path.exists("/tmp/foodir/nested_dir/foobar_file"):
			self.mk_file("/tmp/foodir/nested_dir/foobar_file")
		if not os.path.isdir("/tmp/foodir/nested_dir/nested_foodir"):
			os.mkdir("/tmp/foodir/nested_dir/nested_foodir")

	def mk_file(self, name):
		myfile = open(name, 'w')
		myfile.write('')
		myfile.close()

	def test_process_args_exact(self):
		actual_output = find_packaged.process_args(['/tmp/', '-e', 'foo'])
		self.assertEqual(actual_output,"/tmp/foodir/nested_dir/foo\n")

	def tearDown(self):
		#breaks down the test directory structure in /tmp
		if os.path.exists("/tmp/foodir/foobar_file"):
                	os.remove("/tmp/foodir/foobar_file")
                if os.path.exists("/tmp/foodir/not_valid"):
			os.remove("/tmp/foodir/not_valid")
                if os.path.exists("/tmp/notok/foobar_file"):
			os.remove("/tmp/notok/foobar_file")
                if os.path.exists("/tmp/foodir/nested_dir/foo"):
			os.remove("/tmp/foodir/nested_dir/foo")
                if os.path.exists("/tmp/foodir/nested_dir/foobar_file"):
			os.remove("/tmp/foodir/nested_dir/foobar_file")
                if os.path.isdir("/tmp/foodir/nested_dir/nested_foodir"):
			os.rmdir("/tmp/foodir/nested_dir/nested_foodir")
                if os.path.isdir("/tmp/foodir/nested_dir"):
			os.rmdir("/tmp/foodir/nested_dir")
                if os.path.isdir("/tmp/foodir"):
			os.rmdir("/tmp/foodir")
                if os.path.isdir("/tmp/notok"):
			os.rmdir("/tmp/notok")


if __name__ == '__main__':
	unittest.main()
