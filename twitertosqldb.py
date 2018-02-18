from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import MySQLdb
import time
import json


# #                        server                                         MySQL username	MySQL pass  Database name.
conn = MySQLdb.connect("bruceclark.mysql.pythonanywhere-services.com","bruceclark","@@@@@@@@@@@","bruceclark$default")

c = conn.cursor()


#consumer key, consumer secret, access token, access secret.
ckey="########################"
csecret="##########################################"
atoken="##################-#############################"
asecret="########################################"

class listener(StreamListener):

    def on_data(self, data):

        #print (data)

        #getting data in json
        all_data = json.loads(data)
        
        #separating the column with key = "data"
        tweet = all_data["text"]
        
        username = all_data["user"]["screen_name"]
        
        #inserting in mysql database
        c.execute("INSERT INTO tweeto (time, username, tweet) VALUES (%s,%s,%s)",
            (time.time(), username, tweet))

        #saving it
        conn.commit()

        print((username,tweet))
        
        return True

    def on_error(self, status):
        print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["game of thrones"])