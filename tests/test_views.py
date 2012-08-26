import json

import unittest

import sys
# add app to pp
sys.path.append('../')


from hook_listener import github_flask


class ServerTests(unittest.TestCase):

    def setUp(self):
        #self.app = TestApp(github_flask.app)
        self.app = github_flask.app.test_client()

    def test_app_index(self):
        payload = open('tests/django-sqlpaginator.payload').read()
        resp = self.app.post('/hook', data={'payload': payload})
        self.assertEqual("OK", resp.body)

    def test_status_codes(self):
        # get not allowed
        self.app.get('/hook')

        # post without payload should 500
        self.app.post('/hook')

    def test_index(self):
        self.app.get('/')
