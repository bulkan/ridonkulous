import json

import bottle

from bottle import route, run, request, response


@route('/', method='POST')
def index():
    payload = request.POST.get('payload')
    if not payload:
        response.status = "500 no payload found"
        return response

    payload = json.loads(payload)

    # work out the repo_url
    repo_name = payload['repository']['name']
    owner = payload['repository']['owner']['name']
    repo_url = "git@github.com:%s/%s.git" % (owner, repo_name)


    return 'OK'


app = bottle.default_app()

if __name__ == '__main__':
    run()
