import os
import subprocess
import json
import logging
import tempfile

import git
import bottle

from bottle import route, run, request, response
from bottle import jinja2_template as template


from virtualenv import create_environment


templates = os.path.join(os.getcwd(), 'hook_listener', 'templates')
bottle.TEMPLATE_PATH.append(templates)

logger = logging.getLogger(__name__)


@route('/', method='GET')
def index():
    return template('index.html', test='testing')


@route('/hook', method='POST')
@route('/hook/', method='POST')
def hook():
    payload = request.POST.get('payload')
    if not payload:
        response.status = "500 no payload found"
        return response

    payload = json.loads(payload)
    print payload

    # work out the repo_url
    repo_name = payload['repository']['name']
    owner = payload['repository']['owner']['name']
    repo_url = "git@github.com:%s/%s.git" % (owner, repo_name)

    logger.info("repo: %s" % repo_url)

    vpath = tempfile.mkdtemp(suffix="ridonkulous")

    logger.debug("cloning into: %s" % vpath)
    print vpath

    create_environment(vpath, site_packages=False)

    os.chdir(vpath)

    logger.info('cloning repo')

    git.Git().clone(repo_url)
    os.chdir(os.path.join(vpath, repo_name))

    pip = "%s/bin/pip" % vpath
    #python = "%s/bin/python"
    nose = "%s/bin/nosetests" % vpath

    ret = subprocess.call(r'%s install -r requirements.txt' % pip, shell=True)

    print "running nose"
    ret = subprocess.call(r'%s' % nose, shell=True)

    print ret

    return 'OK'


app = bottle.default_app()

if __name__ == '__main__':
    run(host='0.0.0.0', port=9080)
