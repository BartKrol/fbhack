import urllib2
import urllib
import json

class Freebase:
    def __init__(self,tags):
        tags = tags.split(" ")
        self.tags = " ".join(tags[2:])
        self.name = ""
        self.category = ""
        self.description = ""
        self.categories = []

        self.find_categories()

    def find_categories(self):
        response = urllib2.urlopen('https://www.googleapis.com/freebase/v1/search?query='+urllib.quote_plus(self.tags)+"&key=***REMOVED***")
        html = response.read()
        article = json.loads(html)
        result = article["result"][0]
        self.name = result["name"]
        self.category = result["notable"]["name"]

        for result in article["result"]:
            if "notable" in result:
                if result["notable"].has_key("name"):
                    self.categories.append(result["notable"]["name"])

        mid = result["mid"]

        service_url = 'https://www.googleapis.com/freebase/v1/topic'

        params = {
          'key': '***REMOVED***',
          'filter': 'suggest'
        }

        url = service_url + mid + '?' + urllib.urlencode(params)
        topic = json.loads(urllib.urlopen(url).read())
        try:
            self.description = topic["property"]["/common/topic/article"]["values"][0]["property"]["/common/document/text"]["values"][0]["value"]
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
                    "Mountain": "GEO"}
        if self.category in bindings.keys():
            return bindings[self.category]
        else:
            return "BUY"

def check(token):
    base = Freebase(token)
    return base.get_category()