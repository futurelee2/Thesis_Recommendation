import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/reviews_final.csv')
df.info()
print(df.head())

df_stopwords = pd.read_csv('./stopwords.csv', index_col=0)
stopwords = list(df_stopwords['stopword'])
stopwords = stopwords + ['하다','제시','논문','확인','또는','소개','또한','이다','있다','되다','보다','많다','되어다']

okt = Okt()
df['clean_abstracts'] = None #df에 새로운 컬럼 추가(none값으로)

count = 0
for idx, abstract in enumerate(df.abstracts):
    count += 1

    if count % 10 == 0: #점찍는거
        print('.', end='') #end ''은 줄바꿈이 안됨
    if count % 1000 == 0:
        print() #줄바꿈됨

    abstract = re.sub('[^가-힣 ]', ' ', abstract) # ^글자 빼고, 빈칸으로 만들기, abstract 변수 안에있는 값을
    df.loc[idx, 'clean_abstracts'] = abstract
    token = okt.pos(abstract, stem=True)
    df_token = pd.DataFrame(token, columns=['word', 'class']) #word형태소, class품사
    df_token = df_token[(df_token['class']=='Noun') |
                        (df_token['class']=='Verb') |
                         (df_token['class']=='Adjective')]


    words = []
    for word in df_token.word:
        if len(word) > 1:
            if word not in list(df_stopwords.stopword):
                words.append(word)
    cleaned_sentence = ' '.join(words)
    df.loc[idx, 'clean_abstracts'] = cleaned_sentence
print(df.head(30))
df.dropna(inplace=True)
df.to_csv('./crawling_data/cleaned_abstracts_2020_2022.csv', index=False)


























