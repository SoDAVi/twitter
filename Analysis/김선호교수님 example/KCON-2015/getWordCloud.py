import numpy as np
import pandas as pd
import re
import time

from pandas import Series, DataFrame

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


pathToFiles = ["D:\\Acads\\Summer2015\\Twitter\\kcon\\data\\extractedTweets\\la_data\\",
               "D:\\Acads\\Summer2015\\Twitter\\kcon\\data\\extractedTweets\\ny_data\\"]

baseFileName = ["tweets_"]

ladataFiles = [ pathToFiles[0] + baseFileName[0] + str(fileNum)
                   for fileNum in range(0,45)]

nydataFiles = [ pathToFiles[1] + baseFileName[0] + str(fileNum)
                   for fileNum in range(1,55)]

#tweetFiles = [f for f in ladataFiles+nydataFiles]

#tweetFiles = [f for f in ladataFiles]


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


def get_Word_Freq(listOfFiles,city="LA"):
    """ This function takes a list of filenames containing
        time of tweet and their keywords, and
        returns frequency of occurance of each word 
    """
    #Data Frame to hold data from all files : master data frame
    tweetsFrame = DataFrame()

    for fileName in listOfFiles:

        #read all data into a pandas DataFrame
        fileDataFrame = pd.read_csv(fileName, sep="\t")

        #concat data for this file with master data frame
        tweetsFrame = pd.concat([tweetsFrame,fileDataFrame])

    #dictionary to hold words and their frreq. of occuremce
    wordFreq = {}

    totalTweets = len(tweetsFrame.tweets)
    tweetsProcessed = 0

    print('\nStarting Word frequency calculation...')

    for tweet in tweetsFrame.tweets:
        #get a list of individual words in each tweet
        wordList = word_tokenize(removeTags(tweet))

        #remove all stop words from the list
        wordList = [w.lower() for w in wordList if w not in set(stopwords.words('english'))]

        wordSet = set(wordList)

        for word in wordSet:
            
            #check if the word exists in out mapping words
            if word in mapping.keys():
                mappedWord = mapping[word]
            else:
                mappedWord = word
            
            #checck if the mapped word was encountered previously
            if mappedWord in wordFreq.keys():
                wordFreq[mappedWord] += 1
            else:
                wordFreq[mappedWord] = 1

        tweetsProcessed += 1

        if tweetsProcessed % 100000 == 0:
            print("Processed",tweetsProcessed,"tweets of total",totalTweets,'tweets.')

    if city == "LA":
      fileHandle = open("LAOnly_wordFreqFile.csv","w")
    else:
      fileHandle = open("NYOnly_wordFreqFile.csv","w")

    for k in wordFreq.keys():
        entry = k + ":" + str(wordFreq[k]) + "\n"
        fileHandle.write(entry)

    fileHandle.close()

    return True

        

if __name__ == '__main__':

    start = time.time()

    if get_Word_Freq(ladataFiles, "LA"):
        print('\nWord frequency calculation finished for LA in ',(time.time()-start)/60,'minutes')

    start = time.time()

    if get_Word_Freq(nydataFiles, "NY"):
        print('\nWord frequency calculation finished for NY in ',(time.time()-start)/60,'minutes')