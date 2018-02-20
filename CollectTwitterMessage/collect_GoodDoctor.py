#!/usr/bin/env python

# Copyright 2007-2016 The Python-Twitter Developers

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ----------------------------------------------------------------------

# This file demonstrates how to track mentions of a specific set of users in
# english language and archive those mentions to a local file. The output
# file will contain one JSON string per line per Tweet.

# To use this example, replace the W/X/Y/Zs with your keys obtained from
# Twitter, or uncomment the lines for getting an environment variable. If you
# are using a virtualenv on Linux, you can set environment variables in the
# ~/VIRTUALENVDIR/bin/activate script.

# If you need assistance with obtaining keys from Twitter, see the instructions
# in doc/getting_started.rst.

import os
import json


from pymongo import MongoClient
from twitter import Api

# Either specify a set of keys here or use os.getenv('CONSUMER_KEY') style
# assignment:

uri = "mongodb://localhost:27017"

CONSUMER_KEY   ="Jh0bgCCfJU5paaHVpU1ynTu38"
CONSUMER_SECRET="5eQjtmbmZBaUDdaSJoSJZSC8pfeDVmu7RUfRZOrx2vPtKfm23a"
ACCESS_TOKEN   ="717459929750044673-CB1tIwhHTee3Zqr9TbSeimj9aYDBOzy"
ACCESS_TOKEN_SECRET  ="8f1syLIt0tqTCg3PgR90b2HBEqjrzyIa6uX7SFGkQkAvj"


# Users to watch for should be a list. This will be joined by Twitter and the
# data returned will be for any tweet mentioning:
# @twitter *OR* @twitterapi *OR* @support.
trackingTags = ["GoodDoctor","Dr. Shaun Murphy","Shaun Murphy", "The Good Doctor",
                "TheGoodDoctor","Freddie Highmore", "David Shore"]

# Languages to filter tweets by is a list. This will be joined by Twitter
# to return data mentioning tweets only in the english language.
# LANGUAGES = ['en']

# Since we're going to be using a streaming endpoint, there is no need to worry
# about rate limits.
api = Api(CONSUMER_KEY,
          CONSUMER_SECRET,
          ACCESS_TOKEN,
          ACCESS_TOKEN_SECRET)

def main():

    numberOfMsg = 0
    tweets = []
    
    client = MongoClient(uri)

    db = client["twitterdb"]["goodDoctor"]
    # api.GetStreamFilter will return a generator that yields one status
    # message (i.e., Tweet) at a time as a JSON dictionary.
    for line in api.GetStreamFilter(track=trackingTags):
        
        tweets.append(line)
        numberOfMsg += 1

        if (numberOfMsg == 100) :
            db.collection.insert_many(tweets)
            tweets = []
            numberOfMsg = 0;

if __name__ == '__main__':
    main()
