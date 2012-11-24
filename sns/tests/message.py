import json

from django.test import Client
from django.utils import unittest
from django.contrib.auth.models import User


class MessageTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.sender = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.receiver = User.objects.create_user('felix', 'felix@thebeatles.com', 'felixpassword')

    def test_posting(self):
        self.client.login(email='lennon@thebeatles.com', password='johnpassword')

        # Empty content
        response = self.client.post('/users/' + str(self.receiver.id) + '/messages/', {'content': '', })
        self.assertEqual(response.content, json.dumps({"status": "error"}))

        # Content too long
        response = self.client.post('/users/' + str(self.receiver.id) + '/messages/', {'content': 'a' * 201})
        self.assertEqual(response.content, json.dumps({"status": "error"}))

        # Valid content
        response = self.client.post('/users/' + str(self.receiver.id) + '/messages/', {'content': 'shiyanchen'})
        self.assertEqual(response.content, json.dumps({"status": "ok"}))
