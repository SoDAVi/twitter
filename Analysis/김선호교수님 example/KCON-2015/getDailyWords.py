import numpy as np
import pandas as pd
import re
import time

from pandas import Series, DataFrame
from datetime import date, datetime, timedelta

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


pathToFiles = ["D:\\Acads\\Summer2015\\Twitter\\kcon\\data\\extractedTweets\\la_data\\",
               "D:\\Acads\\Summer2015\\Twitter\\kcon\\data\\extractedTweets\\ny_data\\"]

baseFileName = ["tweets_"]

ladataFiles = [ pathToFiles[0] + baseFileName[0] + str(fileNum)
                   for fileNum in range(0,45)]

nydataFiles = [ pathToFiles[1] + baseFileName[0] + str(fileNum)
                   for fileNum in range(1,55)]

tweetFiles = [f for f in ladataFiles+nydataFiles]


mapping = {'kcon':'kcon',               'kconusa':'kcon',       'la':'kconla',               'kconla':'kconla',
           'kconny':'kconny',           'kconnyc':'kconny',     'kpopconcert':'kcon',        'kconlivechat':'kcon',
           'ny':'kconny',
           'kpop':'k-pop',              'kdrama':'k-drama',     'kbeauty':'k-beauty',        'kculture':'k-culture',
           'pop':'k-pop',               'drama':'k-drama',      'beauty':'k-beauty',         'culture':'k-culture',
           'kfood':'k-food',            'food':'k-food',            
           'jinhyuk':'Jin Hyuk',        'hyuk':'Jin Hyuk',
           'jieunpark':'Ji Eun Park',   'eun':'Ji Eun Park',    'sonhojun':'Son Ho Jun',     'jun':'Son Ho Jun',
           'soo-hyun':'Soo Huyn Kim',                           'soohyun':'Soo Huyn Kim',
           'soohyunkim':'Soo Huyn Kim', 'aoa':'AOA',            'monsta':'Monsta X',         'monstax':'Monsta X',               
           'teentop':'Teen Top',        'teen':'Teen Top',
           'vixx':'VIXX',               'sistar':'Sistar',      'ziont':'Zion T',            'zion':'Zion T',
           'kihonglee':'Ki Hong Lee',   'hong':'Ki Hong Lee',   'superjunior':'Super Junior',
           'junior':'Super Junior',     'kyuhyun':'Cho Kyuhyun',
           'redvelvet':'Red Velvet',    'velvet':'Red Velvet',
           'danielhenney':'Daniel Henney',                      'henney':'Daniel Henney',    'yesung':'Yesung',
           'girlsgeneration':'Girls Generation',                'generation':'Girls Generation',
           'snsd':'Girls Generation',
           'got7':'GOT7',               'god7':'GOT7',           'heechul':'Kim Heechul',     'siwon':'Choi Siwon',
           'bambam':'BamBam',           'jackson':'Jackson Wang',                            'exo':'Exo',
           'shinee':'SHINee',           'apink':'Apink',        'kconlive':'kcon',
           'blockb':'Block B',          'block':'Block B',      'shinhwa':'Shinhwa', 'marktuan':'Mark Tuan',
           'wendy':'Wendy', 'ravi':'Ravi', 'yuri':'Kwon Yuri', 'yurikwon':'Kwon Yuri', 'mark':'Mark Tuan', 'tuanmark':'Mark Tuan'}


#words not necessary for wordcloud analysis
USERSIGN = re.compile('@',re.IGNORECASE)
HASHSIGN = re.compile('#')
URL1 = re.compile('https|http',re.IGNORECASE)
URL2 = re.compile(':',re.IGNORECASE)
URL3 = re.compile('\/\/t.co\/[a-z0-9]*',re.IGNORECASE)
RETWEET = re.compile('^(rt)|^(RT)')
MISC = re.compile('\[|\]|\.\.\.')
NON_APLHA = re.compile('[^a-zA-Z7]')
MULTI_SPACE = re.compile('\s{2,10}')
START_SPACE = re.compile('^\s{1,10}')


def removeTags(text):
    """This function replaces URL in the tweets with a space
    """
    try:
        text = re.sub(USERSIGN,' ', text)
        text = re.sub(HASHSIGN,' ', text)
        text = re.sub(URL1,' ', text)
        text = re.sub(URL2,' ', text)
        text = re.sub(URL3,' ', text)
        text = re.sub(MISC,' ', text)
        text = re.sub(RETWEET,' ', text,1)
        text = re.sub(NON_APLHA,' ', text)
        text = re.sub(MULTI_SPACE,' ',text)
        text = re.sub(START_SPACE,'',text)
        return text
    except BaseException as e:
        print("\n***Inside removeTags()")
        print("***ERROR:",str(e))


