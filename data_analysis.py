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

   
db_server= '127.0.0.1'
user='tete'
db_port = '3306'
password = 'frida2202'
ip = 'localhost'
db_name = 'attitude'

try: 
    server = SSHTunnelForwarder(('138.197.99.33', 4242), ssh_username="tete", ssh_password="frida", remote_bind_address=('127.0.0.1', 3306))
    server.start()
except:
    st.write('Failed opening the tunnel :-(')
port = str(server.local_bind_port)
conn_addr = ('mysql://' + user + ':' + password + '@' + db_server + ':' + port + '/' + db_name)
engine = create_engine(conn_addr)
connection = engine.connect()

st.title('Search for a student:')
nom = st.text_input ("Nom et prénom d'élève")
if nom == "":
    pass
else:

    elevesdf_query = pd.read_sql_query(f"select elevesdf.name, birthday, age, address, city, toulouse, pcode, mail, telephone, legal_representative, course, schedule, course2, schedule2, course3, schedule3, registration, installments, total from elevesdf join coursdf22 on coursdf22.name=elevesdf.name join paimentsdf22 on elevesdf.name=paimentsdf22.name where elevesdf.name = '{nom}'" ,conn_addr)
    st.write(elevesdf_query)

elevesdf = pd.read_sql_query("""select * from elevesdf""",conn_addr)

st.title('How old are the students?')
st.write('All students')
fig1 = px.histogram(elevesdf, x='age', nbins=20)
fig1.update_layout(bargap=0.2)
st.plotly_chart(fig1)

courses_ages =pd.read_sql_query("""select c.name, c.course, e.age from course_filled as c join elevesdf as e on e.name = c.name""",conn_addr)
fig3 = px.bar(courses_ages, x ='name', y=['course'], color = 'age', labels={'x':'Course', 'y':''})
st.plotly_chart(fig3)

st.title('Where do they live?')
fig2 = px.bar(elevesdf, x='name', y=['toulouse'], color='city', labels={'x':'Éleve', 'y':'Ville'})
st.plotly_chart(fig2)

mapbox_access_token ="pk.eyJ1IjoidGV0ZW1lc3F1aXRhIiwiYSI6ImNsM2J5N2dlZzAybmEzZG11NGRrNnZjazgifQ.Knpx0Cs7nDR7zY9aPA55Bg"
px.set_mapbox_access_token(mapbox_access_token)
place = [nom for nom in elevesdf.name]
lattd = [lati for lati in elevesdf.lat]
longi = [lon for lon in elevesdf.long]
lattd.append(43.591001956445716)
longi.append(1.454922592057386)
place.append('École')
ecole = []
for i in lattd:
    if i == 43.591001956445716:
        ecole.append(15)
    else:
        ecole.append(1)

fig = px.scatter_mapbox(lat=lattd, lon=longi, color=place, size=ecole, color_continuous_scale=px.colors.sequential.Inferno, size_max=15, zoom=10)
fig.update_layout(autosize=True,hovermode='closest',showlegend =False,mapbox=dict(accesstoken=mapbox_access_token,bearing=0,center=dict(lat=43.591001956445716, lon=1.454922592057386),pitch=0,zoom=10),)
st.plotly_chart(fig)



cours_cust = pd.read_sql_query(f"select coursdf22.name, course, schedule, course2, schedule2, course3, schedule3, total, CASE WHEN course2 = 0 THEN NULL ELSE course2 END, CASE WHEN course3 = 0 THEN NULL ELSE course3 END from paimentsdf22 join coursdf22 on coursdf22.name=paimentsdf22.name",conn_addr)

fig = go.Figure(go.Bar(cours_cust, x='total', y=['course','course2','course3'],  labels={'x':'Course', 'y':'Total'}))

st.plotly_chart(fig)

paimentsdf22 = pd.read_sql_query("""select * from paimentsdf22""",conn_addr)
fig = px.bar(paimentsdf22, x='name', y=['installments'],  color= 'total', labels={'x':'Installments', 'y':'Total'})
fig.update_layout(barmode='stack', xaxis={'categoryorder':'array', 'categoryarray':['1', '2', '3', '4', '5', '10']})
st.plotly_chart(fig)

num_courses=[]
for course in paimentsdf22['total']:
    if course == 500:
        num_courses.append('1')
    elif course == 720:
        num_courses.append('2')
    elif course == 880:
        num_courses.append('3')
    else:
        num_courses.append('10')

fig = px.bar(paimentsdf22, x=num_courses, y='total', labels={'x':'Numero Cours', 'y':'Total'})
fig.update_layout(barmode='stack', xaxis={'categoryorder': 'array', 'categoryarray':['1', '2', '3', '10']})
st.plotly_chart(fig)



total_bill = paimentsdf22['total'].sum()
st.write(f'Total 2022 = {total_bill}')

#connection.close() 
#server.stop()

#wordcloud = WordCloud().generate(nuvem_de_palavras)
    #fig, ax = plt.subplots()
    #plt.imshow(wordcloud, interpolation='bilinear')
    #plt.axis("off")
    #plt.show()
    #st.pyplot(fig)


def disconnect_mysql ():
    """Disconnect from MySQL server"""
    connection.close()  
    print('MySQL server is not connected anymore!')   
def shut_ssh_tunnel ():
    """Stop the SSH tunnel"""
    server.stop()
    print("You've stopped the SSH tunnel!")
