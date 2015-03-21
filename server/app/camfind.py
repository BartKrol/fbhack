import unirest
from models import Image
from .extensions import db
import urllib
import time
import os
import hashlib
import base64

from urllib import FancyURLopener

api_url_req = "https://camfind.p.mashape.com/image_requests"
api_url_res = "https://camfind.p.mashape.com/image_responses"

api_key = "***REMOVED***"

def save_image_from_base64(base64_encoded_image, filename):
    
    imgdata = base64_encoded_image.decode('base64')
    filename = filename  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)


def get_image_hash(image_url):
    filename = str(int(time.time()))+'.jpg'
    save_image_from_base64(image_url, filename)
    hash = hashlib.md5(open(filename, 'rb').read()).hexdigest()
    #os.remove(filename)
    
    return (hash, filename)
    

def get_image_token(image_url):
    hash, filename = get_image_hash(image_url)
    retrieved_image = Image.query.filter_by(md5=hash).first()
    
    if retrieved_image is None:
        response = unirest.post(api_url_req,
                                headers={
                                    "X-Mashape-Key": api_key

                                },
                                params={
                                    "image_request[language]": "en",
                                    "image_request[locale]": "en_US",
                                    "image_request[image]": open(filename, mode='r')
                                }
        )

        json_response = response.body
        print json_response
        img = Image(hash, json_response['token'], '')
        db.session.add(img)
        db.session.commit()
        os.remove(filename)
        return json_response['token']
    
    else:
        os.remove(filename)
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
    
    if json_response['status'] == 'not completed':
        time.sleep(5)
        return get_image_response(token)
    
    return json_response