import streamlit as st
import pandas as pd
import re
import datetime
from dateutil import parser
from geopy.geocoders import Nominatim 
from sshtunnel import SSHTunnelForwarder
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import pymysql
from dotenv import load_dotenv
pymysql.install_as_MySQLdb()
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib,ssl
import base64
import sqlite3
import pathlib
import uuid 
from contextlib import contextmanager
from pathlib import Path
import os
import os.path

st.set_page_config(page_title='Attitude Corps et Danses | Inscrivez-vous', page_icon=('logo.png'), layout="centered", initial_sidebar_state="auto", menu_items=None)

st.markdown(
    """
    <style>
    .body {
    color: #662d91;
    background-color: #e0d2e0;
    /* font-size: 40px; */
}

.stButton>button{
    color: #662d91;
    backgroud-color: #e0d2e0;
    justify-content: center
    box-sizing: 5%;
    height: 3em;
    width: 17em;
    font-size:20px;
    border: 2px solid;
    border-radius: 5px;
    padding: 30px;
}

.stTextInput>div>div>input {
    color: #000000;
}

.fullScreenFrame > div {
    display: flex;
    justify-content: center;
}

.center {
    display: block;
    margin-left: auto;
    margin-right: auto;
  }
    </style>
    """,
    unsafe_allow_html=True


)
primaryColor="#662d91"
backgroundColor="e0d2e0"
secondaryBackgroundColor="#c9aec4"
textColor="#262730"
font="sans serif"

st.image(('registration.jpg'))

st.subheader("""Bienvenue à Attitude Corps et Danses.""")

st.write("""Veuillez sélectionner réserver un cours pour programmer vos cours de Pilates. Pour vous inscrire, sélectionnez inscrivez-vous. Rendez-vous en classe !""")

col1, col2 = st.columns(2)
with col1:
    pilates = st.button("📆 Réservez un cours")

if pilates:
    components.iframe(f"https://calendar.google.com/calendar/u/0/appointments/schedules/AcZssZ1ZK_mrOF6kydTE4tev8pM3GCg95bcCC0DxyIIw67z_Hk3CF5NNPXObP6TFHcm6VaiOwzT8HxDm", width=1200, height=800, scrolling=True)

with col2:
    inscrivez = st.button('Inscrivez-vous 👈')
