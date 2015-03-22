import tweepy
import json
import urllib2
import urllib
from flask import render_template
import unirest

class People:
    def __init__(self, name, description):
        self.name = name
        self.wikipedia = description

        self.facebook_token = "***REMOVED***"
        self.facebook_api = "https://graph.facebook.com/v2.2/"

        self.twitter = {}

        self.facebook = {}

        self.p_twitter()
        self.p_facebook_page()

    def p_wikipedia(self):
        self.p_wikipedia_(self.name)

    def p_wikipedia_(self, link):

        wiki_maps = {"queen elizabeth": "Elizabeth II"}

        if link in wiki_maps:
            link = wiki_maps[link]
        api = "http://en.wikipedia.org/w/api.php?format=json&action=query&titles="+urllib.quote_plus(link)+"&prop=revisions&rvprop=content&continue="
        response = urllib2.urlopen(api)
        html = response.read()
        message = json.loads(html)
        self.wikipedia = message["query"]["pages"]
        print message

        if "normalized" in message["query"]:
            self.p_wikipedia_(message["query"]["normalized"][0]["to"])
        else:
            pass

      #  for key in self.wikipedia.keys():
      #      if "revisions" in self.wikipedia[key]:
      #          if self.wikipedia[key]["revisions"][0]["*"].startswith("#REDIRECT"):
      #              tokens = self.wikipedia[key]["revisions"][0]["*"]
      #              tokens = tokens.split("[[")
      #              tokens = tokens[1].split("]]")
      #              self.p_wikipedia_(tokens[0])

    def p_twitter(self):
        twitter_mappings = {"queen elizabeth": "BritishMonarchy"}

        api_key = "***REMOVED***"
        api_secret = "***REMOVED***"

        a_token = "***REMOVED***"
        a_secret = "***REMOVED***"
        auth = tweepy.OAuthHandler(api_key, api_secret)

        auth.secure = True

        auth.set_access_token(a_token, a_secret)
        api = tweepy.API(auth)

        user = {}

        if twitter_mappings.has_key(self.name):
            user = api.search_users(twitter_mappings[self.name])[0]
        else:
            user = api.search_users(self.name)[0]

        tweets = user.timeline()[:5]

        self.twitter = {"name": user.name, "tweets": tweets, "image": user.profile_image_url_https,
                        "followers": user.followers_count, "sname": user.screen_name}

    def fb_img(self, query):
        return self.facebook_api+query+"&access_token="+self.facebook_token

    def fb_json(self, query):
        token = self.fb_img(query)
        response = urllib2.urlopen(token)
        html = response.read()
        return json.loads(html)

    def p_facebook_page(self):

        fb_mappings = {"queen elizabeth": "TheBritishMonarchy"}

        id = 0
        if self.name in fb_mappings:
            id = fb_mappings[self.name]
        else:
            search = self.fb_json('search?q='+urllib.quote_plus(self.name)+"&type=page")
            id = search['data'][0]["id"]

        page = self.fb_json(id+"?")

        posts = self.fb_json(id+"/posts?")
        #for item in search['data']:
        #    if item['category'] == "Public figure":
        #        print item['id']
        about = ""
        if "about" in page:
            about = page["about"]

        posts = posts["data"][:5]
        new_posts = []
        for post in posts:
            if "message" in post:
                if len(post["message"]) > 150:
                    post["message"] = post["message"][:150] + "..."
                    print post["message"]
            new_posts.append(post)

        self.facebook = {"id": id, "name": page["name"], "about": about, "posts": new_posts, "picture": self.fb_img(id+"/picture?")}

    def get_html(self, preview):
        return render_template('people.html', facebook=self.facebook, twitter=self.twitter, preview=preview, wikipedia=self.wikipedia)
