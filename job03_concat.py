import pandas as pd
import glob
import datetime

data_path = glob.glob('./crawling_data/reviews_2021_*.csv')
print(data_path)
df = pd.DataFrame()
for path in data_path:
    df_temp = pd.read_csv(path)
    df = pd.concat([df, df_temp], ignore_index=True)
print(df.head(30))
df.dropna(inplace=True)
df.reset_index(inplace=True, drop=True)
print(df.head())

df.info()

df.to_csv('./crawling_data/reviews_2021.csv', index=False)


