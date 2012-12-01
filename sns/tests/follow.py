import json

from django.test import TestCase, Client
from django.utils import unittest
from django.contrib.auth.models import User


class FollowTest(unittest.TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user('john_follow', 'lennon_follow@thebeatles.com', 'johnpassword')
		self.newUser = User.objects.create_user('john_follow2', 'lennon_follow2@thebeatles.com', 'johnpassword')

	def test_following(self) :
		self.client.login(email='lennon_follow@thebeatles.com', password='johnpassword')

        # followee's id is the same as the follower's
		response = self.client.post('/users/' + str(self.user.id)+ '/follow/')
		self.assertEqual(response.content, json.dumps({"status": "error"}))
        
        # followee's id is different from the follower's
	        response = self.client.post('/users/'+str(self.newUser.id)+'/follow/')
		self.assertEqual(response.content, json.dumps({"status": "ok"}))

		
