import find_packaged
import unittest
import os
import sys
import re

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
		if not os.path.exists("/tmp/foodir/gray"):
			self.mk_file("/tmp/foodir/gray")
		if not os.path.exists("/tmp/foodir/grey"):
			self.mk_file("/tmp/foodir/grey")
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
		"""
		tests that an exact name search works all the way through
		"""
		actual_output = find_packaged.process_args(['/tmp/', '-e', 'foo'])
		self.assertEqual(actual_output.getvalue(),"/tmp/foodir/nested_dir/foo\n")
		actual_output.close()

	def test_exact_type(self):
		"""
		test an exact name search with filetype included
		"""
		actual_output = find_packaged.process_args(['/tmp/', '-e', 'gray', '-t', 'f'])
		expected_output = "/tmp/foodir/gray\n"
		self.assertEqual(actual_output.getvalue(), expected_output)

	def test_process_args_glob(self):
		"""
		tests that a fnmatched name search works all the way through
		"""
		actual_output = find_packaged.process_args(['/tmp','-n','n?t_valid'])
		expected_value = "/tmp/foodir/not_valid\n"
		self.assertEqual(actual_output.getvalue(), expected_value)
		actual_output.close()

	def test_glob_type(self):
		"""
		test that filetype matching works with fnmatching
		"""
		actual_output = find_packaged.process_args(['/tmp/', '-n', '*foo*', '-t', 'd'])
		expected_value = "/tmp/foodir\n/tmp/foodir/nested_dir/nested_foodir\n"
		self.assertEqual(actual_output.getvalue(), expected_value)
		actual_output.close()

	def test_process_args_regex(self):
		"""
		tests that a regexed name search works all the way through
		"""
		actual_output = find_packaged.process_args(['/tmp', '-r', 'notok'])
		expected_value = "/tmp/notok\n"
		self.assertEqual(actual_output.getvalue(), expected_value)
		actual_output.close()

	def test_regex_filetype(self):
		"""
		tests that regex works with filetype matching
		"""
		actual_output = find_packaged.process_args(['/tmp/', '-r', 'notok', '-t', 'd'])
		expected_output = "/tmp/notok\n"
		self.assertEqual(actual_output.getvalue(), expected_output)
		actual_output.close()

	def test_bad_arg(self):
		"""
		tests that a bad arg throws some sort of exception
		it's an inelegant solution, but it works.
		"""
		try:
			actual_output = find_packaged.process_args(['/tmp/', '-e', 'foodir', '-stirfry'])
			assert False
		except:
			assert True

	def test_bad_path_given(self):
		"""
		tests that a bad path reverts to the current working directory
		"""
		actual_output = find_packaged.process_args(['/some/path/doesnt/exist/', '-e', 'stirfry'])
		self.assertEqual(actual_output.getvalue(), "")
		actual_output.close()

	def test_no_args_given(self):
		"""
		tests that an error is raised when no args are provided
		"""
		try:
			out = find_packaged.process_args([])
			assert False
		except:
			assert True

	def test_multiple_exclusive_options(self):
		"""
		tests that user can't provide multiple search types
		"""
		try:
			out = find_packaged.process_args(['/tmp/', '-e', 'foo', '-n', 'f?o'])
			assert False
		except:
			assert True

	def test_only_path_given(self):
		"""
		tests that one search type must be provided
		"""
		try:
			out = find_packaged.process_args(['/tmp'])
			assert False
		except:
			assert True

	def tearDown(self):
		#breaks down the test directory structure in /tmp
		if os.path.exists("/tmp/foodir/gray"):
			os.remove("/tmp/foodir/gray")
		if os.path.exists("/tmp/foodir/grey"):
			os.remove("/tmp/foodir/grey")
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
