import unirest
from models import Image
from .extensions import db
import urllib
import time
import os
import hashlib

api_url_req = "https://camfind.p.mashape.com/image_requests"
api_url_res = "https://camfind.p.mashape.com/image_responses"

api_key = "***REMOVED***"


def get_image_hash(image_url):
    filename = str(int(time.time()))+'.jpg'
    urllib.urlretrieve(image_url, filename)
    hash = hashlib.md5(open(filename, 'rb').read()).hexdigest()
    os.remove(filename)
    
    return hash
    

def get_image_token(image_url):
    hash = get_image_hash(image_url)
    retrieved_image = Image.query.filter_by(md5=hash).first()
    
    if retrieved_image is None:
        response = unirest.post(api_url_req,
                                headers={
                                    "X-Mashape-Key": api_key,
                                    "Content-Type": "application/x-www-form-urlencoded",
                                    "Accept": "application/json"
                                },
                                params={
                                    "image_request[language]": "en",
                                    "image_request[locale]": "en_US",
                                    "image_request[remote_image_url]": image_url
                                }
        )

        json_response = response.body

        img = Image(hash, json_response['token'], '')
        db.session.add(img)
        db.session.commit()

        return json_response['token']
    
    else:
        return retrieved_image.token


def get_image_response(token):
    response = unirest.get(api_url_res+"/"+token,
                           headers={
                               "X-Mashape-Key": api_key,
                               "Accept": "application/json"
                           }
    )

    json_response = response.body
    
    
    #{status: '', reason: '', name:''}
    #we are instereted in name
    
    return json_response