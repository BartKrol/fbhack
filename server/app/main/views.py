from flask import request
from . import main
from app.camfind import *
import json
from app.freebase import Freebase
from app.alchemy_api import AlchemyAPI
from app.category_matcher import *

@main.route("/")
def hello():
    return 'Server is running'


@main.route("image", methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        #image_url = str(request.args.get('url'))
        
        image_url = request.form['url']
        
        token = str(get_image_token(image_url))
        json_data = get_image_response(token)

        freebase = Freebase(json_data['name'])
        
        html = freebase.get_html('london')
        
        response = {'status': 'ok', 'html': html}
        
        return json.dumps(response)
        #return 'HI'

@main.route("entity", methods=['GET', 'POST'])
def entity():
    if request.method == 'GET':
        
        text = str(request.args.get('text'))
        
        alchemy = AlchemyAPI()

        entities = alchemy.entities('text', text, {'sentiment': 0})
        
        #TODO: Think how to do this best
        
        
        
        for entity in entities['entities'][:1]:
            freebase = Freebase(entity['text'])
            html = freebase.get_html('london')

            response = {'status': 'ok', 'html': html}
            return json.dumps(response)
        
        
        return json.dumps({'status': 'error'})
            


        
    