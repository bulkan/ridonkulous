import requests
import json

import sys
# add app to pp
sys.path.append('../')


def test_hook():
    payload = open('tests/ridonkulous-example.payload').read()
    response = requests.post('http://localhost:5000', data={'payload': payload})
    import pdb; pdb.set_trace()
    print response
