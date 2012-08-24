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

#bottle.debug(True)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@route('/', method='GET')
def index():
    logger.info('here')
    return template('index.html', test='testing')


@route('/hook', method='POST')
@route('/hook/', method='POST')
def hook():
    payload = request.POST.get('payload')
    if not payload:
        response.status = "500 no payload found"
        return response

    payload = json.loads(payload)
    logger.debug(payload)

    # work out the repo_url
    repo_name = payload['repository']['name']
    owner = payload['repository']['owner']['name']
    repo_url = "git@github.com:%s/%s.git" % (owner, repo_name)

    logger.info("repo: %s" % repo_url)

    vpath = tempfile.mkdtemp(suffix="ridonkulous")

    logger.info("cloning repo %s to: %s" % (repo_url, vpath))

    create_environment(vpath, site_packages=False)

    os.chdir(vpath)

    git.Git().clone(repo_url)
    os.chdir(os.path.join(vpath, repo_name))

    pip = "%s/bin/pip" % vpath
    #python = "%s/bin/python"
    nose = "%s/bin/nosetests" % vpath

    ret = subprocess.call(r'%s install -r requirements.txt --use-mirrors' % pip, shell=True)

    logger.info("running nose")
    ret = subprocess.call(r'%s' % nose, shell=True)
    logger.info(ret)

    return 'OK'


app = bottle.default_app()

if __name__ == '__main__':
    run(host='0.0.0.0', port=9080)
