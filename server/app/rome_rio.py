from flask import render_template
import unirest

api_url = 'https://rome2rio12.p.mashape.com/Search'
api_key = "***REMOVED***"


def get_route(from_name, to_name):
    response = unirest.get(api_url + "?currency=GBP&dName=" + to_name + "&oName=" + from_name,
                           headers={
                               "X-Mashape-Key": api_key,
                               "Accept": "application/json"
                           }
    )

    return response.body


def get_rome_rio(from_name, to_name, preview=False):
    route = get_route(from_name, to_name)
    return render_template('route.html', route=route, preview=preview)
