import json
import logging

from flask import Flask, request, make_response, render_template

from tasks import store_payload


app = Flask(__name__)

logger = logging.getLogger(__name__)


@app.route("/")
def previous_jobs():
    return render_template("previous_runs.html")


@app.route("/job")
def running_job():
    return "OK"


@app.route('/hook', methods=['POST', 'GET'])
def hook():
    payload = request.form['payload']
    if not payload:
        response = make_response("no payload found", 500)
        return response

    payload = json.loads(payload)
    logger.debug(payload)

    jobid = store_payload(payload)

    return jobid

if __name__ == "__main__":
    app.run(debug=True)
