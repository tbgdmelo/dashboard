from pymongo import MongoClient

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


    #dados={"tweets":[]}
    for trend in trends[0]["trends"]:
        
        tts_tema={"tema":(trend["name"]),
        "tweet":[]
        }
        
        resultados = api.search(q=trend["name"],count=50,lang='pt',tweet_mode='extended')
        
        for tweet in resultados:
            tt={"texto":tweet.full_text.encode("utf-8"), "id_tweet":tweet.id}
            tts_tema['tweet'].append(tt)
        
        tweets.insert_one(tts_tema).inserted_id 
        #dados['tweets'].append(tts_tema)
        
    #dados_id = tweets.insert_one(dados).inserted_id

    #print(dados_id)

    print('Coleta realizada em: ')
    print(data)
    time.sleep(3600)

