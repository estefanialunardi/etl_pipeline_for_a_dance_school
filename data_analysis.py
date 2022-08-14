import streamlit as st
import streamlit_authenticator as stauth
import plotly.express as px 
import plotly.graph_objects as go
import pandas as pd
from sshtunnel import SSHTunnelForwarder
import pymysql
pymysql.install_as_MySQLdb()
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
import os
import os.path
from dotenv import load_dotenv

st.title('Attitude Corps et Danses')
load_dotenv()


credentials = {
    "usernames":{
        st.secrets['data_user']:{
            "name":st.secrets['data_name'],
            "password":st.secrets['data_password']
            }
        }
    }

hashed_passwords = stauth.hasher(crdentials['usernames'][st.secrets['data_user']]['password']).generate() # Changed .Hasher to .hasher

authenticator = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=30)


name, authentication_status, username = authenticator.login('Login', 'main')
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.subheader(f'Coucou, {name}!')
    db_server = st.secrets["db_server"]
    user = st.secrets["user"]
    db_port = st.secrets["db_port"]
    password = st.secrets["password"]
    ip = st.secrets["ip"]
    db_name= st.secrets["db_name"]
    ip_ssh = st.secrets["ip_ssh"]
    ssh_username= st.secrets["ssh_username"]
    ssh_password= st.secrets["ssh_password"]
  

    #db_server= os.getenv('db_server')
    #user=os.getenv("user")
    #db_port=os.getenv("db_port")
    #password=os.getenv("password")
    #ip=os.getenv("ip")
    #db_name=os.getenv("db_name")
    #ip_ssh=os.getenv("ip_ssh")
    #ssh_username=os.getenv("ssh_username")
    #ssh_password=os.getenv("ssh_password")
    #remote_bind_address=os.getenv("remote_bind_address")
    try: 
        server = SSHTunnelForwarder((ip_ssh, 4242), ssh_username=ssh_username, ssh_password=ssh_password, remote_bind_address=(db_server, 3306))
        server.start()
    except:
        st.write('Failed opening the tunnel :-(')
    port = str(server.local_bind_port)
    conn_addr = ('mysql://' + user + ':' + password + '@' + db_server + ':' + port + '/' + db_name)
    engine = create_engine(conn_addr)
    connection = engine.connect()

    course_df = st.checkbox('Inscriptions for this year')
    if course_df:
        course_query = pd.read_sql_query(f"SELECT DISTINCT * FROM coursdf23" ,conn_addr)
        st.write(course_query)
    payments_df = st.checkbox('Payments for this year')
    if payments_df:
        payments_query = pd.read_sql_query(f"SELECT DISTINCT * FROM paimentsdf23" ,conn_addr)
        st.write(payments_query)

    st.title('Search for a student:')
    nom = st.text_input ("Nom et prénom d'élève")
    if nom == "":
        pass
    else:
        elevesdf_query = pd.read_sql_query(f"SELECT elevesdf.name, birthday, age, address, city, pcode, mail, telephone, legal_representative, course, schedule, course2, schedule2, course3, schedule3, registration, installments, total FROM elevesdf JOIN coursdf23 ON coursdf3.name=elevesdf.name JOIN paimentsdf23 ON elevesdf.name=paimentsdf23.name WHERE elevesdf.name LIKE '{nom}'" ,conn_addr)
        st.write(elevesdf_query)
        elevesdf = pd.read_sql_query("""select * from elevesdf""",conn_addr)
        st.title("Confirmer l'état du paiement")
        status = st.selectbox('Statut de paiement', options=["En attente", "Payé"])
        status_button = st.button("Confirmer l'état du paiement")
        if status_button:
            mySql_payment_status_query = f"""UPDATE paimentsdf23 set payment_status = '{status}' where `name` = '{nom}'"""
            engine.execute(mySql_payment_status_query)
        else:
            pass

    elevesdf = pd.read_sql_query("""select * from elevesdf""",conn_addr)
    st.title('Data Analysis')
    st.title('How old are the students?')
    st.write('The most prevalent age group is children. 40% of students are under 12 years old. Adolescents (13 to 17) represent 9% of those enrolled. Adults (from 18 to 62 years old) also account for 40% of the total. The other 10% are made up of elderly people up to 75 years old.')
    fig1 = px.histogram(elevesdf, x='age', nbins=20, title="Students by age groups")
    fig1.update_layout(bargap=0.2, xaxis1={'title': 'Age Group'}, yaxis1={'title': 'Students'})
    st.plotly_chart(fig1)

    st.write("""Although they are the proportionally most significant age group in the school, children are divided between the courses they most frequent. Children's classes have an average of 7 students per class(Éveil, Initiation and Préparatoire). Older children also participate in other courses, with teenagers mainly, such as the PBT, Classique 1 and Classique 2. Among the courses aimed at all age groups, the classes of Classique Moyen and Classique Intermediére are the most frequented.    """)
    courses_ages =pd.read_sql_query("""select c.name, c.course, e.age from course_filled as c join elevesdf as e on e.name = c.name""",conn_addr)
    fig3 = px.bar(courses_ages, x ='name', y=['course'], color = 'age', labels={'x':'Course', 'y':''}, title="Courses by age")
    fig3.update_layout(barmode='stack', xaxis1={'title': 'Courses'}, yaxis1={'title': ''})
    st.plotly_chart(fig3)

    st.write("""Most students take only one class - children in particular do not tend to take two different courses. Proportionally, the Pointes course is the one that most receives students who take more than one class.
    """)
    cours_cust = pd.read_sql_query(f"select coursdf23.name, nullif(course,'0') as course, nullif(course2, '0') as course2, nullif(course3, '0') as course3, total from paimentsdf23 join coursdf23 on coursdf23.name=paimentsdf23.name",conn_addr)
    fig = px.bar(cours_cust, x='total', y=['course','course2','course3'],  labels={'x':'Total', 'y':'Courses'}, title="Courses choosen as first, second or third choices")
    fig.update_layout(barmode='stack', xaxis1={'title': 'Courses'}, yaxis1={'range': [0, 30], 'title': ''})
    st.plotly_chart(fig)

    st.title('Where do they live?')
    fig2 = px.bar(elevesdf, x='name', y=['toulouse'], color='city', labels={'x':'Éleve', 'y':'Ville'}, title="Students by city")
    fig.update_layout(barmode='stack', xaxis1={'title': 'City'}, yaxis1={'title': 'Number of students'})
    st.plotly_chart(fig2)
    st.write("""90% of students live in Toulouse, the city where the school is based. In addition, it is possible to observe that most students live extremely close to the school, some even on the same block.""")
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

    st.write("""Students prefer to pay in one or three installments. Those who take three or more courses, in general, pay in one go. In terms of income, the biggest sums come from those who take one or three classes. Proportionally, the 3-lesson package is the most profitable for the school.""")
    paimentsdf23 = pd.read_sql_query("""select * from paimentsdf23""",conn_addr)
    fig = px.bar(paimentsdf23, x='name', y=['installments'],  color= 'total', labels={'x':'Installments', 'y':'Total'}, title="Total paid and number of installments")
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'array', 'categoryarray':['1', '2', '3', '4', '5', '10'], 'title': 'Number of Installments'}, yaxis1={'title': 'Number of students'})
    st.plotly_chart(fig)

    num_courses=[]
    for course in paimentsdf23['total']:
        if course == 500:
            num_courses.append('1')
        elif course == 720:
            num_courses.append('2')
        elif course == 880:
            num_courses.append('3')
        else:
            num_courses.append('10')

    fig = px.bar(paimentsdf23, x=num_courses, y='total', labels={'x':'Numero Cours', 'y':'Total'}, title="Income by number of classes package")
    fig.update_layout(barmode='stack', xaxis={'categoryorder': 'array', 'categoryarray':['1', '2', '3', '10'], 'title': 'Number of classes'},  yaxis1={'title': 'Income'})
    st.plotly_chart(fig)

    total_bill = paimentsdf23['total'].sum()
    st.title(f'In 2023, the regular students payment sumed {total_bill} Euros')

elif authentication_status == False:
    st.error("Nom d'utilisateur et mot de passe erronés")

elif authentication_status == None:
    st.warning("S'il vous plâit, insérer votre nom d'utilisateur et votre mot de passe")

def disconnect_mysql ():
    """Disconnect from MySQL server"""
    connection.close()  
def shut_ssh_tunnel ():
    """Stop the SSH tunnel"""
    server.stop()

