from pymongo import MongoClient
from functions import *
 
import requests
import json
import time
import tweepy
import time

from datetime import datetime

while(1>0):
    now = datetime.now()

    client = MongoClient('localhost', 27017)

    banco = client.dashboard
    data= now.strftime("%m/%d/%Y, %H:%M:%S")
    tweets = banco[data]


    cred = json.load(open('key.json'))
    consumer_key = cred['consumer_key']
    consumer_secret = cred['consumer_secret']
    access_token = cred['access_token']
    access_token_secret = cred['access_token_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')

    BRAZIL_WOE_ID = 23424768
    brazil_trends = api.trends_place(BRAZIL_WOE_ID)
    trends = json.loads(json.dumps(brazil_trends, indent=1))


    for trend in trends[0]["trends"]:
        
        #vai armezar todos os tweets
        tts_tema={"tema":(trend["name"]),
        "tweet":[]
        }
        
        #50 tweets sobre um tema
        resultados = api.search(q=trend["name"],count=50,lang='pt',tweet_mode='extended')
        
        for tweet in resultados:
            tt={"texto":tweet.full_text, "id_tweet":tweet.id}

            #nome de todas as collections do bd
            all_NamesCollections = banco.list_collection_names()

            #verificar se ID já existe no BD para poder fazer o append
            if(exist_tweet(all_NamesCollections, banco, trend["name"], tt['id_tweet'])):
                print('Tweet Repetido')
            else:
                tts_tema['tweet'].append(tt)

        tweets.insert_one(tts_tema).inserted_id 

    print('Coleta realizada em: ')
    print(data)
    time.sleep(300)
