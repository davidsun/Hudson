import json

from django.test import TestCase, Client
from django.utils import unittest
from django.contrib.auth.models import User

class MessageTest(unittest.TestCase):
	def setUp(self):
		self.client = Client()
		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

	def test_posting(self) :
		self.client.login(email='lennon@thebeatles.com', password='johnpassword')

        # Empty content
		response = self.client.post('/messages/', {'content': ''})
		self.assertEqual(response.content, json.dumps({"status": "error"}))
        
        # Content too long
		response=self.client.post('/messages/', {'content': 'a' * 201})
		self.assertEqual(response.content, json.dumps({"status": "error"}))

        # Valid content
		response = self.client.post('/messages/', {'content': 'shiyanchen'})
		self.assertEqual(response.content, json.dumps({"status": "ok"}))
		
