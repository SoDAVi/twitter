import os
import json
import ast
import sys
from datetime import datetime

from pymongo import MongoClient
from bson import json_util

connectionString = "mongodb://summerys:23N725Me@dsicloud1.usc.edu:27018,dsicloud2.usc.edu:27018,dsicloud3.usc.edu:27018,dsicloud4.usc.edu:27018/twitterdb?readPreference=primaryPreferred"

def main():

    client = MongoClient(connectionString)

    file_path = sys.argv[1]
    database_name = sys.argv[2]
    
    db = client["twitterdb"][database_name]

    tweets_file = open(file_path, 'r')

#    tweets_file = open("/home/summeryseo/data_01_21_27/S.Korea_tweets", 'r')
#    tweets_file = open("/Users/summerseo/Desktop/test", 'r')

    count_inserted = 0
    
    start_datetime = str(datetime.now())
    
    for tweet_line in tweets_file:
        
### Code to get id and then query mongo if id exists to decide not to insert if it does
#        tweet_json = json_util.loads(ast.literal_eval(tweet_line))
#        id = tweet_json['id']
#        print(id)
# db.find(id)
### Check if result exists (already inserted) and don't insert (break instead)
# break

        tweet = ast.literal_eval(tweet_line)
        db.insert_one(tweet)
        count_inserted += 1
    
    end_datetime = str(datetime.now())

    file = open(file_path + '_Results',"w")
    file.write("Done, uploaded " + str(count_inserted) + "\n")
    file.write("Started " + start_datetime + "\n")
    file.write("Ended " + end_datetime + "\n")
    file.close()
    
    print("Done, uploaded " + str(count_inserted) + " for file " + file_path)
if __name__ == '__main__':
    main()
