import pandas as pd


f = pd.read_csv("/Users/suyoung/Desktop/GoodDoctor/1~22.csv")

#f1 = f[f.Day == 25]
#f1 = f[f.Hour == 19]
f1 = f.loc[f['Day'].isin(['9','10','11','12','13','14','15'])]
# f2 = f1[f1.Hour == 19]


f1.to_csv("/Users/suyoung/Desktop/GoodDoctor/twelve_9~15/9~15.csv", index = False)