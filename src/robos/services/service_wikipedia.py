import wikipedia as wiki
#quando executar esse arquivo diretamente discomente essa linha
#from estrutura_dados import Page, Resumo 
from robos.services.estrutura_dados import Page, Resumo #quando executado de outro pacote descomente essa linha

wiki.set_lang("pt")

def page(termo):
    page = wiki.page(termo)
    return Page(page.title, page.content, page.url)

def resumo(termo):
    return Resumo(wiki.summary(termo) )
