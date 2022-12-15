#단어를 백터화

import pandas as pd
from gensim.models import Word2Vec

review_word = pd.read_csv('./crawling_data/cleaned_abstracts_2020_2022_1.csv')
review_word.dropna(inplace=True) #none값 안지워져서 다시 한번 더 넣음
review_word.info()

one_sentence_reviews = list(review_word['clean_abstracts'])


cleaned_tokens = []
for sentence in one_sentence_reviews: #형태소가 들어있는 리스트로 줘야함(형태소단위로 띄어쓰기 되어있음)
    # print(sentence)
    token = sentence.split()
    # print(token)
    cleaned_tokens.append(token)

embedding_model = Word2Vec(cleaned_tokens, vector_size=100,
                           window=4, min_count=10,
                           workers=8, epochs=100, sg=1)

embedding_model.save('./models/word2vec_thesis_abstract.model')
print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))


# word2vec 는 cpu여러개써서 병행처리 가능 (가진 cpu의 절반만 줘야함)
# vector size = 100으로 차원축소
# window =4는 convd1 레이어처럼 4단어를 비교해서 보겟다(4단어씩 잘라서 학습을 하겠다)
# min count = n번 이상 나와야 학습한다, 이하는 버린다 (n번 이상 나와야 종이백에 넣음)
# workers = cpu 개수
# sg =0 > cbow 알고리즘 단어: 단어의 순서까지 고려, 오늘 저녁은 이태리,아시아(비슷한단어) 풍으로.. (: 바뀌는 자리만)
# sg =1 > 여름엔 수박, 여름휴가는 해수욕장(여름 수박 휴가 해수욕장: 비슷한단어) (:단어의 주변, 앞뒤를 보는 것)
#bow: back of word (단어들의 종이봉투, 무작위)

#겨울 축에 겨울과 관련된 단어들이 겨울과 관계있으면 큰 값을 줌(의미차원=의미가 크면 큰값, 작으면 작은값)
#비슷한 의미를 가진 단어들이 가깝게 배치
#좌표(1,1)는 값일 뿐, 벡터(1,1)는 길이와 방향,크기(모든 값 제곱한뒤 루트)를 가짐
#word2vec 말뭉치들을 의미차원에 배치하고 각 단어들의 좌표를 만듦 > 유니크한 단어들의 개수만큼 차원(좌표)이 만들어지는 것 차원 축소 필요(학습을 하면서 의미공간에 좌표 배치됨)
#차원축소 시 데이터 손실있음 ( 최대한 유지하면서 축소시키는게 pca)