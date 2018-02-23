import sys
import json

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

#consumer key, consumer secret, access token, access secret.
CONSUMER_KEY   ="X1vRzw8CHXB8J2oK4chU7Eo89"
CONSUMER_SECRET="nruklsM9kG3GRImjUExnajKlHZ5kdaYH1Q05ZmiTbZiUmFJcei"
ACCESS_TOKEN   ="3194748342-PVnugKAmT88oFGzvqHs9CI1tFw6fUOxPUKmAWQ2"
ACCESS_SECRET  ="rZrCp5Cl3uXKHkX8wg2GlFS8pxJtWcGbWN7LDYw6rUwcY"


filename = ["data//all_tweets"]
trackingTags = ['kcon','kconla','kconusa','kcon15la','kconny','kcon15ny','kpopconcert','kconlivechat','kconnyc',
                'hallyu','korean wave','kpop','k-pop','kdrama','k-drama',
                'k-beauty','kbeauty','k-culture','kculture','k-food','kfood',
                'Jin Hyuk','jinhyuk',
                'Ji Eun Park','jieunpark',
                'Son Ho Jun','sonhojun',
                'Daniel Henney','danielhenney',
                'Soo-Hyun Kim','Soo Huyn Kim','Soohyun Kim','soohyunkim',
                'Teen Top','teentop',
                'VIXX',
                'Girls Generation','girlsgeneration',
                'Zion.T','ziont',
                'Super Junior','superjunior',
                'sistar',
                'Ki Hong Lee','kihonglee',
                'SHINHWA','shinhwa',
                'Red Carpet','redcarpet',
                'GOT7','got7',
                'Roy Kim','roykim',
                'Crush','AOA']

class listener(StreamListener):

    def __init__(self):
        self.fileNumber = 18
        self.tweetCounter = 0

    def on_data(self, data):
        try:
            #capture tweet in json format
            all_data = json.loads(data)

            self.tweetCounter += 1
            self.tweetCounter %= 25000

            if self.tweetCounter == 0:
                self.fileNumber += 1

            f = filename[0] + '_' + str(self.fileNumber)

            """
            for x in range(len(trackingTags)):
                if trackingTags[x].lower() in (all_data['text']).lower():
                   f = filename[x]
                   break
            """
            fHandle = open(f,"a")
            try:
                fHandle.write(str(all_data))
                fHandle.write("\n")
                fHandle.close()
            except:
                fHandle.write(str(all_data).encode('utf-8'))
                fHandle.write("\n")
                fHandle.close()        
        
        except BaseException as e:
            print("\n***Inside on_data")
            print("***ERROR:",str(e)) 

    def on_error(self, status):
        print(status)
        return True # Don't kill the stream

    def on_timeout(self):
        print ('Timeout...\n')
        return True # Don't kill the stream

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

twitterStream = Stream(auth, listener())

twitterStream.filter(track=trackingTags,languages=['en'])
