import os
import json

import bottle

from bottle import route, run, request, response
from bottle import jinja2_template as template


templates = os.path.join(os.getcwd(), 'hook_listener', 'templates')

bottle.TEMPLATE_PATH.append(templates)


@route('/', method='GET')
def index():
    return template('index.html', test='testing')


@route('/hook', method='POST')
def hook():
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
