import tweepy
import json
import urllib2
import urllib

class People:
    def __init__(self, name):
        self.name = name

        self.facebook_token = "***REMOVED***"
        self.facebook_api = "https://graph.facebook.com/v2.2/"

        self.twitter = {}

        self.facebook = {}

    def twitter(self):

        twitter_mappings = {"Queen Elizabeth": "BritishMonarchy"}

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

        # print user.timeline()[0].text
        # print user.timeline()[1].text
        # print user.timeline()[2].text

        # print user

        self.twitter = {"name": user.name, "tweets": user.timeline()[3:], "image": user.profile_image_url_https,
                        "followers": user.followers_count, "sname": user.screen_name}

    def fb_img(self, query):
        return self.facebook_api+query+"&access_token="+self.facebook_token
    
    def fb_json(self, query):
        token = self.fb_img(query)
        response = urllib2.urlopen(token)
        html = response.read()
        return json.loads(html)

    def facebook_page(self):

        fb_mappings = {"Queen Elizabeth": "TheBritishMonarchy"}

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

        self.facebook = {"id": id, "name": page["name"], "about": about, "posts": posts["data"][:3], "picture": self.fb_img(id+"/picture?")}

    def get_html(self):
        twitter = "<div id=\"twitter\"> " \
                  "<img src=\""+self.twitter["image"]+"\" alt=\"Twitter Account\"> " \
                  "<a href=\"http://twitter.com/"+self.twitter["sname"]+"\">"+self.twitter["name"]+"</a>" \
                  "Followers: "+str(self.twitter["followers"])+"</div>"
        facebook = "<div id=\"facebook\"><img src=\""+self.facebook["picture"]+"\" alt=\"Profile Picture\">" \
                  "<a href=\"http://facebook.com/"+self.facebook["id"]+"\">"+self.facebook["name"]+"</a>" \
                  "</div>"

        return twitter+facebook

p = People("Queen Elizabeth")
p.twitter()
p.facebook_page()
print p.get_html()

p = People("Kylie Minogue")
p.twitter()
p.facebook_page()
print p.get_html()

p = People("Brad Pitt")
p.twitter()
p.facebook_page()
print p.get_html()