import unittest
import json
import random
import string
import os

from unittest.case import SkipTest
import twython

from sneakers.channels import twitter
import sneakers
basePath = os.path.dirname(os.path.abspath(sneakers.__file__))

class TwitterTest(unittest.TestCase):

    def setUp(self):

        configPath = os.path.join(basePath, 'config', 'twitter-config.json')
        try:
            with open(configPath, 'rb') as f:
                s = json.loads(f.read())
        except:
            raise SkipTest("Could not access Twitter configuration file.")

        self.params = s['twitter']

        self.client = twython.Twython(
            self.params['key'],
            self.params['secret'],
            self.params['token'],
            self.params['tsecret'])

        self.randText = ''.join([random.choice(string.letters) for i in range(10)])

        self.channel = twitter.Twitter()
        self.channel.params['sending'] = self.params
        self.channel.params['receiving'] = self.params

    def test_send(self):
        self.channel.send(self.randText)

        resp = self.client.get_user_timeline(screen_name=self.params['name'])
        if 'text' in resp[0]:
            self.assertEqual(resp[0]['text'], self.randText)

    def test_receive(self):
        self.client.update_status(status=self.randText)

        tweets = self.channel.receive()
        self.assertEqual(tweets[0], self.randText)