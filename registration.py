import streamlit as st
import pandas as pd
import re
import os, os.path
from dateutil import parser
from sshtunnel import SSHTunnelForwarder
import sqlalchemy as db
from sqlalchemy import create_engine

st.image(('passaporte-estrada-real (11).jpg'))

st.title('Para onde ir na Estrada Real?')
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    st.image(('https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54'), width=60)
with col2:
    st.image(('https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white'), width=60)
with col3:
    st.image(('https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white'), width=60)
with col4:
    st.image(('https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=whitehttps://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white'), width=60)
with col5:
    st.image(('https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white'), width=60)
with col6:
    st.image(('https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white'), width=60)
with col7:
    st.image(('https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white'), width=120)
        
st.image(('passaporte-estrada-real (11).jpg'))
st.write('''Com mais de 1600km de extensão total, a Estrada Real é a maior rota turística do Brasil. São 245 municípios dos estados de Minas Gerais, Rio de Janeiro e São Paulo, por onde passavam os percursos delegados pela Coroa Portuguesa para o transporte de ouro e diamantes mineiros até os portos cariocas. Esses trajetos foram divididos em quatro trilhas oficiais: Caminho Velho, Caminho Novo, Caminho dos Diamantes e Caminho do Sabarabuçu. Hoje, esses roteiros são destinos polivalentes com características múltiplas, com opções de turismo cultural, religioso, gastronômico e ecoturismo.

Para escolher os destinos, dentre as centenas de opções da Estrada, é fundamental alinhar as preferências de viagem e perfil do turista, tempo disponível e meio de locomoção com a vocação turística de cada município e com as características específicas dos trajetos a serem percorridos.

Este projeto busca trazer informações dos percursos e municípios da Estrada Real, favorecendo a escolha racional dos destinos de viagem, bem como dos melhores trechos a serem percorridos com diferentes opções de locomoção, a partir dos objetivos do turista. ''')

caminhos = pd.read_csv('./data/caminhos.csv')
cidades = pd.read_csv('./data/cidades.csv')
pontos_turisticos = pd.read_csv('./data/pontos_turisticos.csv')
roteiros = pd.read_csv('./data/roteiros.csv')
hoteis_pet_friendly = pd.read_csv('./data/hoteis_pet_friendly.csv')
micro_mesorregioes_mg = pd.read_csv('./data/micro_mesorregioes_mg.csv')
micro_municipios_mg = pd.read_csv('./data/micro_municipios_mg.csv')


st.sidebar.markdown('#### Escolha seu destino')
cam_dia=0
cam_nov=0
cam_vel=0
cam_sab=0
todos_cam=0
duracao = st.sidebar.slider('Qual a duração da sua viagem?', min_value=2, max_value=30)
if duracao < 2:
    cam_dia+=6
    cam_nov+=4
    cam_vel+=2
    cam_sab+=12
elif duracao < 4:
    cam_dia+=8
    cam_nov+=4
    cam_vel+=4
    cam_sab+=4
elif duracao < 6:
    cam_dia+=6
    cam_nov+=8
    cam_vel+=6
    cam_sab+=2
else:
    cam_dia+=4
    cam_nov+=6
    cam_vel+=8
    cam_sab+=2
transporte = st.sidebar.selectbox('Qual o meio de transporte?', ('Carro', 'Ônibus','Moto','Cavalo','Bicicleta','A pé'))
if transporte == 'Carro' or transporte == 'Ônibus'or transporte == 'Moto':
    pass
elif transporte == 'Cavalo' or transporte == 'Bicicleta':
    dificuldade_bike = st.sidebar.slider ('Qual grau de dificuldade de trilhas você busca?', min_value=1, max_value=5)
    if dificuldade_bike <2:
        cam_dia+=3
        cam_nov+=1
        cam_vel+=2
        cam_sab+=1
    elif dificuldade_bike <3:
        cam_dia+=2
        cam_nov+=1
        cam_vel+=2
        cam_sab+=1
    elif dificuldade_bike <4:
        cam_dia+=1
        cam_nov+=3
        cam_vel+=2
        cam_sab+=3
    else:
        cam_dia+=1
        cam_nov+=4
        cam_vel+=2
        cam_sab+=4
