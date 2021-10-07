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