def get_Word_Freq(listOfFiles, UTCdiff=-7):
    """ This function takes a list of filenames containing
        time of tweet and their keywords, and
        returns frequency of occurance of each word 
    """
    #Data Frame to hold data from all files : master data frame
    tweetsFrame = DataFrame()

    for fileName in listOfFiles:

        #read all data into a pandas DataFrame
        fileDataFrame = pd.read_csv(fileName, sep="\t")

        #list to hold tweet created_at time in datetime format
        dates = []
        
        for d in fileDataFrame['date']:
            #discarding the minutes and seconds portion of time
            #they are not pertinent to current analysis
            dates.append(datetime.strptime(d[:9]+d[-5:], '%b %d %H %Y'))

        #adjusting time for timezone conversion
        dates = [dtObj + timedelta(hours=UTCdiff) for dtObj in dates]

        #adding a column having dates in datetime format
        fileDataFrame['DATETIME'] = [datetime(dtObj.year, dtObj.month, dtObj.day) for dtObj in dates]

        tweetsFrame = pd.concat([tweetsFrame,fileDataFrame])

    #sorting all rows based on datetime
    tweetsFrame.sort(columns='DATETIME', inplace=True)

    #collecting the dates and hours during which tweets were captured
    pdUniqDays = [datetime.utcfromtimestamp((d - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's'))\
                  for d in tweetsFrame['DATETIME'].unique()]

    #resetting the index to count from zero in order
    tweetsFrame.reset_index(drop=True, inplace=True)

    #Series to hold all tweets tweetwed within a particular hour on a particular date
    temp = Series(["" for _ in range(len(pdUniqDays))],index=pdUniqDays)

    
    print('\nStarting aggregation of tweets on date basis...')
    s = time.time()

    #Aggregating tweets for each day
    for idx in range(len(tweetsFrame.DATETIME)):
        cleanText = removeTags(tweetsFrame.tweets[idx])
        noRepeatWordsText = ' '.join(set(cleanText.split()))
        temp[tweetsFrame.DATETIME[idx]] += " " + noRepeatWordsText

    print('\nFinished aggregating tweets in ',(time.time()-s)/60,'minutes')

    #data frame holding word count for each day
    data = {"aggTweets":temp, "wordFreq":[{} for _ in range(len(pdUniqDays))]}
    wordCountStats = DataFrame(data, index=pdUniqDays)

    totalDays = len(wordCountStats.aggTweets)
    daysProcessed = 0

    print('\nStarting Word frequency calculation...')

    for d in pdUniqDays:
        #get a list of individual words in each tweet
        wordList = word_tokenize(wordCountStats.aggTweets[d])

        #remove all stop words from the list
        wordList = [w.lower() for w in wordList if w not in set(stopwords.words('english'))]

        for word in wordList:
            
            #check if the word exists in out mapping words
            if word in mapping.keys():
                mappedWord = mapping[word]
            else:
                mappedWord = word
            
            #check if the mapped word was encountered previously
            if mappedWord in wordCountStats.wordFreq[d].keys():
                wordCountStats.wordFreq[d][mappedWord] += 1
            else:
                wordCountStats.wordFreq[d][mappedWord] = 1

        daysProcessed += 1

        if daysProcessed % 2 == 0:
            print("Processed",daysProcessed,"days of total",totalDays,'days.')

    destFilePath = "D:\\Acads\\Summer2015\\Twitter\\kcon\\wordCountEachDay\\"
    
    for d in pdUniqDays:
        filename = destFilePath+"wordFreqFile_"+d.strftime("%b%d")+".csv" 
        fileHandle = open(filename,"w")

        for k in wordCountStats.wordFreq[d].keys():
            entry = k + ":" + str(wordCountStats.wordFreq[d][k]) + "\n"
            fileHandle.write(entry)

        fileHandle.close()

    print('Completed writing to files')
    return True

        

if __name__ == '__main__':

    start = time.time()

    if get_Word_Freq(tweetFiles):
        print('\nWord frequency calculation finished in ',(time.time()-start)/60,'minutes')