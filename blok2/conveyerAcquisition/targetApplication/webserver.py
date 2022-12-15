from flask import Flask, json

from doa.classifications import Classifications

# get root path
import os
root_path = os.path.dirname(os.path.abspath(__file__))


def run_server():
    api.run()


api = Flask(__name__)


@api.route('/api/classifications', methods=['GET'])
def get_all():
    # create the object
    classifications_object = Classifications()
    # get all the classifications
    classifications = classifications_object.get_all()
    # return the classifications
    return json.dumps(classifications)


@api.route('/', methods=['GET'])
def home():
    try:
        with open(root_path + '/htdocs/index.html') as f:
            return f.read()
    except:
        return handle500()

# catch all and return page in htdocs


@api.route('/<path>', methods=['GET'])
def catch_all(path):
    try:
        with open(root_path + '/htdocs/' + path) as f:
            return f.read()
    except:
        return handle404()


def handle404():
    try:
        with open(root_path + '/htdocs/statuscodes/404.html') as f:
            return f.read(), 404
    except:
        return "404", 404


def handle500():
    try:
        with open(root_path + '/htdocs/statuscodes/500.html') as f:
            return f.read(), 500
    except:
        return "500", 500


if __name__ == '__main__':
    api.run()
