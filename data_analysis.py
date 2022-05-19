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
from datetime import datetime, date


st.title('Data Analysis?')
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

courses = pd.read_sql_query("""SELECT name, course from coursdf22 union all select name, course2 from coursdf22 union all select name, course3 from coursdf22""",conn_addr)
courses_filled=[]
name_filled=[]
for row in range(len(courses['course'])):
    if courses['course'].iloc[row] !='0' and courses['course'].iloc[row]  != "":
        courses_filled.append(courses['course'].iloc[row])
        name_filled.append(courses['name'].iloc[row])
course_filled = pd.DataFrame(zip(courses_filled, name_filled))
st.write(course_filled)
course_filled.to_csv('toutescours22.csv')

#fig3 = px.bar(classes_age, x =['course', 'course2','course3'], y='name', color = 'age')
#st.plotly_chart(fig3)




st.title('How old are they?')
st.write('All students')
fig1 = px.histogram(elevesdf, x='age', nbins=20)
fig1.update_layout(bargap=0.2)
st.plotly_chart(fig1)

st.title('Where do they live?')
fig2 = px.bar(elevesdf, x='name', y=['toulouse'], color='city', labels={'x':'Éleve', 'y':'Ville'})
st.plotly_chart(fig2)
cola, colb = st.columns(2)
with cola:
    st.write('XXXXXX')
with colb:
    mapbox_access_token ="pk.eyJ1IjoidGV0ZW1lc3F1aXRhIiwiYSI6ImNsM2J5N2dlZzAybmEzZG11NGRrNnZjazgifQ.Knpx0Cs7nDR7zY9aPA55Bg"
    fig = go.Figure(go.Scattermapbox(
            lat=elevesdf['lat'],
            lon=elevesdf['long'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=9
            ),
            text=elevesdf['name'],
        ))
    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=43.591001956445716, 
                lon=1.454922592057386),
            pitch=0,
            zoom=10),)
    st.plotly_chart(fig)






#st.write(course_age)

#y_cours = coursdf22[coursdf22['schedule']]
#fig = px.bar(coursdf22, x='course', y=y_cours, labels={'x':'Caminho', 'y':'Vocação Turística'})
#st.plotly_chart(fig)

classesdf22 = pd.read_sql_query("""select * from classesdf22""",conn_addr)
st.write(classesdf22)
#fig = px.histogram(classesdf22, x=('initiation', 'contemporain', 'carte_10_cours','preparatoire','barre_a_terre',
# 'classique_avance','classique_2','eveil','pbt','pointes','pilates','moderne','pbt_ballet_fitness', 'classique_1','classique_interm_avance','classique_moyen'))
#fig.update_layout(bargap=0.2)
#st.plotly_chart(fig)


#paimentsdf22 = pd.read_sql_query("""select * from paimentsdf22""",conn_addr)
#st.write(paimentsdf22.columns)
#paiments_installments
#fig = px.bar(paimentsdf22, x='installments', y='count', color= 'total', labels={'x':'Installments', 'y':'Total'})
#st.plotly_chart(fig)
#connection.close() 
#server.stop()

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
