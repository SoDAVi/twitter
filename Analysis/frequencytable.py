import pandas as pd

f = pd.read_csv("/Users/suyoung/Desktop/GoodDoctor/twelve_9~15/Week12_clean.csv")

f1 = f.loc[f['Day'].isin(['11'])]
f2 = f1.loc[f['Hour'].isin(['19'])]
# print(len(f2))
print(len(f2))

f3 = f2['Time Zone'].value_counts().to_frame()

# print(f2)
f3.to_csv("/Users/suyoung/Desktop/GoodDoctor/twelve_9~15/day11_7pmfrequency.csv", index = True)

# print(len(f2))
# f3 = f2['Time Zone'].value_counts().to_frame()


# f1 = f.loc[f['Day'].isin(['9'])]
#
# f2 = f1.loc[f['Hour'].isin(['19'])]
#
# print (len(f2))

# f3 = f1['Time Zone'].value_counts().to_frame()
# #
# print f3
# f3.to_csv("/Users/suyoung/Desktop/GoodDoctor/thirdweek/Oct9_timezone_allday_frequency.csv", index = True)
#