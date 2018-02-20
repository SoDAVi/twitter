import pandas as pd
from collections import Counter
import nltk
nltk.download("stopwords")

top_N = 100

f = pd.read_csv("/Users/suyoung/Desktop/GoodDoctor/seventhweek_4~10/Week7_clean.csv")

f = df[df['Text'].str.contains("the good doctor")]

# print(f.head(50))
f.to_csv("/Users/suyoung/Downloads/good doctor.csv")


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
print(rslt)
rslt.to_csv("/Users/suyoung/Downloads/btsfrequency.csv", index = True)

plot
rslt.plot.bar(rot=0, figsize=(16,10), width=0.8)