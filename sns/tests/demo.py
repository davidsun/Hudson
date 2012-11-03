from django.test import TestCase, Client
from django.utils import unittest

class SimpleTest(unittest.TestCase) :
	def test_basic_addition(self) :
		self.assertEqual(1 + 1, 2)
