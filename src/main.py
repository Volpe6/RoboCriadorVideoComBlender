from model import Contexto, Sentence
from robos import robo_input, robo_texto, robo_state, robo_imagem, robo_video
from util.gerencia_arquivo import GerenciaArquivo as ga

def main():
    ctx = Contexto()
    ctx.num_max_sentences = 7
   
    if ga.existe_diretorio('./assets/img'):
        ga.apaga_arquivos_dir('./assets/img')

    robo_input.init(ctx)
    robo_texto.init()
    robo_imagem.init()
    robo_video.init()

    print('programa finalizado')
   
main()