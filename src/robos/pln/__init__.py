from robos.pln.pipeline import Pipeline
from robos.pln.watson_pln import get_palavras_chave as w_get_plr_chave
import sklearn

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from heapq import nlargest
from collections import defaultdict
import re

pipe = Pipeline()

def get_entidades_nomeadas(text):
    
    def preprocess(text):
        return re.sub(r'\d', '', text)

    stops              = pipe.get_stop_words() + ['``', 'vez', 'vezes', 'ter', 'tinha', 'º', "''", 'filho']
    palavras_sem_stops = pipe.get_palavras_sem_stops(preprocess(text), stops)

    tag_token = pipe.tag(palavras_sem_stops)
    entidades_nomeadas = []
    for token, tag in tag_token:
        if tag in 'N' or  tag in 'NPROP':
            entidades_nomeadas.append(token)
    
    return entidades_nomeadas[:6]

def get_palavras_chave_watson(sentence):
    return w_get_plr_chave(sentence)

def get_palavras_chave(text, sentence):

    def preprocess(text):
        return re.sub(r'\d', '', text)

    qtd_entidades_nomeadas = 3
    qtd_demais_palavras    = 3

    doc  = [preprocess(text)]
    sent = [preprocess(sentence)]
    
    stops             = pipe.get_stop_words() + ['``', 'vez', 'vezes', 'ter', 'tinha', 'º']
    count_vector      = CountVectorizer(tokenizer=pipe.tokenize_tf_idf, stop_words=stops, ngram_range=(1,1))
    word_count_vector = count_vector.fit_transform(doc)

    tf_idf_transformer = TfidfTransformer(smooth_idf=True, use_idf=False)
    tf_idf_transformer.fit(word_count_vector)

    arr_tf_idf = tf_idf_transformer.transform(count_vector.transform(sent))
    #transforma em uma matriz de coordenadas
    arr_tf_idf = arr_tf_idf.tocoo()
    arr_tf_idf = zip(arr_tf_idf.col, arr_tf_idf.data)
    
    sorted_item = sorted(arr_tf_idf, key=lambda x: (x[1], x[0]), reverse=True)

    feature_names = count_vector.get_feature_names()
    
    entidades_nomeadas = []
    scores_entidades_nomeadas = defaultdict(int)
    for idx, score in sorted_item:
        token, tag = pipe.tag([feature_names[idx]])[0]
        #aqui eu pego as palavras que possouem a tag de nome proprio
        if tag in 'N' or  tag in 'NPROP':
            entidades_nomeadas.append(token)
            scores_entidades_nomeadas[idx] = score
    
    cont = 0
    palavras_melhor_ranqueadas = []
    for idx, score in sorted_item:
        token = feature_names[idx]
        if token in entidades_nomeadas:
            continue
        
        if cont >= qtd_demais_palavras:
            break
        
        palavras_melhor_ranqueadas.append(token)
        cont += 1

    idx_ent_rank = nlargest(qtd_entidades_nomeadas, scores_entidades_nomeadas, key=scores_entidades_nomeadas.get)

    n_entidades_nomeadas = [feature_names[i] for i in sorted(idx_ent_rank)]
    palavras_chave = n_entidades_nomeadas + palavras_melhor_ranqueadas

    return palavras_chave