elif transporte == 'A pé':
    dificuldade_pe = st.sidebar.slider ('Qual grau de dificuldade de trilhas você busca?', min_value=1, max_value=5)
    if dificuldade_pe <2:
        cam_dia+=2
        cam_nov+=1
        cam_vel+=3
        cam_sab+=2
    elif dificuldade_pe <3:
        cam_dia+=2
        cam_nov+=1
        cam_vel+=2
        cam_sab+=2
    elif dificuldade_pe <4:
        cam_dia+=3
        cam_nov+=4
        cam_vel+=2
        cam_sab+=3
    else:
        cam_dia+=3
        cam_nov+=4
        cam_vel+=1
        cam_sab+=3
turismo = st.sidebar.multiselect('Que atrações você deseja?', ('Ecoturismo e Turismo de Aventura','Turismo Cultural e Histórico', 'Turismo Gastronômico', 'Turismo Religioso'))
if 'Ecoturismo e Turismo de Aventura' in turismo:
    cam_dia+=2
    cam_nov+=2
    cam_vel+=3
    cam_sab+=1
if 'Turismo Cultural e Histórico' in turismo:
    cam_dia+=3
    cam_nov+=4
    cam_vel+=1
    cam_sab+=2
if 'Turismo Gastronômico' in turismo:
    cam_dia+=2
    cam_nov+=3
    cam_vel+=4
    cam_sab+=1
if 'Turismo Religioso' in turismo:
    cam_dia+=4
    cam_nov+=2
    cam_vel+=3
    cam_sab+=2
pets = st.sidebar.radio(
     "Precisa de hospedagem para pets?",
     ('Sim', 'Não'))
if pets == "Sim":
    cam_dia+=1
    cam_nov+=2
    cam_vel+=4
    cam_sab+=4
else:
    pass
if cam_dia > cam_nov and cam_dia > cam_vel and cam_dia > cam_sab:
    st.sidebar.info('Considere conhecer o Caminho dos Diamantes')
elif cam_dia < cam_nov and cam_nov > cam_vel and cam_nov > cam_sab:
    st.sidebar.info('Considere conhecer o Caminho Novo')
elif cam_dia < cam_sab and cam_sab > cam_vel and cam_nov < cam_sab:
    st.sidebar.info('Considere conhecer o Caminho Sabarabuçu')
elif cam_dia < cam_vel and cam_sab < cam_vel and cam_nov < cam_vel:
    st.sidebar.info('Considere conhecer o Caminho Velho')
else:
    st.sidebar.info('Que tal conhecer todos os roteiros?')



st.markdown('## ETL')
cola, colb, colc = st.columns(3)
with cola:
    checkbox_bibliotecas = st.checkbox('Bibliotecas utilizadas')
if checkbox_bibliotecas:
    st.markdown('### Bibliotecas utilizadas:')
    st.markdown(''' 
        - Beautifulsoup4
        - Requests
        - Pandas
        - Lxml
        - Selenium 
        - Time
        - SQLAlchemy
        - Pymysql
        - Streamlit ''')
with colb:
    checkbox_metodos = st.checkbox('Métodos')
