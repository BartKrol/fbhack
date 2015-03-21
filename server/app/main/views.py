from flask import request
from . import main
from app.camfind import *

@main.route("/")
def hello():
    return 'Server is running'

@main.route("image", methods=['GET', 'POST'])
def image():
    if request.method == 'GET':
        image_url = str(request.args.get('url'))

        token = str(get_image_token(image_url))
        json = str(get_image_response(token))
        
        return json