import logging
#import json
import os
import subprocess
import tempfile

import git

from redis import Redis
from rq import Queue

from virtualenv import create_environment


logger = logging.getLogger(__name__)


redis_conn = Redis()
q = Queue(connection=redis_conn)


def store_payload(payload):
    ''' store payload into redis '''

    job = q.enqueue(run_tests, payload)

    return job.id


def get_payload(payload_id):
    ''' get the payload from redis '''

    return {}


def get_all_jobs(self):
    ''' getall the existing jobs '''

    return q.jobs


def run_tests(payload):
    #payload = get_payload(payload_id)

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
