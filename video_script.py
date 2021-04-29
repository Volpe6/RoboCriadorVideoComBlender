import bpy
import os
from pathlib import Path
import json
import traceback

def existe_diretorio(caminho):
    return Path(caminho).exists()

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


def load():
    dirr = f'{os.getcwd()}/data.json'
    data = object()
    with open(dirr) as file:
        try:
            data = json.load(file)
        except Exception as ex:
            traceback.print_exc()
            print(f'nao foi possivel abrir o arquivo {dirr}')
    
    return load_json_object(data)

class Sentence:

    def __init__(self, text, sentence):
        #texto do qual a sentenca pertence
        self._original_text  = text
        self._sentence       = sentence
        self._palavras_chave = []
        self._image_url      = []
        self._pontuacao      = None
    
    def set_original_text(self, text):
        self._original_text = text
    
    def get_original_text(self):
        return self._original_text
    
    def set_sentence(self, sentence):
        self._sentence = sentence
    
    def get_sentence(self):
        return self._sentence
    
    def set_palavras_chave(self, palavras):
        self._palavras_chave = palavras
    
    def get_palavras_chave(self):
        return self._palavras_chave
    
    def set_image_url(self, url):
        self._image_url = url
    
    def get_image_url(self):
        return self._image_url
    
    def set_pontuacao(self, pontuacao):
        self._pontuacao = pontuacao
    
    def get_pontuacao(self):
        return self._pontuacao
    
    def to_string(self):
        attr = ''
        attr += f'Sentenca: {self._sentence},\n'
        attr += f'Palavras-chave: {self._palavras_chave},\n'
        attr += f'image-url: {self._image_url},\n'
        attr += f'Pontuação: {self._pontuacao}\n'
        return attr
        
class Contexto:

    def __init__(self,termo = None, prefix = None):
        self.num_max_sentences  = None 

        self._termo_busca       = termo
        self._prefix            = prefix
        self._original_content  = None
        self._sanitized_content = None
        self._dir_img           = None
        self._output_dir_video  = None
        self._sentences         = None 

    def set_output_dir_video(self, dirr):
        self._output_dir_video = dirr
    
    def get_output_dir_video(self):
        return self._output_dir_video

    def set_imgs_dir(self, dirr):
        self._dir_img = dirr
    
    def get_imgs_dir(self):
        return self._dir_img

    def set_termo_busca(self, s_termo):
        self._termo_busca = s_termo

    def get_termo_busca(self):
        return self._termo_busca

    def set_prefixo(self, prefix):
        '''
        prefixo utilizado no termo de busca
        '''
        self._prefix = prefix
    
    def get_prefixo(self):
        return self._prefix

    def set_original_content(self, content):
        '''
        conteudo original obtido da wiki
        '''
        self._original_content = content
    
    def get_original_content(self):
        return self._original_content
    
    def set_sanitized_content(self, content):
        '''
        conteudo da wiki sanitizado
        '''
        self._sanitized_content = content

    def get_sanitized_content(self):
        return self._sanitized_content

    def set_sentences(self, sentences):
        self._sentences = sentences
    
    def get_sentences(self):
        return self._sentences
    
    def get_full_termo_busca(self):
        return f'{self.get_prefixo()} {self.get_termo_busca()}'

    def to_string(self):
        attr = ''
        attr += f'Termo de Busca: {self._termo_busca} \n'
        attr += f'Prefixo: {self._prefix} \n'
        return attr

class Video:
    
    def __init__(self):
        self.area_ui       = None
        self.current_frame = 1
        self.dir           = "C:/Users/Drew/Documents/python/botCriadorVideo/assets/img/"
        self.sequencer     = bpy.ops.sequencer
        self.C             = bpy.context
        self.C.scene.render.image_settings.file_format = 'FFMPEG'
        self.C.scene.render.ffmpeg.format = 'MKV'
        
    def set_video_render_output_file(self, dirr):
        bpy.data.scenes['Scene'].render.filepath = dirr

    def get_area_sequencer(self):
        if self.area_ui is None:
            for window in bpy.context.window_manager.windows:
                screen = window.screen
                for sc_area in screen.areas:
                    if sc_area.ui_type == 'SEQUENCE_EDITOR':
                        #voce pode sovreescrever o contexto e passar como parametro posicional
                        self.area_ui = sc_area
                        break
        return self.area_ui
    
    def set_end_frame_video(self, fr):
        bpy.data.scenes['Scene'].frame_end = fr
    
    def add_texto_inicial(self, texto):
        area = self.get_area_sequencer()
        #voce pode sovreescrever o contexto e passar como parametro posicional
        override = {"area":area}
        print(area.ui_type)
        fr_ini = self.current_frame
        fr_fim = self.current_frame + 10
        self.current_frame += 10  
        self.sequencer.effect_strip_add(override, frame_start=fr_ini, frame_end=fr_fim, channel=2, type='COLOR')
        self.sequencer.effect_strip_add(override, frame_start=fr_ini, frame_end=fr_fim, channel=2, type='TEXT')
        self.C.scene.sequence_editor.sequences_all["Text"].text = texto
        self.C.scene.sequence_editor.sequences_all["Text"].font_size = 150
        self.C.scene.sequence_editor.sequences_all["Text"].location[1] = 0.4
        
    def add_images_senquencer(self, img, fr_ini, fr_fim):
        area = self.get_area_sequencer()
        override = {"area":area}
        self.sequencer.image_strip_add(override, directory=self.dir, files=[{"name": img}], frame_start=fr_ini, frame_end=fr_fim, channel=2)
    
    
    def add_images_sentence_senquencer(self, indice):
        file_img_name  = f'{indice}-converted.png'
        file_sent_name = f'{indice}-sentence.png'
        
        fr_ini = self.current_frame
        fr_fim = self.current_frame + 23
        self.current_frame += 24  
        self.add_images_senquencer(file_img_name, fr_ini, fr_fim)
        self.add_images_senquencer(file_sent_name, fr_ini, fr_fim)
        self.set_end_frame_video(self.current_frame)
    
    def render(self):
        bpy.ops.render.render(animation=True, use_viewport=False)


contexto = load()
video = Video()

video.dir = contexto.get_imgs_dir()
video.set_video_render_output_file(contexto.get_output_dir_video())


video.add_texto_inicial(contexto.get_termo_busca())

for i, sent in enumerate(contexto.get_sentences()):
    if not existe_diretorio(f'{os.getcwd()}/assets/img/{i}-converted.png'):
        print(f'corrompido:{i}-converted.png')
        continue
    video.add_images_sentence_senquencer(i)

video.render()
bpy.ops.wm.window_close()
#for window in bpy.context.window_manager.windows:
#    screen = window.screen
#    for area in screen.areas:
#        if area.ui_type == 'SEQUENCE_EDITOR':
#            #voce pode sovreescrever o contexto e passar como parametro posicional
#            override = {"area":area}
#           #adiciona a imagem na time line
#            bpy.ops.sequencer.image_strip_add(override, directory="C:/Users/Drew/Documents/python/botCriadorVideo/assets/img/", files=[{"name":"1-converted.png", "name":"1-converted.png"}], frame_start=1, frame_end=26, channel=2)
#            break
