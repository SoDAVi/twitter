import numpy as np
import pandas as pd
from pandas import Series,DataFrame

import ast
import re

#function to remove URL, hasgtag and usernames and non-alphabets
def removeTags(text):
    """
    This function finds URLs, Hashtags, Username and non-aplhabets
    in the text passed and replaces them with empty string
    """

    USERNAME = re.compile('@[A-Za-z0-9]+',re.IGNORECASE)
    HASHTAG = re.compile('#[A-Za-z0-9]+',re.IGNORECASE)
    HASHSIGN = re.compile('#')
    URL = re.compile('(((https?|ftp|file)(:)(\/\/)?)|(www.))[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]',re.IGNORECASE)
    RETWEET = re.compile('^(rt)|^(RT)')
    NON_APLHA = re.compile('[^a-zA-Z]')
    MULTI_SPACE = re.compile('\s{2,10}')
    START_SPACE = re.compile('^\s{1,10}')

    try:
        #text = re.sub(USERNAME,' ', text)
        #text = re.sub(HASHSIGN,' ', text)
        #text = re.sub(URL,' ', text)
        #text = re.sub(RETWEET,' ', text,1)
        #text = re.sub(NON_APLHA,' ', text)
        text = re.sub(MULTI_SPACE,' ',text)
        text = re.sub(START_SPACE,'',text)
        return text
    except BaseException as e:
        print("\n***Inside removeTags()")
        print("***ERROR:",str(e))


#function to extract tweets from files containing all tweets
def extractTweets(srcFiles, destFiles):
    """
    This function reads each file mentioned in the list srcFiles
    Extracts tweet text from each file
    Writes the tweet text to corresponding destination file mentioned in list destFiles
    """

    rawfiles = Series(srcFiles)

    tweetFiles = Series(destFiles)

    #file to hold tweet count
    counterHandle = open('tweetCounterFile.csv','w')

    for idx, filename in rawfiles.iteritems():

        print('Processing file', filename)

        #counter to count total tweets
        counter = 0
        
        fileHandle = open(filename,'r')
        tweetHandle = open(tweetFiles[idx],'a')

        tweetHandle.write('date\ttweets\n')

        lines = fileHandle.readlines()

        for line in lines:
            counter += 1
            lineDict = ast.literal_eval(line)

            try:
                #tweetHandle.write(lineDict['created_at']+'\t'+removeTags(lineDict['text']))
                tweetHandle.write(lineDict['created_at'][4:-14]+" "+lineDict['created_at'][-4:]+'\t'+removeTags(lineDict['text'])
                tweetHandle.write('\n')
            except BaseException as e:
                print("Error : while extracting tweet:",str(e))
                continue

        fileHandle.close()
        tweetHandle.close()
        counterHandle.write(filename+'\t'+str(counter))

    counterHandle.close()
    return True

if __name__ == "__main__":

    dataFiles = ["data\\all_tweets_0","data\\all_tweets_01"]

    tweetFiles = ["data\\tweet_freq_0","data\\tweet_freq_01"]

    if extractTweets(dataFiles, tweetFiles):
        print('\nTweets extraction completed')