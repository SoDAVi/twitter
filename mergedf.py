import pandas as pd


f1 = pd.read_csv("/Users/suyoung/Desktop/GoodDoctor/eleven_2~8/2~5.csv")
f2 = pd.read_csv("/Users/suyoung/Desktop/GoodDoctor/eleven_2~8/1~8.csv")
# f3 = pd.read_csv("/Users/suyoung/Desktop/GoodDoctor/seventhweek_4~10/all_tweets_1_parse.csv")

frames = [f1, f2]
result = pd.concat(frames,ignore_index=True)

result.to_csv("/Users/suyoung/Desktop/GoodDoctor/eleven_2~8/merged.csv",index=False)