if checkbox_metodos:
    st.markdown('#### Métodos')
    st.markdown('''         __* Extração: *__

        Para a extração dos dados da internet, foram utilizadas métodos de web scraping para coletar dados-chave sobre os destinos da Estrada Real. 

        As tabelas com informações regionais (tabela_micro_meso_mg etabelas_micro_municipio_mg) foram extraídas de duas tabelas em página única da Wikipedia, utilizando a biblioteca Beautiful Soup.

        Para extrair os dados do site do Instituto Estrada Real foram criadas rotinas para navegação automatizada com a biblioteca Selenium de diversas páginas diferentes do site. Como o site utiliza o mesmo formato de página para informações da mesma natureza, foi possível aplicar funções para extrair os dados sobre diferentes destinos.

        Foram utilizados três modelos de página do site do Instituto para criar quatro tabelas. A tabela "caminhos" foi criada a partir da página com informações específicas do caminho, que além das informações gerais dessa trilha (como início, fim e distância), possibilitou extrair uma lista de links para páginas com informações de cada município parte do destino, como número de habitantes e vocação turística (de onde foram retirados os dados da tabela "cidades". Dessas mesmas páginas com dados sobre as cidades, foi gerado um dicionário com todas as atrações turísticas da Estrada Real, por município - que foi convertido na tabela "pontos_turisticos". Finalmente, para a tabela "roteiros" foram utilizadas os dados específicos de cada trecho, nas páginas com Roteiros Planilhados.
        Finalmente, para extração das informações sobre hoteis que aceitem animais nos destinos da Estrada Real, foi necessário desabilitar o JavaScript para possibilitar a navegação automatizada. Com isso, todos os filtros de pesquisa (que normalmente são selecionados por objetos dinâmicos/interativos) precisaram ser definidos a priori, para armazenamento das preferências de pesquisa ainda no endereço URL, alterando apenas o nome do município no campo específico do caminho HTML a partir de iteração da tabela de cidade. 

        __* Transformação: *__

        De maneira geral, os dados foram extraídos de forma objetiva e com bastante qualidade, já com a preocupação de extrair o dado no formato mais provavelmente adequado para a análise, sem qualquer valor nulo e com pouquíssima necessidade de limpeza. Pontualmente, foi utilizada o método .loc seguido do ".replace()" para correção de pequenas incorreções, erros de digitação ou informações desviantes (por diferenças na padronização da alimentação de alguns dados nos sites fonte). Para facilitar a leitura e trabalho com os dados, foram utilizados métodos de padronização de valores em massa(.lower(), .strip(), .replace(), etc.). 

        __* Carregamento: *__

        Todos os dados foram carregados e armazenados em uma database no MySQL, utilizando as bibliotecas SQLAlchemy e Pymysql para conexão com a ferramenta de banco de dados e da biblioteca Pandas para envio das tabelas ("pandas.DataFrame.to_sql").
        
        __* Apresentação: *__

        O conteúdo, de texto e de dados, foi preparado no Visual Studio Code, com código em Python puro para ser apresentado em uma aplicação Web utilizando a biblioteca Streamlit. Além da análise dos dados, o usuário tem acesso a todas as informações de bibliotecas e métodos utilizados nesse projeto.

        __* Sistema de recomendações: *__
        
        Foi desenvolvido um sistema de recomendações de viagem com filtragem baseada na preferência e perfil de viagem do usuário. Ele considera o tempo, meio de locomoção, preferências de destino turístico e a necessidade de acomodar pets. 
        ''')

with colc:
    checkbox_dados = st.checkbox('Dados extraídos')
if checkbox_dados:
    dados = st.multiselect('Quais dados você gostaria de acessar?',
    ['Todos os Dados Disponíveis', 'Dados dos Caminhos','Dados das Cidades','Dados dos Roteiros', 'Dados dos Pontos Turísticos', 'Dados dos Hoteis Pet Friendly', 'Dados das Mesorregiões de MG', 'Dados das Microrregiões de MG'])
try: 
    if 'Todos os Dados Disponíveis' in dados:
        st.write(caminhos)
        st.write(cidades)
        st.write(roteiros)
        st.write(pontos_turisticos)
        st.write(hoteis_pet_friendly)
        st.write(micro_mesorregioes_mg)
        st.write(micro_municipios_mg)
except:
    pass
try: 
    if 'Dados dos Caminhos' in dados:
        st.write(caminhos)
except:
    pass
try: 
    if 'Dados das Cidades' in dados:
        st.write(cidades)
except:
    pass
try: 
    if 'Dados dos Roteiros' in dados:
        st.write(roteiros)
except:
    pass
try: 
    if 'Dados dos Pontos Turísticos' in dados:
        st.write(pontos_turisticos)
except:
    pass
try: 
    if 'Dados dos Hoteis Pet Friendly' in dados:
        st.write(hoteis_pet_friendly)
except:
    pass
try: 
    if 'Dados das Mesorregiões de MG' in dados:
     st.write(micro_mesorregioes_mg)
except:
    pass
try: 
    if 'Dados das Microrregiões de MG' in dados:
        st.write(micro_municipios_mg)
except:
    pass


st.markdown('## Análise dos dados')
with st.expander("Veja a análise"):



