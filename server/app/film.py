import urllib, urllib2
import json
from flask import render_template

class Film:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def get_info(self):
        api = "http://www.omdbapi.com/?"
        response = urllib2.urlopen(api + "t="+urllib.quote_plus(self.title))
        html = response.read()
        self.data = json.loads(html)

    def get_data(self):
        return self.data

    def get_html(self, preview=False):
        return render_template('film.html', film=self.data)