#!/usr/bin/python
import os.path
from collections import Counter
import nltk
import ast
from datetime import datetime
import tzlocal
import pandas as pd
import csv
import sys
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def main():

	filePath = sys.argv[1] # Takes filePath(Initial CSV) as an argument
	header = sys.argv[2] # header of the text file 
    
	def divideCSV_original_retweet(): # Takes in original CSV file and seperate into two files. (Retweet and NonRetweet)

		containRetweet = csvFile[csvFile["Text"].str.contains("rt @")]
		notContainRetweet = csvFile[csvFile["Text"].str.contains("rt @")==False] 

		reTweetCSVPath = final_directory + "/reTweet.csv" 
		originalTweetCSVPath = final_directory + "/originalTweet.csv"
		containRetweet.to_csv( reTweetCSVPath, index = True, encoding='utf-8')
		notContainRetweet.to_csv( originalTweetCSVPath, index = True, encoding='utf-8')

	def numTweets(): #Counting number of twitter messages that contain keywords

		#keywords to search
		keywords = []
		total_containKeywords = 0

		keyword_input = "" 
		while keyword_input != "exit":
			
			keyword_input = raw_input("please type keywords. Type \"exit\" when finished: \n" )
			if keyword_input != "exit": 
				keywords.append(keyword_input)
			
		for keyword in keywords:

			containKeywords = originalTweetFile[originalTweetFile["Text"].str.contains(keyword)]
			outFile.write( "total number of tweets that contain keyword ["+ keyword + "]: " + str(len(containKeywords)) + "\n\n" )
			total_containKeywords += len(containKeywords)

		outFile.write( "total number of tweets that contain all keywords: " +  str(total_containKeywords) + "\n\n" )

	def numReTweets(): # Counting Number of Retweets 

		containRetweet = csvFile[csvFile["Text"].str.contains("rt")]
		outFile.write("total number of retweet: " + str(len(containRetweet)) + "\n\n" )
	
	def originalTweetsSentiment(): # Sentiment values for non-retweeted messages

		outFile.write("[Nonretweeted Tweets]\nPositive: " + str(originalTweetFile["Positive"].mean()) + "\n" +
		       "Negative: " + str(originalTweetFile["Negative"].mean()) + "\n" +
		       "Neutral: " + str(originalTweetFile["Neutral"].mean()) + "\n" +
		       "Compound: " + str(originalTweetFile["Compound"].mean()) + "\n\n" )
	
	def retweetSentiment(): # Sentiment values for tweeted messages

		outFile.write("[Retweeted Tweets]\nPositive: " + str(reTweetFile["Positive"].mean()) + "\n" +
		       "Negative: " + str(reTweetFile["Negative"].mean()) + "\n" +
		       "Neutral: " + str(reTweetFile["Neutral"].mean()) + "\n" +
		       "Compound: " + str(reTweetFile["Compound"].mean()) + "\n\n" )

	def frequencyTimeZoneTable():

		#Calculate for All Tweets (original + retweet)
		
		#initialize start date & end date
		print("\nTime Zone Frequency Comparison: ")
		input_day = int(raw_input("Enter day: \n"))
		input_hour = int(raw_input("Enter hour: \n"))

		day = csvFile.loc[csvFile['Day'].isin([input_day])]
		hour = csvFile.loc[csvFile['Hour'].isin([input_hour])]
		timeZone_hourly = hour['Time Zone'].value_counts().to_frame()
		timeZone_day = day['Time Zone'].value_counts().to_frame()

		timeZoneCSVPath_hourly = final_directory+"/day"+str(input_day)+"hours"+str(input_hour)+"timeZoneResult.csv" 
		timeZoneCSVPath_day = final_directory+"/day"+str(input_day)+"hours"+str(input_hour)+"timeZoneResult.csv" 
		timeZone_hourly.to_csv( timeZoneCSVPath_hourly, index = True)
		timeZone_day.to_csv( timeZoneCSVPath_day, index = True)

	def frequencyWord():

		top_N = 100

		df = pd.DataFrame(originalTweetFile)
		#initizlie the word to check frequency

		frequentWord = raw_input("\nEnter a word to search: (Frequency Word)\n")
		containFrequentWord = df[df['Text'].str.contains(frequentWord, case=False)]

		#write out as csv file 
		freqWordCSVPath = final_directory+"/freqWordResult.csv" 
		containFrequentWord.to_csv(freqWordCSVPath, index = True, encoding='utf-8')

		stopwords = nltk.corpus.stopwords.words('english')
		# RegEx for stopwords
		RE_stopwords = r'\b(?:{})\b'.format('|'.join(stopwords))
		# replace '|'-->' ' and drop all stopwords
		words = (df['Text']
		           .str.lower()
		           .replace([r'\|', RE_stopwords], [' ', ''], regex=True)
		           .str.cat(sep=' ')
		           .split()
		)

		# generate DF out of Counter
		rslt = pd.DataFrame(Counter(words).most_common(top_N),
		                    columns=['Word', 'Frequency']).set_index('Word')
		#print(rslt)
		btsFrequencyPath=final_directory+"/btsfrequency.csv"
		rslt.to_csv(btsFrequencyPath, index = True, encoding='utf-8')

		#plot
		# rslt.plot.bar(rot=0, figsize=(16,10), width=0.8) 
	
	################################################################################

	current_directory = os.getcwd()
	final_directory = os.path.join(current_directory, r'Results')
	if not os.path.exists(final_directory):
   		os.makedirs(final_directory)

	outFilePath = final_directory + "/Result.txt" 

	csvFile = pd.read_csv(open(filePath,'rU'), encoding='utf-8', engine='c')
	divideCSV_original_retweet() # 1) Divide csvFile to original tweet and retweet
	
	# 2) Open original tweet csv file 
	originalTweetFile = pd.read_csv(open(os.path.join(final_directory,'originalTweet.csv'),'rU'), encoding='utf-8', engine='c')
	reTweetFile = pd.read_csv(open(os.path.join(final_directory,'reTweet.csv'),'rU'), encoding='utf-8', engine='c')
	
	outFile = open(outFilePath, 'w')
	

	select = int(input(" **************************************\
	 \n 1. All \n 2. Num of tweeets that contain keywords (Original Tweet)\
	 \n 3. Num of retweets \n 4. Sentimental Analysis (Original Tweet + Retweet) \n 5. Frequency Time Zone Table\
	  \n 6. Frequency Word \n**************************************\n\n"))

	#Update the header of the result file
	outFile.write(header)

	if(select == 1):

		numTweets()
		numReTweets()
		originalTweetsSentiment()
		retweetSentiment()
		frequencyTimeZoneTable()
		frequencyWord()

	elif(select == 2):

		numTweets()

	elif(select == 3):

		numReTweets()
		
	elif(select == 4):

		originalTweetsSentiment()
		retweetSentiment()

	elif(select == 5):

		frequencyTimeZoneTable()

	elif(select == 6):
		
		frequencyWord()

	else:
		print("wrong number")

main() # Initialize the program
