import json

from django.test import Client
from django.utils import unittest
from django.contrib.auth.models import User


class MessageTest(unittest.TestCase):
    def test_message(self):
        User.objects.create_user('john_message', 'john_message@thebeatles.com', 'johnpassword')
        receiver = User.objects.create_user('felix_message', 'felix_message@thebeatles.com', 'felixpassword')

        client = Client()
        client.login(email='john_message@thebeatles.com', password='johnpassword')

        # Empty content
        response = client.post('/users/' + str(receiver.id) + '/messages/', {'content': '', })
        self.assertEqual(response.content, json.dumps({"status": "error"}))

        # Content too long
        response = client.post('/users/' + str(receiver.id) + '/messages/', {'content': 'a' * 201})
        self.assertEqual(response.content, json.dumps({"status": "error"}))

        # Valid content
        response = client.post('/users/' + str(receiver.id) + '/messages/', {'content': 'shiyanchen'})
        self.assertEqual(response.content, json.dumps({"status": "ok"}))

        # User that doesn't exist
        response = client.post('/users/0/messages/', {'content': 'shiyanchen', })
        self.assertEqual(response.status_code, 404)

    def test_message_no_login(self):
        receiver = User.objects.create_user('felix_message2', 'felix_message2@thebeatles.com', 'felixpassword')

        client = Client()
        response = client.post('/users/' + str(receiver.id) + '/messages/', {'content': 'shiyanchen', })
        self.assertEqual(response.status_code, 302)
