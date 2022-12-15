from flask import Flask, json, send_file

from dao.classifications import Classifications

# get root path
import os
root_path = os.path.dirname(os.path.abspath(__file__))


def run_server():
    api.run()


api = Flask(__name__)

# 
# API
# 
@api.route('/api/classifications', methods=['GET'])
def get_all():
    # create the object
    classifications_object = Classifications()
    # get all the classifications
    classifications = classifications_object.get_all()
    # return the classifications
    return json.dumps(classifications)

# get latest classification
@api.route('/api/classifications/latest', methods=['GET'])
def get_latest():
    # create the object
    classifications_object = Classifications()
    # get all the classifications
    classification = classifications_object.get_last()
    if classification:
        # return the classification
        return json.dumps(classification)
    else:
        return "[]"
        

# get latest classification image
@api.route('/api/classifications/latest/image', methods=['GET'])
def get_latest_image():
    # create the object
    classifications_object = Classifications()
    # get the last image path
    image = classifications_object.get_last_image()
    # check if the image exists
    if os.path.isfile(image):
        # return the image
        return send_file(image, mimetype='image/jpg'), 200
    else:
        return handle204()
    



# 
# Htdocs
# 
@api.route('/', methods=['GET'])
def home():
    try:
        with open(root_path + '/htdocs/index.html') as f:
            return f.read()
    except:
        return handle500()

@api.route('/<path>', methods=['GET'])
def catchCMD(path):
    try:
        with open(root_path + '/htdocs/' + path) as f:
            return f.read()
    except:
        return handle404()

# catch all and return page in htdocs
@api.route('/<path>/<path2>', methods=['GET'])
def catchPage(path, path2):
    try:
        with open(root_path + '/htdocs/' + path + '/' + path2) as f:
            return f.read()
    except:
        return handle404()



# 
# Exception handlers
# 
def handle204():
    try:
        with open(root_path + '/htdocs/statuscodes/204.html') as f:
            return f.read(), 204
    except:
        return "204", 204

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
    run_server()
