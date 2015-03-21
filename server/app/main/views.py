from flask import request
from . import main

@main.route("/")
def hello():
    return 'Server is running'

@main.route("image", methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        return request.data
