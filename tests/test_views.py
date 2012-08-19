import json

import unittest

import sys
# add app to pp
sys.path.append('../')

from webtest import TestApp

from hook_listener import github


class ServerTests(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(github.app)

    def test_app_index(self):
        payload = open('tests/payload').read()
        resp = self.app.post('/hook', {'payload': payload})
        self.assertEqual("OK", resp.body)

    def test_status_codes(self):
        # get not allowed
        self.app.get('/hook', status=405)

        # post without payload should 500
        self.app.post('/hook', status=500)

    def test_index(self):
        self.app.get('/')
