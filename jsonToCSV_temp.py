import csv
import json
import ast

jsonFilePath = "/Users/summerseo/Desktop/TwitterCode/all_tweets_18.json"

data_json = open(jsonFilePath, mode='r').read() #reads in the JSON file into Python as a string
data_python = json.loads(data_json) #turns the string into a json Python object

# with open(jsonFilePath, 'r+') as inFile: 

#   # jsonFile = json.loads(open(jsonFilePath, "r").read())
# 	# jsonFile = ast.literal_eval(json.dumps(inFile, ensure_ascii=False).encode('utf8'))
# 	jsonFile = ast.literal_eval(inFile)
# 	# print(json.dumps(jsonFile))
# 	# print(jsonFile)
# 	infile.close()

# # jsonFile = ast.literal_eval(open(jsonFilePath, "r"))
# # json_dump = json.dumps(jsonFile)
# # inFile.close()

# csvFile = csv.writer(open("/Users/summerseo/Desktop/TwitterCode/test.csv", "wb+"))

# headers = ["Text", "Positive", "Negative", "Neutral", "Compound", "Username", "Time Zone",
#                "Timestamp", "Time", "Year", "Month", "Day", "Hour", "Minute"]

# csvFile.writerow(headers)


csv_out = open("/Users/summerseo/Desktop/TwitterCode/test.csv", mode='w') #opens csv file
writer = csv.writer(csv_out) #create the csv writer object
 
headers = ["Text", "Positive", "Negative", "Neutral", "Compound", "Username", "Time Zone",
               "Timestamp", "Time", "Year", "Month", "Day", "Hour", "Minute"] #field names
writer.writerow(headers) #writes headers
