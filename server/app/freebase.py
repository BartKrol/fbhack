import urllib2
import urllib
import json

import people
import amazon_search
import rome_rio
import film


class Freebase:
    def __init__(self, tags):

        colours = ['black',
                   'blue',
                   'brown',
                   'gray',
                   'green',
                   'orange',
                   'pink',
                   'purple',
                   'red',
                   'white',
                   'yellow',
                   'the',
                   'a']

        tags = tags.lower().split(" ")
        f_tags = []
        for t in tags:
            if t not in colours:
                f_tags.append(t)

        self.tags = " ".join(f_tags[:2])
        self.name = ""
        self.category = ""
        self.description = ""
        self.categories = []

        self.find_categories()

    def find_categories(self):
        url = 'https://www.googleapis.com/freebase/v1/search?query=' + urllib.quote_plus(
            self.tags) + "&key=***REMOVED***"
        response = urllib2.urlopen(url)
        html = response.read()
        article = json.loads(html)
        mid = ""
        for result in article["result"]:
            self.name = result["name"]
            print result
            if "notable" in result:
                if "name" in result:
                    self.category = result["notable"]["name"]
                    mid = result["mid"]
            if self.category != "":
                break

        print self.category

        for result in article["result"]:
            if "notable" in result:
                if result["notable"].has_key("name"):
                    self.categories.append(result["notable"]["name"])

        print self.categories

        service_url = 'https://www.googleapis.com/freebase/v1/topic'

        params = {
            'key': '***REMOVED***',
            'filter': 'suggest'
        }

        url = service_url + mid + '?' + urllib.urlencode(params)
        topic = json.loads(urllib.urlopen(url).read())
        try:
            self.description = \
                topic["property"]["/common/topic/article"]["values"][0]["property"]["/common/document/text"]["values"][
                    0][
                    "value"] + "..."
        except KeyError:
            self.description = ""

    def get_json(self):
        data = {'name': self.name, 'category': self.category, 'description': self.description}
        return json.dump(data)

    def get_category(self):
        return self.category

    def get_categories(self):
        return self.categories

    def get_module(self):
        bindings = {"Dance-pop Artist": "PER",
                    "City/Town/Village": "GEO",
                    "Monarch": "PER",
                    "Noble person": "PER",
                    "Mountain": "GEO",
                    "Actor": "PER",
                    "Hard rock Artist": "PER",
                    "Castle": "GEO"}
        if self.category in bindings.keys():
            return bindings[self.category]
        elif "Film" in self.category:
            return "MOV"
        else:
            return "BUY"

    def get_html(self, position):
        mod = self.get_module()
        if mod == "PER":
            p = people.People(self.tags, self.description)
            return p.get_html(False)
        elif mod == "GEO":
            return rome_rio.get_rome_rio(position, self.tags)
        elif mod == "BUY":
            return amazon_search.get_amazon_items(self.tags, False)
        elif mod == "MOV":
            f = film.Film(self.tags, self.description)
            f.get_info()
            return f.get_html()


def check(token):
    base = Freebase(token)
    return base.get_category()