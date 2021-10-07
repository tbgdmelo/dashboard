from nltk import word_tokenize
import nltk
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn import metrics
from sklearn.model_selection import cross_val_predict
#%matplotlib inline
from tratamento import *
from nltk.tokenize import word_tokenize as tokenizador

nltk.download('punkt')

def createModel():

    df = pd.read_csv('imdb-reviews-pt-br.csv', encoding='utf-8')

    df["sentiment_int"] = df["sentiment"].map({"pos": 0, "neg": 1})
    del df['text_en']
    del df['sentiment']

    texto = df['text_pt']
    classes = df['sentiment_int']

    # Aplica a função de processamento em todos os dados
    texto = [Preprocessing(i) for i in texto]

    # Instancia o objeto que faz a vetorização dos dados de texto
    vectorizer = CountVectorizer(analyzer="word", tokenizer=tokenizador)

    # Aplica o vetorizador nos dados de texto e retorna uma matriz esparsa ( contendo vários zeros)
    freq_textos = vectorizer.fit_transform(texto)

    # Treino de modelo de Machine Learning
    modelo = MultinomialNB()
    modelo.fit(freq_textos,classes)

    return modelo

