
from flask import Flask, request, make_response


logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/hook', methods=['POST'])
def hook():
    payload = request.form['payload']
    if not payload:
        response = make_response("no payload found", 500)
        return response

    payload = json.loads(payload)
    logger.debug(payload)


    return 'OK'

if __name__ == "__main__":
    app.run(debug=True)
