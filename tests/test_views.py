import json

import unittest

import sys
# add app to pp
sys.path.append('../')

from webtest import TestApp

from hook_listener import github


class ServerTests(unittest.TestCase):

    def test_app_index(self):
        app = TestApp(github.app)
        payload = open('tests/payload').read()
        resp = app.post('/', {'payload': payload})
        self.assertEqual("OK", resp.body)

    def test_status_codes(self):
        app = TestApp(github.app)

        # get not allowed
        app.get('/', status=405)

        # post without payload should 500
        app.post('/', status=500)
