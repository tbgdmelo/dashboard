import requests
import json
import time
import re

#t é uma string contendo o tweet completo
def tratamento(t):
        #remover os @ marcados no tweet
        t=re.sub(r'@[aA-zZ]* ', '', t, flags=re.MULTILINE)

        #remover dados quando é RT
        t=re.sub(r'RT @*[aA-zZ]*[0-9]*: ', '', t, flags=re.MULTILINE)

        #remover links
        t=re.sub(r'https:\/\/t.co\/*[aA0-zZ9]* ', '', t, flags=re.MULTILINE)

        emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                "]+", flags=re.UNICODE)

        t=emoji_pattern.sub(r' ', t)


        return t