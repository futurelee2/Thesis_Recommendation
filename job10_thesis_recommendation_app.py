import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QSize
from PyQt5 import QtGui
import pandas as pd
from PyQt5.QtCore import QStringListModel
from scipy.io import mmread
import pickle
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import linear_kernel
import re
from konlpy.tag import Okt




form_window = uic.loadUiType('./designer/kiss_application.ui')[0]

class Exam(QWidget, form_window):  # class ~ def 라인만 의미를 가지고 있는 문장.
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('My Second Application')
        self.setFixedSize(QSize(1155, 650))
        self.line_edit.setFrame(False)



        # 모델 로딩
        self.tfidf_matrix = mmread('./models/tfidf_thesis_abstracts.mtx').tocsr()
        with open ('./models/tfidf.pickle', 'rb') as f:
            self.tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_thesis_abstract.model')
    #
    #
        self.df_thesis = pd.read_csv('./crawling_data/cleaned_abstracts_2020_2022.csv')
        self.titles = self.df_thesis['titles']
        self.address = list(self.df_thesis['address'])
    #
        # model = QStringListModel()
        # model.setStringList(self.titles)               # ()안에는 필요한 대상 | () 안에는 list or series 형태
        # completer = QCompleter()
        # completer.setModel(model)
        # self.line_edit.setCompleter(completer)


    #     # Slot 연결
        self.btn_search.clicked.connect(self.search_thesis)



    def search_thesis(self):
        key_word = self.line_edit.text()

        # # title로 검색할 때,
        # if key_word in self.titles:
        #     self.recommendation_by_movie_title(key_word)

        # 리뷰 키워드로 검색할 때,
        if key_word in list(self.embedding_model.wv.index_to_key):
            self.recommendation_by_key_word(key_word)

        # 문장으로 검색할 때,
        else:
            self.recommendation_by_sentence(key_word)


    def getRecommendation(self, cosin_sim):

        simScore = list(enumerate(cosin_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)  # simScore를 유사도 높은 순으로 sort.
        simScore = simScore[:6]  # 자기 자신을 포함하기 때문에 출력하고 싶은 영화 갯수 + 1을 줘야함 ([:11] -> [0]~[10] 11개 추출)
        thesis_idx = [i[0] for i in simScore]  # [0] = 영화의 Index가 들어있음. |  [1] = 영화 유사도
        recThesisList = self.df_thesis.iloc[thesis_idx, 0]  # df_reviews의 컬럼_0 = 영화 제목
        return recThesisList

    def getURL(self, cosin_sim):

        simScore = list(enumerate(cosin_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)  # simScore를 유사도 높은 순으로 sort.
        simScore = simScore[:6]  # 자기 자신을 포함하기 때문에 출력하고 싶은 영화 갯수 + 1을 줘야함 ([:11] -> [0]~[10] 11개 추출)
        thesis_idx = [i[0] for i in simScore]  # [0] = 영화의 Index가 들어있음. |  [1] = 영화 유사도
        urlThesisList = self.df_thesis.iloc[thesis_idx, 2]
        return urlThesisList


    def recommendation_by_key_word(self, key_word):
        sim_word = self.embedding_model.wv.most_similar(key_word, topn=10)
        words = [key_word]
        for word, _ in sim_word:
            words.append(word)
        sentence = []
        count = 11
        for word in words:
            sentence = sentence + [word] * count
            count -= 1
        sentence = ' '.join(sentence)
        sentence_vec = self.tfidf.transform([sentence])
        cosin_sim = linear_kernel(sentence_vec, self.tfidf_matrix)
        recommendation = self.getRecommendation(cosin_sim)
        urlThesisList = self.getURL(cosin_sim)
        recommendation = list(recommendation)
        urlThesisList = list(urlThesisList)
        recommendations = ''
        for i in range(5):
            recommendations_i = '<a href = "{}" style="text-decoration:none; color: black">{}</a><br><br>'.format(
                urlThesisList[i], recommendation[i])
            recommendations += recommendations_i
        self.lbl_recommend.setText(recommendations)
        self.lbl_recommend.setWordWrap(True)
        self.lbl_recommend.setOpenExternalLinks(True)
        self.lbl_recommend.setFont(QtGui.QFont("칠곡할매 이종희체", 15))  # 폰트,크기 조절


    def recommendation_by_sentence(self, key_word):
        review = re.sub('[^가-힣 ]', ' ', key_word)
        okt = Okt()
        token = okt.pos(review, stem=True)
        df_token = pd.DataFrame(token, columns=['word', 'class'])
        df_token = df_token[(df_token['class']=='Noun') |
                            (df_token['class']=='Verb') |
                            (df_token['class']=='Adjective')]
        words = []
        for word in df_token.word:
            if 1 < len(word):
                words.append(word)
        cleaned_sentence = ' '.join(words)
        print(cleaned_sentence)
        sentence_vec = self.tfidf.transform([cleaned_sentence])
        cosin_sim = linear_kernel(sentence_vec, self.tfidf_matrix)
        recommendation = self.getRecommendation(cosin_sim)
        urlThesisList = self.getURL(cosin_sim)
        recommendation = list(recommendation)
        urlThesisList = list(urlThesisList)
        recommendations = ''
        for i in range(5):
            recommendations_i = '<a href = "{}" style="text-decoration:none; color: black">{}</a><br><br>'.format(
                urlThesisList[i], recommendation[i])
            recommendations += recommendations_i
        self.lbl_recommend.setText(recommendations)
        self.lbl_recommend.setWordWrap(True)
        self.lbl_recommend.setOpenExternalLinks(True)
        self.lbl_recommend.setFont(QtGui.QFont("칠곡할매 이종희체", 15))  # 폰트,크기 조절









if __name__ == "__main__":

    app = QApplication(sys.argv)   #Qapplication : PyQt5 내부 어플리케이션
    mainWindow = Exam()            # 해당 라인에서 객체가 생성됨
    mainWindow.show()              # .show : 화면에 출력하도록 하는 명령
    sys.exit(app.exec_())          # (app.exec_()) : 해당 프로그램 종료.
                                   # app ~ exec_()) 까지가 위젯에 쓰이는 모듈.