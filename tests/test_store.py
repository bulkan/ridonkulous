import requests
import json

import sys

# add app to pp
sys.path.append('../')


from redis import Redis
from rq import Queue
from rq.job import Job


def test_hook():
    redis_conn = Redis()
    myq = Queue(connection=redis_conn)

    payload = open('tests/ridonkulous-example.payload').read()
    response = requests.post('http://localhost:5000/hook', data={'payload': payload})
    jobid = response.content
    job = Job.fetch(jobid, connection=redis_conn)
    done = False
    while not done:
        job.refresh()
        if hasattr(job, 'progress'):
            print json.loads(job.progress)
            job.progress = ''
            job.save()
        done = job.is_finished
