import pandas as pd
import csv
# import statistics as s
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


f = pd.read_csv("/Users/suyoung/Desktop/GoodDoctor/twelve_9~15/Week12_clean.csv")

# f = open("/Users/suyoung/Desktop/GoodDoctor/ninethweek_18~24/Week9_clean.csv", 'rU')

# with open("/Users/suyoung/Desktop/GoodDoctor/eigthweek_11~17/Week8_clean.csv", 'rU') as f:


# f.to_csv("/Users/suyoung/Desktop/Week7_clean")

# f1 = f[f["Text"].str.contains("rt")]
# f1 = f[f["Text"].str.contains("rt")==False]
f1 = f[f["Text"].str.contains("korea" or "korean" or "remake")]
print (len(f1))
#
# f2 = f1['Text'].value_counts().to_frame()
# # # #
# # #
# f2.to_csv("/Users/suyoung/Desktop/GoodDoctor/twelve_9~15/toprt.csv", index = True)
# # #
# #
#
print("Positive: " + str(f1["Positive"].mean()) + "\n" +
       "Negative: " + str(f1["Negative"].mean()) + "\n" +
       "Neutral: " + str(f1["Neutral"].mean()) + "\n" +
       "Compound: " + str(f1["Compound"].mean()))