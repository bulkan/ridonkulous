import logging
#import json
import os
import subprocess
import tempfile

import git

from virtualenv import create_environment


logger = logging.getLogger(__name__)


def get_payload(payload_id):
    ''' get the payload from redis '''

    return {}


def run_tests(payload_id):
    payload = get_payload(payload_id)

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
