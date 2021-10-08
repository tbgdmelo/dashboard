import random
import pandas as pd

from functions import *
from tratamento import tratamentoTweet

#recebe como parametro o banco e a collection
def dbtoDf(banco, nomeCollection):
    #coletar o tweet do banco

    collection = get_collection(nomeCollection,banco)

    df = pd.DataFrame(columns=["tema","texto"])

    #coletar os tweets da base pra poder gerar o df
    k=0
    lista = get_all_tweets( collection )
        
    p=0
    while(p<len(lista)):
        for tweet in lista[p]['tweets']:
            df.loc[len(df)]=[ lista[p]['tema'], tratamentoTweet(tweet)]
                
        p+=1
    k+=1

    return df

#recebe como parametro: banco e limite de quantos ultimos
#retorna uma lista de obj collections

def ultimasCollections(banco, limite):
    #coletar o nome das ultimas 10 collections
    all_NamesCollections = banco.list_collection_names()
    all_NamesCollections.sort()

    #nomes das ultimas collections
    ultimos=[]
    i=1
    while(i<limite):
        ultimos.append( all_NamesCollections[len(all_NamesCollections)-i])
        i+=1
    ultimos

    i=0
    l_collection=[] #lista com obj collections
    while(i<len(ultimos)):
        l_collection.append(get_collection(ultimos[i],banco))
        i+=1


#recebe como parametro: lista com as collections
#retorna dataframe contendo tema e tweet das collections pedidas
def collectionToDf(l_collection):
    df = pd.DataFrame(columns=["tema","texto"])
    #coletar os tweets da base pra poder gerar 
    k=0
    while(k<len(l_collection)):
        lista = get_all_tweets( l_collection[k] )
        
        p=0
        while(p<len(lista)):
            for tweet in lista[p]['tweets']:
                df.loc[len(df)]=[ lista[p]['tema'], tratamentoTweet(tweet)]
                
            p+=1
        k+=1
    
    return df

#recebe a conexao com o banco e retorna uma lista com os obj collections
def ultimasCollections(banco):
    #coletar o nome das ultimas 10 collections
    all_NamesCollections = banco.list_collection_names()
    all_NamesCollections.sort()

    #nomes das ultimas collections
    ultimos=[]
    i=1
    while(i<10):
        ultimos.append( all_NamesCollections[len(all_NamesCollections)-i])
        i+=1
    ultimos

    i=0
    l_collection=[] #lista com obj collections
    while(i<len(ultimos)):
        l_collection.append(get_collection(ultimos[i],banco))
        i+=1

    return l_collection


#recebe uma lista de collections e retorna um df de todas
def createDf(l_collection):
    #cria um dataframe de todas as collections juntas
    df2 = pd.DataFrame(columns=["tema","texto"])
    #coletar os tweets da base pra poder gerar o df
    k=0
    while(k<len(l_collection)):
        lista = get_all_tweets( l_collection[k] )
        
        p=0
        while(p<len(lista)):
            for tweet in lista[p]['tweets']:
                df2.loc[len(df2)]=[ lista[p]['tema'], tratamentoTweet(tweet)]
                
            p+=1
        k+=1
    
    return df2

#recebe como parametro um dataframe e retorna a lista e o dicionario com os temas
def tratamentoDf(df):
    #conta quantos temas tem no dataframe
    temas = df['tema'].value_counts()

    #cria um dicionario com os temas e quantos tweets ele tem
    #cria uma lista com os nomes dos temas
    dic_temas  = dict(temas)
    nome_temas = list(dic_temas.keys())

    #removendo temas que tem menos de 100 tweets coletados
    i=0
    while(i<len(nome_temas)):
        if(dic_temas[nome_temas[i]] < 100):
            del dic_temas[nome_temas[i]]
        i+=1

    return dic_temas, nome_temas

#recebe o dataframe grande e o nome do tema
def separaDataframe(s,df):
    #separa do datraframe gigante apenas as linhas que tem um tema especifico
    df_de_um_tema = df.query('tema == "'+ s +'"')
    df_de_um_tema.head()

    return df

