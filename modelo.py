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

#recebe o df de um tema, o modelo e o vetorizador
#retorna 1 se for negativo e 0 positivo
def defineSentimento(df_tema, modelo, vectorizer):
    #verifica se o sentimento daquele tema é negativo ou positivo

    #processa os dados para passar pro modelo
    tweets = df_tema['texto']
    tweets = [Preprocessing(i) for i in tweets]
    tweets_testes = vectorizer.transform(tweets)

    # 1= negativo
    # 0= positivo
    positivo=0
    negativo=0

    #conta qual sentimento mais aparece
    for t, c in zip (tweets,modelo.predict(tweets_testes)):
        if(c==1):
            negativo+=1
        else:
            positivo+=1
            
    if(negativo>positivo):
        return 1
    else:
        return 0