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
