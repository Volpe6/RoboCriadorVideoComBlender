# Robô criador de video com Python e Blender

Um robô que com base em termo de busca informado pelo usuário faz um vídeo. Esse projeto é um protótipo.

O robo foi feito utilizando como referência os video do Filipe Deschamps: <https://www.youtube.com/watch?v=kjhu1LEmRpY&list=PLMdYygf53DP4YTVeu0JxVnWq01uXrLwHi>.

![](/video_gif.gif)

## Pré requisitos

* conta no Google Cloud <https://cloud.google.com/>
* conta na IBM Cloud <https://cloud.ibm.com/login>

### Google Cloud

Uma vez com a conta na Google Cloud criada, deve-se criar um novo projeto no Google Cloud. Com o projeto criado procure pela biblioteca do Google Cloud e nela procure pela **Custom Search API** e ativia. Com o **Custom Search API** ativado, crie credenciais para poder usa-lo, ao final dessa etapa será obtido uma API KEY, que deve ser usada no projeto no arquivo ".env".

Com as etapas anteriores finalizadas, deve-se criar um custom search engine e obter seu id, que deve ser colocado no arquivo ".env". Link com os primeiros passos do search engine: <https://programmablesearchengine.google.com/about/>.

### IBM Cloud

Uma vez com a conta na IBM Cloud criada, vá até o catálogo e procure por **Natural Language Understanding**. Uma vez lá, crie um projeto, com o projeto criado obtenha a API KEY, e coloque no ".env", também deverá por a url da aplicação.

## Requisitos

* Blender - 2.81
* ImageMagick

Blender e ImageMagick, devem estar instalados em seu computador

### ImageMagick

Para a utilização do ImageMagick em conjunto com o Python foi utilizado o **Wand**. A documentação do **Wand** pode ser visualizada aqui: <https://buildmedia.readthedocs.org/media/pdf/wand/latest/wand.pdf>.


