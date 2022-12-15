import numpy as np
import pandas as pd
import glob
import datetime

data_path = glob.glob('./crawling_data/reviews_202?.csv') #리스트로 불러옴
print(data_path)
df = pd.DataFrame()
for path in data_path:
    df_temp = pd.read_csv(path)
    df = pd.concat([df, df_temp], ignore_index=True) #데이터프레임만 합치기: concat, 리스트합치기: append(마지막 행의 끝에 추가됨)

#df['year'] = 2022
print(df.head(30))
# df['abstracts'].replace(' ', np.NaN ,inplace=True)
# print(df['abstracts'])
df.drop_duplicates(inplace=True) #중복제거
df.dropna(inplace=True) #결측치 제거
df.reset_index(inplace=True, drop=True)
print(df.head())

df.info()

df.to_csv('./crawling_data/reviews_final.csv', index=False)


