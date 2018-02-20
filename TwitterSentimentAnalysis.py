#Python NLTK sentiment analysis

import nltk
import json
import sys
import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
csv.field_size_limit(sys.maxsize)

file_path = sys.argv[1]

total_sentiment_pos = 0
total_sentiment_neg = 0
total_sentiment_neu = 0
total_sentiment_compound = 0

#keywords = ['the good doctor', 'thegooddoctor', 'gooddoctor', 'david shore', 'freddie highmore', 'shaun murphy']

with open(file_path) as file:
	for tweet in file:
		if tweet['text']: #if 'text' column exists
		             
		    # change to lowercase
		    textToLowerCase = (data['text'].lower().encode('utf-8').strip())
		    formattedString = textToLowerCase.replace(",", " ").replace("\n"," ").replace("\r", " ").replace("\u", " ")
		       
		        if any(key in formattedString for key in keywords): # if the tweets includes any of the above keywords
		            total_sentiment_pos += analyzer.polarity_scores(formattedString)['pos']
		            total_sentiment_neg = analyzer.polarity_scores(formattedString)['neg']
		            total_sentiment_neu = analyzer.polarity_scores(formattedString)['neu']
		            total_sentiment_compound = analyzer.polarity_scores(formattedString)['compound']



                