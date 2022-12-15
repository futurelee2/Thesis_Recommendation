# 자연어처리 유용한 시각화 도구 > 많이 나오면 크게 그려줌, 작게 나오면 작게그려줌
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections
from matplotlib import font_manager, rc
from PIL import Image
import matplotlib as mpl


font_path = './malgun.ttf' #다운받은 폰트
font_name = font_manager.FontProperties(fname=font_path).get_name()
mpl.rcParams['axes.unicode_minus']=False #플랏에 한글 적기 위해( 안하면 깨짐)
rc('font',family=font_name)

df = pd.read_csv('./crawling_data/cleaned_abstracts_2020_2022.csv')
words = df[df['titles']=='유도탄 전자기 내성 시험에 대한 고찰']['clean_abstracts']
print(words.iloc[0])
words = words.iloc[0].split()
print(words)

worddict = collections.Counter(words)
worddict = dict(worddict)
print(worddict)

wordcloud_img = WordCloud(background_color='white', max_words=2000,
                          font_path=font_path). generate_from_frequencies(worddict) # 출력되는 단어개수 2000개로 제한
#wordcloud 이미지 생성
plt.figure(figsize=(12,12))
plt.imshow(wordcloud_img, interpolation='bilinear') #bilinear 블러처리
plt.axis('off') #많이 나오는 단어는 크게 그려줌


# 이부분 비교하기 위해서 추가함 (겨울왕국과 겨울왕국을 통해 추천받은 영화를 비교하기 위해)
words = df[df['titles']=='Caffe를 이용한 얼굴 인식 파이프라인 모델 구현']['clean_abstracts']
words = words.iloc[0].split()
worddict = collections.Counter(words)
worddict = dict(worddict)
wordcloud_img = WordCloud(background_color='white', max_words=2000,
                          font_path=font_path). generate_from_frequencies(worddict)
plt.figure(figsize=(12,12))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')

plt.show() #show 전에 두개 그리면 둘다 그려줌

