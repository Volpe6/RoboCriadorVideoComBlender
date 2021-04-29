from robos import robo_state
from util.gerencia_arquivo import GerenciaArquivo as ga

from wand.image import Image
from wand.display import display
from wand.color import Color
from wand.font import Font

import os
import subprocess 
import traceback

indice_img_corrompidas = []


def imprimir(msg):
    print(f'Robo video > {msg}')

def remove_img_corrompidas():
    for i in indice_img_corrompidas:
        if not ga.existe_diretorio(f'./assets/img/{i}-original.png'):
            return
        ga.remove(f'./assets/img/{i}-original.png')

def convert_all_imagens(contexto):
    for i, sent in enumerate(contexto.get_sentences()):
        try:
            convert_image(i)
        except:
            print(f'nao foi possivel converter a imagem:"./assets/img/{i}-original.png"')
            traceback.print_exc()
            indice_img_corrompidas.append(i)

def convert_image(idx_sentence):
    #doc: https://buildmedia.readthedocs.org/media/pdf/wand/latest/wand.pdf
    original_file = f'./assets/img/{idx_sentence}-original.png[0]'#o comando no final é para q caso seja um gif, pegue a primeira imagem
    
    if not ga.existe_diretorio(f'./assets/img/{idx_sentence}-original.png'):
        raise Exception('o arquivo que esta tentando acessar nao existe')
    
    output_file   = f'./assets/img/{idx_sentence}-converted.png'

    width  = 1920
    height = 1080
    with Image(filename=original_file) as img:
        with img.clone() as img_clone:
            img_clone.blur(radius=0, sigma=20)
            img_clone.resize(int(width), int(height))
            with img.clone() as img_clone2:
                img_clone.resize(int(width), int(height))
                img_clone.composite(img_clone2, operator='over', gravity='center')
            img_clone.extent(int(width), int(height))
            img_clone.save(filename=output_file)

def create_all_sentences_images(contexto):
    for i, sent in enumerate(contexto.get_sentences()):
        create_sentence_image(i, sent.get_sentence())

def create_thumbnail(contexto):
    file = {}
    for i in range(len(contexto.get_sentences())):
        if ga.existe_diretorio(f'./assets/img/{i}-original.png'):
            file['indice'] = i
            file['name']   = f'./assets/img/{i}-original.png'
            break
    
    with Image(filename=file['name']) as img:
        with img.clone() as img_clone:
            img_clone.save(filename='./assets/img/{}-thumbnail.jpg'.format(file['indice']))
            

def create_sentence_image(idx_sentence, text):
    if not ga.existe_diretorio(f'./assets/img/{idx_sentence}-original.png'):
        print(f'"./assets/img/{idx_sentence}-original.png" nao foi encontrado')
        return 
    
    output_file = f'./assets/img/{idx_sentence}-sentence.png'

    template_conf = {
        '0': {
            'width': 1920,
            'height': 400,
            'gravity': 'center'
        },
        '1': {
            'width': 1920,
            'height': 1080,
            'gravity': 'center'
        },
        '2': {
            'width': 800,
            'height': 1080,
            'gravity': 'west'
        },
        '3': {
            'width': 1920,
            'height': 400,
            'gravity': 'center'
        },
        '4': {
            'width': 1920,
            'height': 1080,
            'gravity': 'center'
        },
        '5': {
            'width': 800,
            'height': 1080,
            'gravity': 'west'
        },
        '6': {
            'width': 1920,
            'height': 400,
            'gravity': 'center'
        }
    }
    current_sent = template_conf[str(idx_sentence)]
    with Image(width=current_sent['width'], height=current_sent['height']) as img:
        img.gravity          = current_sent['gravity']
        img.background_color = Color('transparent')
        img.text_kerning     = -1
        img.caption(text,font=Font(path='./assets/font/Roboto-Regular.ttf', color=Color('white')))
        img.save(filename=output_file)

def render_video_blender():
    if not ga.existe_diretorio('./assets/video'):
        ga.cria_diretorio('./assets/video')

    template_path     = f'{os.getcwd()}/video_template.blend'
    video_script_path = f'{os.getcwd()}/video_script.py'
    blender_path = '{}/blender'.format(get_blender_path())
    # subprocess.run(['blender', template_path, '--python', video_script_path])
    subprocess.run([blender_path, template_path, '--background', '--python', video_script_path])
    # subprocess.run([blender_path, template_path, '--python', video_script_path])


def get_blender_path():
    paths = os.environ['PATH'].split(";")
    for path in paths:
        if 'blender' in path.lower():
            return path
    
def define_dirs(contexto):
    current_dir = os.getcwd()
    imgs_dir    = f'{current_dir}/assets/img/'
    output_dir_video = f'{current_dir}/assets/video/'

    contexto.set_output_dir_video(output_dir_video)
    contexto.set_imgs_dir(imgs_dir)
    robo_state.save(contexto)

def init():
    imprimir('iniciando')
    ctx = robo_state.load()
    define_dirs(ctx)
    imprimir('convertendo imagens')
    convert_all_imagens(ctx)
    imprimir('removendo imagens corrompidas')
    remove_img_corrompidas()
    imprimir('criando as sentencas para as imgs')
    create_all_sentences_images(ctx)
    # create_thumbnail(ctx)
    imprimir('renderizando o video')
    render_video_blender()
    imprimir('finalizado')
