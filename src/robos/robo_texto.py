import re
from model import Sentence

import robos.pln as pln
from robos.services import service_wikipedia as wiki_api
from robos.pln.pipeline import Pipeline

from robos import robo_state

def imprimir(msg):
    print(f'Robo texto > {msg}')

def busca_conteudo_wikipedia(contexto):
    '''
    baixa o conteuda pela api da wikipedia
    '''
    imprimir('baixando o conteudo da wikepedia')
    page_wikipedia = wiki_api.page(contexto.get_full_termo_busca())
    conteudo_wiki  = page_wikipedia.content
    
    contexto.set_original_content(conteudo_wiki)
    imprimir('conteudo da wiki baixado')
    

def sanitize_wikipedia_content(contexto):
    '''
    trata o conteudo retornado da wikipedia
    '''
    imprimir('iniciando a limpeza do conteudo da wiki')
    def remove_datas_in_parenteses(text):
        pattern = r'\((\d{4})\)|\([^()]*\)'
        return re.sub(pattern, ' ', text)


    def sanitize_content(text):
        '''
        remove as linhas em branco e linhas com markdown
        '''
        imprimir('removendo markdown e linhas em branco')
        linhas = text.split('\n')#todas as linhas to texto

        linhas_sem_espacos_em_branco_markdown = []
        for linha in linhas:
            if len(linha) == 0 or linha.strip().startswith('='):
                continue
            linhas_sem_espacos_em_branco_markdown.append(linha)
        
        imprimir('unindo tudo em uma unica string')
        text = ' '.join(linhas_sem_espacos_em_branco_markdown)
        imprimir('removendo datas dentro de parenteses')
        text = remove_datas_in_parenteses(text)
        return text
    
    content_tratado = sanitize_content(contexto.get_original_content())

    contexto.set_sanitized_content(content_tratado)
    imprimir('limpeza do conteudo finalizada')

def quebra_content_in_sentencas(contexto):
    pipe = Pipeline()
    pipe.set_texto(contexto.get_sanitized_content())

    oTexto = pipe.process()

    sentencas = oTexto.sentencas
    ranking   = oTexto.ranking

    sents = []
    for idx, sent in enumerate(sentencas):
        sentenca = Sentence(contexto.get_sanitized_content(), sent)
        sentenca.set_pontuacao(ranking[idx])
        sents.append(sentenca)
    
    contexto.set_sentences(sents)

def limite_maximo_sentencas(contexto):
    contexto.set_sentences(contexto.get_sentences()[:contexto.num_max_sentences])

def obtem_palavras_chaves(contexto):
    imprimir('iniciado checagem das palavras chave')
    for sent in contexto.get_sentences():
        # sent.set_palavras_chave(pln.get_palavras_chave(sent.get_original_text(), sent.get_sentence()))
        # sent.set_palavras_chave(pln.get_entidades_nomeadas(sent.get_sentence()))
        sent.set_palavras_chave(pln.get_palavras_chave_watson(sent.get_sentence()))
    imprimir('checagem das palavras chave finalizada')


def init():
    imprimir('iniciando')
    ctx = robo_state.load() 

    busca_conteudo_wikipedia(ctx)
    sanitize_wikipedia_content(ctx)
    quebra_content_in_sentencas(ctx)
    limite_maximo_sentencas(ctx)
    obtem_palavras_chaves(ctx)

    robo_state.save(ctx)    
    imprimir('finalizado')