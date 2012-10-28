"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase,Client
from django.utils import unittest
from django.contrib.auth.models import User

class SimpleTest(unittest.TestCase):
	def test_basic_addition(self):
		self.assertEqual(1 + 1, 2)

class MessageTest(unittest.TestCase):
	def setUp(self):
		self.client=Client()
		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
	def test_details(self):
		self.client.login(email='lennon@thebeatles.com',password='johnpassword')
		response=self.client.post('/messages/',{'content':''})
		self.assertEqual(response.content,'{"status": "error"}')
		response=self.client.post('/messages/',{'content':'shiyanchen'})
		self.assertEqual(response.content,'{"status": "ok"}')
		response=self.client.post('/messages/',{'content':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'})
		self.assertEqual(response.content,'{"status": "error"}')
		
