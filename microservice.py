from flask import Flask, Response
from botocore.exceptions import ClientError
import os
from flask import make_response
import json
from dynamodb import GreetingHandler


app = Flask(__name__)

service = GreetingHandler('greetings')


def root_dir():
    """ Returns root director for this project """
    return os.path.dirname(os.path.realpath(__file__ + '/..'))


def nice_json(arg):
    response = make_response(json.dumps(arg, sort_keys=True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response


@app.route("/", methods=['GET'])
def hello():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "greetings": "/greetings",
            "add_greeting": "/greetings/<id>/<date>/<content>",
        }
    })


@app.route("/greetings", methods=['GET'])
def greetings():
    data = service.table.scan()['Items']
    for greeting in data:
        greeting['gid'] = float(greeting['gid'])
    return nice_json(data)


@app.route("/addgreeting/<gid>/<date>/<content>", methods=['POST', 'PUT'])
def add_greeting(gid, date, content):
    try:
        service.add_greeting(int(gid), date, content)
        return Response(status=201)
    except ClientError:
        return Response(status=404)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
