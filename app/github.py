import json

from bottle import route, run, request, response

import bottle


@route('/', method='POST')
def index():
    payload = request.POST.get('payload')
    if not payload:
        response.status = "500 no payload found"
        return response

    payload = json.loads(payload)

    return 'OK'


app = bottle.default_app()

if __name__ == '__main__':
    run()