if inscrivez:
    def course_choice (cours):
        """Student may choose its courses and better schedule"""
        cours_info =[]
        courses_qtd = 0
        
        if cours== 'Carte de 10 cours':
                carte_10_cours = st.multiselect('Cours', ['Sélectionnez vos cours', 'Classique 1','Classique 2','Classique Moyen','Classique Interm. – Avancé','Classique Avancé','Pointes','Éveil','Préparatoire','Moderne','Contemporain','Barre à Terre','PBT + Ballet Fitness','PBT','Pilates'])
                courses_qtd +=4
        else:
            pass
        if cours== 'Classique 1':
            heure= st.multiselect('Horaire', ['Mercredi 14h15-15h30', 'Je voudrais un autre horaire'])
            courses_qtd += len(heure)
        elif cours== 'Classique 2':
            heure= st.multiselect('Horaire', ['Mercredi 17h45-19h15', 'Je voudrais un autre horaire'])
            courses_qtd +=len(heure)
        elif cours=='Classique Moyen':
            heure= st.multiselect('Horaire', ['Lundi 10h-11h30','Mardi 18h-19h30','Vendredi 10h-11h30','Vendredi 19h15-20h45', 'Je voudrais un autre horaire'])
            courses_qtd +=len(heure)
        elif cours=='Classique Interm. – Avancé':
            heure= st.multiselect('Horaire', ['Mercredi 19h30-21h','Jeudi 18h30-20h', 'Je voudrais un autre horaire'])
            courses_qtd +=len(heure)
        elif cours=='Classique Avancé':
            heure= st.multiselect('Horaire', ['Mardi 19h30-21h','Samedi 10h30-12h', 'Je voudrais un autre horaire'])
            courses_qtd +=len(heure)
        elif cours=='Pointes':
            heure= st.multiselect('Horaire', ['Vendredi 20h45-21h30', 'Je voudrais un autre horaire'])
            courses_qtd +=len(heure)
        elif cours=='Éveil':
            heure= st.multiselect('Horaire', ['Mardi 17h-17h45', 'Je voudrais un autre horaire'])
            courses_qtd +=len(heure)
        elif cours=='Préparatoire':
            heure= st.multiselect('Horaire', ['Lundi 17h-18h', 'Je voudrais un autre horaire'])
            courses_qtd +=len(heure)
        elif cours=='Moderne':
            heure= st.multiselect('Horaire', ['Avertissez-moi lorsque les cours sont disponibles'])
        elif cours=='Contemporain':
            heure= st.multiselect('Horaire', ['Vendredi 18h-19h15', 'Je voudrais un autre horaire'])
            courses_qtd +=len(heure)
        elif cours=='Barre à Terre':
            heure= st.multiselect('Horaire', ['Lundi 12h15-13h15','Mardi 9h-10h','Samedi 12h-13h', 'Je voudrais un autre horaire'])
            courses_qtd +=len(heure)
        elif cours=='PBT + Ballet Fitness':
            heure= st.multiselect('Horaire', ['Jeudi 9h30-10h30', 'Je voudrais un autre horaire'])
            courses_qtd +=len(heure)
        elif cours=='PBT':
            heure= st.multiselect('Horaire', ['Lundi 18h-19h','Mercredi 15h30-16h30', 'Je voudrais un autre horaire'])
            courses_qtd +=len(heure)
        elif cours=='Pilates':
            heure= st.multiselect('Horaire', ['Lundi 9h-10h','Lundi 20h45-21h45','Mercredi 9h-10h','Jeudi 20h-21h','Vendredi 9h-10h', 'Je voudrais un autre horaire'])
            courses_qtd +=len(heure)
        try:
            cours_info.append(cours)
            cours_info.append(heure)
            cours_info.append(courses_qtd)
        except:
            pass
        return cours_info


    try:
        name= st.text_input ("Nom e prénom d'élève")
        birthday=st.text_input("Date de naissance (jj/mm/aaaa)")
        address = st.text_input ("Addresse")
        city = st.text_input ("Ville")
        pcode = st.text_input ("Postal / Zip Code", key = int)
        mail = st.text_input ("Email")
        telephone =st.text_input('Téléphone (example: +3306XXXXXXXX)')
        legal_representative =st.text_input ("Représentant légal de l’inscrit (Pour les mineurs)")

        course = st.selectbox('Cours', ['Sélectionnez votre cours', 'Classique 1','Classique 2','Classique Moyen','Classique Interm. – Avancé','Classique Avancé','Pointes','Éveil','Préparatoire', 'Moderne', 'Contemporain', 'Barre à Terre', 'PBT + Ballet Fitness', 'PBT', 'Pilates'])
        first_choice = course_choice(course)
        courses_qtd = 0
        course = first_choice[0]
        schedule = first_choice[1]
        courses_qtd_1 = first_choice[2]
        courses_qtd += courses_qtd_1

    except:
        st.write("S'il vous plaît, remplissez tout le formulaire!")
        
    with st.expander("Plus de cours"):
            course2 = st.selectbox('Cours', ['Sélectionnez votre second cours', 'Classique 1','Classique 2','Classique Moyen','Classique Interm. – Avancé','Classique Avancé','Pointes','Éveil','Préparatoire', 'Moderne', 'Contemporain', 'Barre à Terre', 'PBT + Ballet Fitness', 'PBT', 'Pilates'])
            second_choice = course_choice(course2)
            course3 = st.selectbox('Cours', ['Sélectionnez votre troisième cours', 'Classique 1','Classique 2','Classique Moyen','Classique Interm. – Avancé','Classique Avancé','Pointes','Éveil','Préparatoire', 'Moderne', 'Contemporain', 'Barre à Terre', 'PBT + Ballet Fitness', 'PBT', 'Pilates'])
            third_choice = course_choice(course3)
            try:
                course2 = second_choice[0]
                if course2 == 'Sélectionnez votre second cours':
                    course2 = '0'
                    schedule2 = '0'
                    courses_qtd_2 = '0'
                else:
                    schedule2 = second_choice[1]
                    courses_qtd_2 = second_choice[2]
                course3 = third_choice[0]         
                if course3 == 'Sélectionnez votre troisième cours':
                    course3 = '0'
                    schedule3 = '0'
                    courses_qtd_3 = '0'
                else:
                    schedule3 = third_choice[1]
                    courses_qtd_3 = third_choice[2]
                
            except:
                pass
            try: 
                courses_qtd += courses_qtd_2 
                courses_qtd += courses_qtd_3
            except:
                pass

    if courses_qtd == 0:
        st.write("Sélectionnez votre cours pour continuez")
    elif courses_qtd == 1:
        price = 470
    elif courses_qtd == 2:
        price = 690   
    elif courses_qtd == 3:
        price = 850
    elif courses_qtd > 3:
        price = 1100      
    try:
        registration = 30
        total = price+registration
        st.write(f'Total {total}€ ({price}€ des cours + {registration}€ adhésion)')
        installments = st.selectbox("Le paiement du cours sera effectué avec", ('1 chèque', '2 chèques', '3 chèques', '4 chèques', '5 chèques', '6 chèques', '7 chèques', '8 chèques', '9 chèques', '10 chèques')) 
        installments = installments.split(' ')[0]
        st.write(" Découvrez notre planning et nos tarifs a attitudecorpsetdanses.com/tarifs-et-planning")
        certificat_medical = st.file_uploader("Téléverser le Certificat Médical")
        if certificat_medical:
            certificat_dassurance = st.file_uploader("Téléverser le Certificat d’assurance extra-scolaire ou assurance civil")
            if certificat_dassurance:
                st.write("")
                daccord = st.multiselect("Pour l’abonnement annuel à Attitude Corps et Danses de la saison 2021/2022 je ne pourrai en aucun cas faire opposition à mes chèques ( voir article L131-35 du code monétaire et financier) ou en demander la restitution en cas d’arrêt de ma part.", ["Je suis d'accord", "Je suis pas d'accord"])
                autorise_image = st.multiselect("J'autorise l'autorisation de droit à l'image et/ou à la voix pour la promotion de l'Attitude Corps et Danses.", ["Oui", "Non"])
                reconnais_pris = st.multiselect("Je reconnais avoir pris connaissance du règlement intérieur *, des conditions générales d’inscriptions* de l’Association Attitude Corps et Danses, d’avoir présenté un certificat médical de non-contre indication à la pratique de la danse et d’avoir présenté un certificat d’assurance extra-scolaire ou assurance civil.* (*Règlement intérieur/ conditions générales disponibles sur: https://attitudecorpsetdanses.com/reglement-interieur/*).", ["Oui", "Non"])
                submitted = st.button("Envoyer")
    except:
        pass

    try:
        if submitted:
            name= name.title()
            date = parser.parse(birthday)
            birthday=date.strftime('%d-%m-%Y')
            born = str(birthday).split('-')[-1]
            today = date.today()
            age = today.year - int(born)
            address = address.title()
            geolocator = Nominatim(user_agent="geolocalização")
            location = geolocator.geocode(f'{address} {city} {pcode}')
            lat = location.latitude
            lon = location.longitude       
            city = city.title()
            if city == "Toulouse" or city =="toulouse":
                toulouse = "Toulouse"
            else:
                toulouse = "Autre ville"
            pcode = pcode
            mail = mail.lower()
            legal_representative =legal_representative.title()
            classes=[]
            for i in range(len(schedule)):
                classes.append(schedule[i])
            classes= ", ".join(classes)
            schedule=classes
            classes2=[]
            for i in range(len(schedule2)):
                classes2.append(schedule2[i])
            classes2= ", ".join(classes2)
            schedule2=classes2
            classes3=[]
            for i in range(len(schedule3)):
                classes3.append(schedule3[i])
            classes3= ", ".join(classes3)
            schedule3=classes3
            classes_student=[mail]
            data_courses= ['carte 10 cours', 'classique 1', 'pointes', 'classique interm. – avancé', 'éveil', 'classique 2', 'pbt', 'préparatoire', 'moderne', 'pilates', 'classique moyen', 'classique avancé', 'contemporain', 'barre à terre', 'pbt + ballet fitness', 'initiation']
            for cours in data_courses:
                if course == cours or course2 == cours or course3 == cours:
                    if course != 'carte 10 cours':
                        classes_student.append(1)
                    else:
                        for i in range(15):
                            classes_student.append(1)
                else:
                    classes_student.append(0)
    except:
        pass
        
    try:
        #connect_to_tunnel_and_mysqlserver  
        load_dotenv()
        
        db_server= os.getenv('db_server')
        user=os.getenv("user")
        db_port=os.getenv("db_port")
        password=os.getenv("password")
        ip=os.getenv("ip")
        db_name=os.getenv("db_name")
        ip_ssh=os.getenv("ip_ssh")
        ssh_username=os.getenv("ssh_username")
        ssh_password=os.getenv("ssh_password")
        remote_bind_address=os.getenv("remote_bind_address")
        try:
            server = SSHTunnelForwarder((ip_ssh, 4242), ssh_username=ssh_username, ssh_password=ssh_password, remote_bind_address=(db_server, 3306))
            server.start()
            port = str(server.local_bind_port)
            conn_addr = 'mysql://' + user + ':' + password + '@' + db_server + ':' + port + '/' + db_name
            engine = create_engine(conn_addr)
            connection = engine.connect()
        except:
            st.error("Quelque chose s'est mal passé. Réessayez plus tard!")
        try:
            mySql_insert_query0 = f"""UPDATE elevesdf set name = '{name}', birthday='{birthday}', age='{age}', address='{address}', city='{city}', toulouse = '{toulouse}', cpode='{pcode}',lat='{lat}',long='{lon}', mail='{mail}', telephone = '{telephone}', legal_representative= '{legal_representative}' where `name` = '{name}'"""
            engine.execute(mySql_insert_query0)
            st.spinner(text="S'il vous plaît, attendez !")
        except: 
            mySql_insert_query1 = f"""INSERT INTO elevesdf (name, birthday, age, address, city, toulouse, pcode, lat, `long`, mail, telephone, legal_representative) VALUES ('{name}', '{birthday}', {age}, '{address}', '{city}', '{toulouse}', {pcode},{lat}, {lon}, '{mail}', '{telephone}', '{legal_representative}')"""
            engine.execute(mySql_insert_query1)
            st.spinner(text="Veuillez patienter pendant que nous enregistrons vos informations !")
        try: 
            mySql_insert_query2 = f"""INSERT INTO coursdf22 (name, course, schedule, course2, schedule2, course3, schedule3) VALUES ('{mail}', '{course}', '{schedule}','{course2}', '{schedule2}','{course3}', '{schedule3}'); """
            engine.execute(mySql_insert_query2)
        except:
            st.error("Quelque chose s'est mal passé. Réessayez plus tard!")
        try: 
            mySql_insert_query3 = f"""INSERT INTO paimentsdf22 (name, registration, installments, total) VALUES  ('{mail}', '{registration}', '{installments}', '{total}');"""
            engine.execute(mySql_insert_query3)
        except:
            st.error("Quelque chose s'est mal passé. Réessayez plus tard!")
        try:
            courses = pd.read_sql_query("""SELECT name, course FROM coursdf22 UNION ALL SELECT name, course2 FROM coursdf22 UNION ALL SELECT name, course3 FROM coursdf22""",conn_addr)
            courses_filled=[]
            name_filled=[]
            for row in range(len(courses['course'])):
                if courses['course'].iloc[row] !='0' and courses['course'].iloc[row]  != "":
                    courses_filled.append(courses['course'].iloc[row])
                    name_filled.append(courses['name'].iloc[row])
            course_filled = pd.DataFrame(zip(courses_filled, name_filled))
            course_filled.columns = ['course', 'name']
            course_filled.to_sql('course_filled', conn_addr, if_exists='replace', index=False)
        except:
            st.error("Quelque chose s'est mal passé. Réessayez plus tard!")
        #bytes_medical = certificat_medical.getvalue()
        #sql_blob_query = f""" INSERT INTO medical23 VALUES (%s,%s)""" 
        #engine.execute(sql_blob_query, ['2',memoryview(bytes_medical)])
        #bytes_dassurance = certificat_dassurance.getvalue()
        #sql_blob_query = f""" INSERT INTO assurance23 VALUES (%s,%s)""" 
        #engine.execute(sql_blob_query, ['2',memoryview(bytes_dassurance)])    

        connection.close()  
        server.stop()
        #my_email= os.getenv('my_email')
        #mail_password= os.getenv('mail_password')
        #msg=MIMEText(f"""{name} , 
        #votre inscription à Attitude Corps et Danses a été reçue! En cas de problème concernant les informations ou les fichiers fournis, nous vous contacterons !
        #Rendez-vous en classe !""")
        #msg['Subject']= f" {name}, votre inscription à Attitude Corps et Danses !"
        #msg['From']= my_email
        #msg["To"]= f'{mail}, {my_email}'
        #mail_server = smtplib.SMTP_SSL('smtp.gmail.com' ,465)
        #mail_server.ehlo()
        #mail_server.login(my_email, mail_password)
        #mail_server.sendmail(msg["From"], msg["To"], msg.as_string())
        #mail_server.close()
        st.success("Merci! Rendez-vous en classe !")
        st.balloons()
    except:
        pass    




