import streamlit as st
import seaborn as sns
import plotly.express as px 
import plotly.graph_objects as go
import pandas as pd
from sshtunnel import SSHTunnelForwarder
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

st.title('Para onde ir na Estrada Real?')
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.image(('https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54'), width=60)
with col2:
    st.image(('https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white'), width=60)
with col3:
    st.image(('https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white'), width=60)
with col4:
    st.image(('https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white'), width=60)
with col5:
    st.image(('https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white'), width=60)
with col6:
    st.image(('https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white'), width=120)

   
db_server= '127.0.0.1'
user='tete'
db_port = '3306'
password = 'frida2202'
ip = 'localhost'
db_name = 'attitude'

try: 
    server = SSHTunnelForwarder(('138.197.99.33', 4242), ssh_username="tete", ssh_password="frida", remote_bind_address=('127.0.0.1', 3306))
    server.start()
    st.write('Tunnel opend :-P')
except:
    st.write('Failed opening the tunnel :-(')
port = str(server.local_bind_port)
conn_addr = ('mysql://' + user + ':' + password + '@' + db_server + ':' + port + '/' + db_name)
engine = create_engine(conn_addr)
connection = engine.connect()
st.write('Yeah! MySQL server connected using the SSH tunnel connection!')

nom = st.text_input ("Nom et prénom d'élève")
if nom == "":
    elevesdf = pd.read_sql_query("""select * from elevesdf""",conn_addr)
    st.write(elevesdf)
else:
    elevesdf_query = pd.read_sql_query(f"""select * from elevesdf where name = "{nom}" """ ,conn_addr)
    st.write(elevesdfquery)
try:
    birthday_today = pd.read_sql_query(f"""select name from elevesdf where birthday = CURRENT_DATE() """ ,conn_addr)
    if birthday_today != "":
        st.write(f"Aujourd'hui c'est l'anniversaire de {birthday_today}!")
except:
    pass







#coursdf22 = pd.read_sql_query("""select * from coursdf22 where schedule <> '0' and schedule2 <>'0' and schedule3<>'0'""",conn_addr)
#st.write(coursdf22)
#fig = px.bar(coursdf22, x='name', y=["schedule", "schedule2", "schedule3"],labels={'x':'Caminho', 'y':'Vocação Turística'})
#st.plotly_chart(fig)

classesdf22 = pd.read_sql_query("""select * from classesdf22""",conn_addr)
st.write(classesdf22)
fig = px.bar(classesdf22 ,labels={'x':'Caminho', 'y':'Vocação Turística'})
st.plotly_chart(fig)

paimentsdf22 = pd.read_sql_query("""select * from paimentsdf22""",conn_addr)

#wordcloud = WordCloud().generate(nuvem_de_palavras)
    #fig, ax = plt.subplots()
    #plt.imshow(wordcloud, interpolation='bilinear')
    #plt.axis("off")
    #plt.show()
    #st.pyplot(fig)

#fig = px.bar(cidades, x="cod_caminho", y=["ecoturismo", "cultural", "gastronomico", 'religioso'],labels={'x':'Caminho', 'y':'Vocação Turística'})
    #fig.update_xaxes(showticklabels=False)
    #fig.update_yaxes(showticklabels=False)
    #st.plotly_chart(fig)

##fig = px.scatter(roteiros, x="inicio", y='dificuldade_fisica',labels={'x':'Trechos', 'y':'Dificuldade Física'}, color = 'cod_caminho', size='distancia', hover_data=['inclinacao_media'])
        #fig.update_xaxes(showticklabels=False)
        #st.plotly_chart(fig)



def disconnect_mysql ():
    """Disconnect from MySQL server"""
    connection.close()  
    print('MySQL server is not connected anymore!')   
def shut_ssh_tunnel ():
    """Stop the SSH tunnel"""
    server.stop()
    print("You've stopped the SSH tunnel!")
