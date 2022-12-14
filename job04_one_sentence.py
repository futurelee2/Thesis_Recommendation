# 하나로 합쳐서 하나의 문장으로 만들기
# 영화제목 하나당 하나의 리뷰 문장으로 만들기

import pandas as pd

df = pd.read_csv('./crawling_data/cleaned_abstracts_2020_2022.csv') #앞에 ./ 없으면 현재폴더에서 찾음
df.dropna(inplace=True)
df.info()

one_sentences = []
for title in df['titles'].unique():
    temp = df[df['titles']==title]
    if len(temp) > 30:
        temp = temp.iloc[:30, :]
    one_sentence = ' '.join(temp['clean_abstracts'])
    one_sentences.append(one_sentence)

df_one = pd.DataFrame({'titles':df['titles'].unique(),'abstracts':one_sentences})
print(df_one.head())
df_one.to_csv('./crawling_data/one_sentences.csv',index=False)
