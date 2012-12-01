import json

from django.test import Client
from django.utils import unittest
from django.contrib.auth.models import User


class PostTest(unittest.TestCase):
    def test_message(self):
        sender = User.objects.create_user('john_post', 'lennon_post@thebeatles.com', 'johnpassword')
        receiver = User.objects.create_user('felix_post', 'felix_post@thebeatles.com', 'felixpassword')

	client = Client()

        client.login(email='lennon_post@thebeatles.com', password='johnpassword')

        # Empty content
        response = client.post('/posts/', {'content': '', })
        self.assertEqual(response.content, json.dumps({"status": "error"}))

        # Content too long
        response = client.post('/posts/', {'content': 'a' * 201})
        self.assertEqual(response.content, json.dumps({"status": "error"}))

        # Valid content
        response = client.post('/posts/', {'content': 'shiyanchen'})
        self.assertEqual(response.content, json.dumps({"status": "ok"}))
	
    def test_message_no_login(self):
        receiver = User.objects.create_user('felix_post2', 'felix_post2@thebeatles.com', 'felixpassword')
    
        client = Client()
	response = client.post('/posts/', {'content': 'shiyanchen', })
	self.assertEqual(response.status_code, 302)
