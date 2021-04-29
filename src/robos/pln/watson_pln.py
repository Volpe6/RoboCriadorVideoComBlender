import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions

from dotenv import load_dotenv
import os 

authenticator = IAMAuthenticator(os.getenv('WATSON_API_KEY'))
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=authenticator
)

natural_language_understanding.set_service_url(os.getenv('WATSON_SERVICE_URL'))

def get_palavras_chave(sentence):
    response = natural_language_understanding.analyze(
        text=sentence,
        language='Portuguese',
        features=Features(keywords=KeywordsOptions(
            sentiment=False,
            emotion=False,
            limit=3,
        ))
    ).get_result()

    palavras_chave = []
    try:
        for palavra in response['keywords']:
            palavras_chave.append(palavra['text'])
    except:
        print('Não foram retornadas palavras chave')
    return palavras_chave