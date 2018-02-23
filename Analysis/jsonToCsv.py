import nltk
import ast
from datetime import datetime
import tzlocal
import json
import sys
import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
csv.field_size_limit(sys.maxsize)

neg = 0;
pos = 0;
neu = 0;
compound = 0;

with open("ResultCSV.csv", 'w') as f1: #output file
    with open("/data/olympic_tweets_1", 'r+') as f: #input file
        
        #Adding Header
        headers = ["Text", "Positive", "Negative", "Neutral", "Compound", "Username", "Time Zone",
                   "Timestamp", "Time", "Year", "Month", "Day", "Hour", "Minute"]
        mywriter = csv.DictWriter(f1, fieldnames=headers)
        mywriter.writeheader()

        for line in f:
#            print(line)
            try:
                #Parsing json data
                data = ast.literal_eval(line)

#                data = json.loads(line)
                # data = json.JSONDecoder(line)

                if data['text']: #if 'text' exists
             
                    # change to lowercase
                    s = (data['text'].lower().encode('utf-8').strip())
                
                    ss = s.replace(",", " ").replace("\n"," ").replace("\r", " ").replace("\u", " ")
                   
                    #keywords
                    a = ['the good doctor', 'thegooddoctor', 'gooddoctor', 'david shore', 'freddie highmore', 'shaun murphy']
                    if any(x in ss for x in a): # if the tweets includes any of the above keywords
                        ss_pos = analyzer.polarity_scores(ss)['pos']
                        ss_neg = analyzer.polarity_scores(ss)['neg']
                        ss_neu = analyzer.polarity_scores(ss)['neu']
                        ss_com = analyzer.polarity_scores(ss)['compound']
                        local_timezone = tzlocal.get_localzone()
                        local_time = datetime.fromtimestamp(float(data['timestamp_ms']) / 1000, local_timezone) # change to local timezone
#                        print(ss + "," + str(data['user']['time_zone']) + "," + str(local_time.strftime("%d")) + "," +
#                              str(data['id']) + "\n")
                        f1.write(ss + "," + str(float(ss_pos)) + "," + str(float(ss_neg)) + "," + str(float(ss_neu)) +
                                 "," + str(float(ss_com)) + "," + str(data['user']['screen_name']) + "," +
                                 str(data['user']['time_zone']) + "," + str(data['timestamp_ms']) + "," +
                                 str(local_time.strftime("%Y-%m-%d %H:%M:%S")) + "," + str(local_time.strftime("%Y")) +
                                 "," + str(local_time.strftime("%m")) + "," + str(local_time.strftime("%d")) + "," +
                                 str(local_time.strftime("%H")) + "," + str(local_time.strftime("%M")) + "\n")
            except:
                print ("-_-ERROR-----------------------------------------") #error
