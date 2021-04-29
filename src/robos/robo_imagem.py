import requests
import traceback

from googleapiclient.discovery import build
from robos.pln.pipeline import Pipeline
from robos import robo_state
from util.gerencia_arquivo import GerenciaArquivo as ga

from wand.image import Image
from wand.display import display
from wand.color import Color
from wand.font import Font

from dotenv import load_dotenv
import os 

pipe = Pipeline()

load_dotenv()

custom_search = build("customsearch", "v1", developerKey=os.getenv('API_KEY'))

def imprimir(msg):
    print(f'Robo imagem > {msg}')

def verifica_palavras_chave_mesmo_termo_busca(contexto, sent):
    imprimir('verificando se as palavras chaves são as mesmas do termo de busca')
    termo_busca = pipe.tokenize(contexto.get_termo_busca().lower())
    for i, palavra in enumerate(sent.get_palavras_chave()):
        imprimir(f'verificando a {i+1}º palavra')
        palavra_chave = palavra.lower()
        for termo in termo_busca:
            if termo in palavra_chave:
                sent.get_palavras_chave().remove(palavra)
                break
    imprimir('verificação das palavras chave terminadas')


def busca_google_return_imagens(query):
    response = custom_search.cse().list(
        cx=os.getenv('SEARCH_ENGINE_ID'),
        q=query,
        searchType = 'image',
        num=2#quantidade de resultados da busca
    ).execute()

    img_links = []
    try:
        for item in response['items']:
            img_links.append(item['link'])
    except:
        print(f'O termo de busca ficou montado estranho, e provavelmente nao retornou resultado. termo {query}')
    
    return img_links

def busca_imagem_all_sentences(contexto):
    imprimir('iniciando a busca das imagens correspondentes as sentenças')
    for i, sent in enumerate(contexto.get_sentences()):
        if len(sent.get_palavras_chave()) <= 0:
            continue
        verifica_palavras_chave_mesmo_termo_busca(contexto, sent)
        query = '{} {}'.format(contexto.get_termo_busca(), ' '.join(sent.get_palavras_chave()[:1]))
        imprimir(f'termo busca gerado: {query}')
        sent.set_image_url(busca_google_return_imagens(query))
    imprimir('busca das imagens finalizada')

def baixa_salva(url_image, nome_arquivo):
    response = requests.get(url_image)

    if not ga.existe_diretorio('./assets/img'):
        ga.cria_diretorio('./assets/img')

    with open(f'./assets/img/{nome_arquivo}', 'wb') as file:
        file.write(response.content)

def download_imagens(contexto):
    imprimir('iniciando o download das imagens das sentenças')
    imagens_baixadas = []
    for i, sent in enumerate(contexto.get_sentences()):
        for image_url in sent.get_image_url():
            try:
                if image_url in imagens_baixadas:
                    raise Exception('imagem ja foi baixada')
                
                baixa_salva(image_url, f'{i}-original.png')
                imprimir(f'baixou a imagem: {image_url}')
                break
            except:
                imprimir(f'nao foi possivel baixa a imagem: {image_url}')
    imprimir('finalizado o download das imagens')

def init():
    imprimir('iniciando')
    ctx = robo_state.load()

    busca_imagem_all_sentences(ctx)
    download_imagens(ctx)
    
    imprimir('finalizado')