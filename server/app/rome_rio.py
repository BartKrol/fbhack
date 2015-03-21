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


def duration_hours(value):
    hours = int(value) / 60
    minutes = int(value) % 60

    ret = ''
    if hours:
        ret += str(hours) + 'h '

    ret += str(minutes) + 'min'

    return ret


def get_rome_rio(from_name, to_name, preview=False):
    routes = get_route(from_name, to_name)['routes']

    routes = sorted(routes, key=lambda route: int(route['duration']))

    routes = routes[0:3]

    for route in routes:
        route['duration'] = duration_hours(int(route['duration']))

    return render_template('route.html', routes=routes, preview=preview, duration_hours=duration_hours)
