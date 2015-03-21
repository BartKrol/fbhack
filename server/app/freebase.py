import urllib2
import urllib
import json
import re

class Freebase:
    def __init__(self,tags):
        self.tags = tags
        self.name = ""
        self.category = ""
        self.description = ""

    def get_categories(self):
        response = urllib2.urlopen('https://www.googleapis.com/freebase/v1/search?query='+urllib.quote_plus(self.tags)+"&key=***REMOVED***")
        html = response.read()
        article = json.loads(html)
        result = article["result"][0]
        self.name = result["name"]
        self.category = result["notable"]["name"]
        mid = result["mid"]

        service_url = 'https://www.googleapis.com/freebase/v1/topic'
        params = {
          'key': '***REMOVED***',
          'filter': 'suggest'
        }
        url = service_url + mid + '?' + urllib.urlencode(params)
        topic = json.loads(urllib.urlopen(url).read())
        self.description = topic["property"]["/common/topic/article"]["values"][0]["property"]["/common/document/text"]["values"][0]["value"]


wiki = Freebase("Edinburgh")
wiki.getCategories()
wiki = Freebase("Facebook")
wiki.getCategories()