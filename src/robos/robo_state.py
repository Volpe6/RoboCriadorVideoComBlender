import json
from model import Contexto, Sentence

NOME_ARQUIVO = 'data.json'

def generate_json_object(obj):
    data = {}
    for attr in obj.__dict__:
        nome  = attr
        campo = obj.__dict__[attr]#valor do campo. por um nome melhor, para o nome da variavel

        if type(campo) is list:
            if len(campo) > 0:
                
                if type(campo[0]) is str:
                    data[nome] = campo
                    continue

                if isinstance(campo[0], object):
                    lista = []
                    for obj in campo:
                        lista.append(generate_json_object(obj))
                    data[nome] = lista
                    continue        

        data[nome] = campo
        
    return data

def load_json_object(json_object):
    con = Contexto()
    for key, value in json_object.items():

        if type(value) is list:
            if len(value) > 0 and isinstance(value[0], object):
                list_sent = []
                for sent in value:
                    sentt = Sentence('', '')
                    for keyy, valuee in sent.items():
                        setattr(sentt, keyy, valuee)
                    list_sent.append(sentt)
                setattr(con, key, list_sent)
                continue

        setattr(con, key, value)
    
    return con

def save(contexto):
    data = generate_json_object(contexto)
    with open(NOME_ARQUIVO, 'w') as file:
        json.dump(data, file)

def load():
    data = object()
    with open(NOME_ARQUIVO) as file:
        try:
            data = json.load(file)
        except Exception as ex:
            print(f'nao foi possivel abrir o arquivo {NOME_ARQUIVO}')
    
    return load_json_object(data)
