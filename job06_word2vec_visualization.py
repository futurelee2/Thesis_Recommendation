import pandas as pd
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.manifold import TSNE #차원축소
from matplotlib import font_manager, rc
import matplotlib as mpl

font_path = './malgun.ttf' #다운받은 폰트
font_name = font_manager.FontProperties(fname=font_path).get_name()
mpl.rcParams['axes.unicode_minus']=False #플랏에 한글 적기 위해( False 안하면 깨짐)
rc('font',family=font_name) #폰트 지정

embedding_model = Word2Vec.load('./models/word2vec_thesis_abstract.model')
key_word = '항공' #유사어는 학습한 데이터 기준이됨으로 유사어가 달라질수있음
sim_word = embedding_model.wv.most_similar(key_word, topn=10) #키워드 기준으로 유사한 단어 10개 (topn 개수)
print(sim_word) #첫번째값: 라벨, 두번째값:유사도

vectors = []
labels = []

for label, _ in sim_word:
    labels.append(label)
    vectors.append(embedding_model.wv[label])
print(vectors[0])
print(len(vectors[0]))

df_vector = pd.DataFrame(vectors)
print(df_vector)

tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500)
# TSNE: 차원 축소 모델: 데이터의 정보를 최대한 날아가지않도록 해줌
# n_components: N차원으로 축소

new_value = tsne_model.fit_transform(df_vector)
df_xy = pd.DataFrame({'words':labels, 'x':new_value[:,0], 'y':new_value[:,1]}) #유사단어
df_xy.loc[len(df_xy)] = (key_word, 0, 0)
print(df_xy) #x,y 좌표로 바꿔서 2차원상 그릴 수 있음


plt.figure(figsize=(8,8))
plt.scatter(0,0,s = 500, marker='*')
plt.scatter(df_xy['x'], df_xy['y']) #점찍기

for i in range(len(df_xy)):
    a = df_xy.loc[[i,10]]
    plt.plot(a.x, a.y, '-D', linewidth =3)
    plt.annotate(df_xy.words[i], xytext=(1,1), xy=(df_xy.x[i], df_xy.y[i]),
                 textcoords = 'offset points', ha ='right', va='bottom') #선긋기

plt.show()  #key_word 값이 중심