import streamlit as st
import pandas as pd
import re
import os, os.path
import datetime
from dateutil import parser
from geopy.geocoders import Nominatim 
from sshtunnel import SSHTunnelForwarder
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import pymysql
import os, os.path
from dotenv import load_dotenv
pymysql.install_as_MySQLdb()
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib,ssl


st.image(('logo.png'))

st.title('Inscrivez-vous')
st.sidebar.title('Réservez un cours')

#with st.form("Inscrivez-vous"):
try:
    name= st.text_input ("Nom e prénom d'élève")
    birthday=st.text_input("Date de naissance (jj/mm/aaaa)")
    address = st.text_input ("Addresse")
    city = st.text_input ("Ville")
    pcode = st.text_input ("Postal / Zip Code", key = int)
    mail = st.text_input ("Email")
    telephone =st.text_input('Téléphone (example: +3306XXXXXXXX)')
    legal_representative =st.text_input ("Représentant légal de l’inscrit (Pour les mineurs)")


    courses_qtd = 0
    course = st.selectbox('Cours', ['Sélectionnez votre cours', 'Carte de 10 cours', 'Classique', 'Moderne', 'Contemporain', 'Barre à Terre', 'PBT + Ballet Fitness', 'PBT', 'Pilates'])
    if course == 'Classique':
        course = st.selectbox("Cours", ['Sélectionnez votre cours Classique','Classique 1','Classique 2','Classique Moyen','Classique Interm. – Avancé','Classique Avancé','Pointes','Éveil','Préparatoire'])
    else:
        pass
    if course == 'Carte de 10 cours':
            carte_10_cours = st.multiselect('Cours', ['Sélectionnez vos cours', 'Classique 1','Classique 2','Classique Moyen','Classique Interm. – Avancé','Classique Avancé','Pointes','Éveil','Préparatoire','Moderne','Contemporain','Barre à Terre','PBT + Ballet Fitness','PBT','Pilates'])
            courses_qtd +=4
    else:
        pass
    if course == 'Classique 1':
        schedule = st.multiselect('Horaire', ['Mercredi 14h15-15h30', 'Je voudrais un autre horaire'])
        courses_qtd += len(schedule)
        if schedule == 'Je voudrais un autre horaire':
            st.text_input ("Suggérer l'horaire")
    elif course == 'Classique 2':
        schedule = st.multiselect('Horaire', ['Mercredi 17h45-19h15', 'Je voudrais un autre horaire'])
        courses_qtd +=len(schedule)
        if schedule == 'Je voudrais un autre horaire':
            st.text_input ("Suggérer l'horaire")
    elif course =='Classique Moyen':
        schedule = st.multiselect('Horaire', ['Lundi 10h-11h30','Mardi 18h-19h30','Vendredi 10h-11h30','Vendredi 19h15-20h45', 'Je voudrais un autre horaire'])
        courses_qtd +=len(schedule)
        if schedule == 'Je voudrais un autre horaire':
            st.text_input ("Suggérer l'horaire")
    elif course =='Classique Interm. – Avancé':
        schedule = st.multiselect('Horaire', ['Mercredi 19h30-21h','Jeudi 18h30-20h', 'Je voudrais un autre horaire'])
        courses_qtd +=len(schedule)
        if schedule == 'Je voudrais un autre horaire':
            st.text_input ("Suggérer l'horaire")
    elif course =='Classique Avancé':
        schedule = st.multiselect('Horaire', ['Mardi 19h30-21h','Samedi 10h30-12h', 'Je voudrais un autre horaire'])
        courses_qtd +=len(schedule)
        if schedule == 'Je voudrais un autre horaire':
            st.text_input ("Suggérer l'horaire")
    elif course =='Pointes':
        schedule = st.multiselect('Horaire', ['Vendredi 20h45-21h30', 'Je voudrais un autre horaire'])
        courses_qtd +=len(schedule)
        if schedule == 'Je voudrais un autre horaire':
            st.text_input ("Suggérer l'horaire")
    elif course =='Éveil':
        schedule = st.multiselect('Horaire', ['Mardi 17h-17h45', 'Je voudrais un autre horaire'])
        courses_qtd +=len(schedule)
        if schedule == 'Je voudrais un autre horaire':
            st.text_input ("Suggérer l'horaire")
    elif course =='Préparatoire':
        schedule = st.multiselect('Horaire', ['Lundi 17h-18h', 'Je voudrais un autre horaire'])
        courses_qtd +=len(schedule)
        if schedule == 'Je voudrais un autre horaire':
            st.text_input ("Suggérer l'horaire")
    elif course =='Moderne':
        schedule = st.multiselect('Horaire', ['Avertissez-moi lorsque les cours sont disponibles'])
    elif course =='Contemporain':
        schedule = st.multiselect('Horaire', ['Vendredi 18h-19h15', 'Je voudrais un autre horaire'])
        courses_qtd +=len(schedule)
        if schedule == 'Je voudrais un autre horaire':
            st.text_input ("Suggérer l'horaire")
    elif course =='Barre à Terre':
        schedule = st.multiselect('Horaire', ['Lundi 12h15-13h15','Mardi 9h-10h','Samedi 12h-13h', 'Je voudrais un autre horaire'])
        courses_qtd +=len(schedule)
        if schedule == 'Je voudrais un autre horaire':
            st.text_input ("Suggérer l'horaire")
    elif course =='PBT + Ballet Fitness':
        schedule = st.multiselect('Horaire', ['Jeudi 9h30-10h30', 'Je voudrais un autre horaire'])
        courses_qtd +=len(schedule)
        if schedule == 'Je voudrais un autre horaire':
            st.text_input ("Suggérer l'horaire")
    elif course =='PBT':
        schedule = st.multiselect('Horaire', ['Lundi 18h-19h','Mercredi 15h30-16h30', 'Je voudrais un autre horaire'])
        courses_qtd +=len(schedule)
        if schedule == 'Je voudrais un autre horaire':
            st.text_input ("Suggérer l'horaire")
    elif course =='Pilates':
        schedule = st.multiselect('Horaire', ['Lundi 9h-10h','Lundi 20h45-21h45','Mercredi 9h-10h','Jeudi 20h-21h','Vendredi 9h-10h', 'Je voudrais un autre horaire'])
        courses_qtd +=len(schedule)
        if schedule == 'Je voudrais un autre horaire':
            st.text_input ("Suggérer l'horaire")
    else:
        pass   
    with st.expander("Plus de cours"):
        try:
            course2 = st.selectbox("Cours 2",('Sélectionnez votre cours', 'Classique','Moderne','Contemporain','Barre à Terre','PBT + Ballet Fitness','PBT','Pilates'))
            try:
                if course2 == 'Classique':
                    course2 == st.selectbox("Cours 2",('Sélectionnez votre cours', 'Classique 1','Classique 2','Classique Moyen','Classique Interm. – Avancé','Classique Avancé','Pointes','Éveil','Préparatoire'))
            except:
                pass
            if course2 == 'Classique 1':
                schedule2 = st.multiselect('Horaire', ['Mercredi 14h15-15h30', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule2)
                if schedule2 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course2 == 'Classique 2':
                schedule2 = st.multiselect('Horaire', ['Mercredi 17h45-19h15', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule2)
                if schedule2 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course2 =='Classique Moyen':
                schedule2 = st.multiselect('Horaire', ['Lundi 10h-11h30','Mardi 18h-19h30','Vendredi 10h-11h30','Vendredi 19h15-20h45', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule2)
                if schedule2 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course2 =='Classique Interm. – Avancé':
                schedule2 = st.multiselect('Horaire', ['Mercredi 19h30-21h','Jeudi 18h30-20h', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule2)
                if schedule2 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course2 =='Classique Avancé':
                schedule2 = st.multiselect('Horaire', ['Mardi 19h30-21h','Samedi 10h30-12h', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule2)
                if schedule2 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course2 =='Pointes':
                schedule2 = st.multiselect('Horaire', ['Vendredi 20h45-21h30', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule2)
                if schedule2 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course2 =='Éveil':
                schedule2 = st.multiselect('Horaire', ['Mardi 17h-17h45', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule2)
                if schedule2 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course2 =='Préparatoire':
                schedule2 = st.multiselect('Horaire', ['Lundi 17h-18h', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule2)
                if schedule2 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course2 =='Moderne':
                schedule2 = st.multiselect('Horaire', ['Avertissez-moi lorsque les cours sont disponibles'])
                courses_qtd +=len(schedule2)
            elif course2 =='Contemporain':
                schedule2 = st.multiselect('Horaire', ['Vendredi 18h-19h15', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule2)
                if schedule2 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course2 =='Barre à Terre':
                schedule2 = st.multiselect('Horaire', ['Lundi 12h15-13h15','Mardi 9h-10h','Samedi 12h-13h', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule2)
                if schedule2 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course2 =='PBT + Ballet Fitness':
                schedule2 = st.multiselect('Horaire', ['Jeudi 9h30-10h30', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule2)
                if schedule2 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course2 =='PBT':
                schedule2 = st.multiselect('Horaire', ['Lundi 18h-19h','Mercredi 15h30-16h30', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule2)
                if schedule2 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course2 =='Pilates':
                schedule2 = st.multiselect('Horaire', ['Lundi 9h-10h','Lundi 20h45-21h45','Mercredi 9h-10h','Jeudi 20h-21h','Vendredi 9h-10h', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule2)
                if schedule2 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")   
            else:
                course2="0"
                schedule2 = "0"
        except:
            course2="0"
            schedule2="0"  
        try:
            course3 = st.selectbox("Cours 3",('Sélectionnez votre cours','Classique','Moderne','Contemporain','Barre à Terre','PBT + Ballet Fitness','PBT','Pilates'))
            try:
                if course3 == 'Classique':
                    course3 == st.selectbox("Cours 3",('Sélectionnez votre cours','Classique 1','Classique 2','Classique Moyen','Classique Interm. – Avancé','Classique Avancé','Pointes','Éveil','Préparatoire'))
            except:        
                pass
            if course3 == 'Classique 1':
                schedule3 = st.multiselect('Horaire', ['Mercredi 14h15-15h30', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule3)
                if schedule3 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course3 == 'Classique 2':
                schedule3 = st.multiselect('Horaire', ['Mercredi 17h45-19h15', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule3)
                if schedule3 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course3 =='Classique Moyen':
                schedule3 = st.multiselect('Horaire', ['Lundi 10h-11h30','Mardi 18h-19h30','Vendredi 10h-11h30','Vendredi 19h15-20h45', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule3)
                if schedule3 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course3 =='Classique Interm. – Avancé':
                schedule3 = st.multiselect('Horaire', ['Mercredi 19h30-21h','Jeudi 18h30-20h', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule3)
                if schedule3 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course3 =='Classique Avancé':
                schedule3 = st.multiselect('Horaire', ['Mardi 19h30-21h','Samedi 10h30-12h', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule3)
                if schedule3 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course3 =='Pointes':
                schedule3 = st.multiselect('Horaire', ['Vendredi 20h45-21h30', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule3)
                if schedule3 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course3 =='Éveil':
                schedule3 = st.multiselect('Horaire', ['Mardi 17h-17h45', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule3)
                if schedule3 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course3 =='Préparatoire':
                schedule3 = st.multiselect('Horaire', ['Lundi 17h-18h', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule3)
                if schedule3 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course3 =='Moderne':
                schedule3 = st.multiselect('Horaire', ['Avertissez-moi lorsque les cours sont disponibles'])
                courses_qtd +=len(schedule3)
            elif course3 =='Contemporain':
                schedule3 = st.multiselect('Horaire', ['Vendredi 18h-19h15', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule3)
                if schedule3 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course3 =='Barre à Terre':
                schedule3 = st.multiselect('Horaire', ['Lundi 12h15-13h15','Mardi 9h-10h','Samedi 12h-13h', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule3)
                if schedule3 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course3 =='PBT + Ballet Fitness':
                schedule3 = st.multiselect('Horaire', ['Jeudi 9h30-10h30', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule3)
                if schedule3 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course3 =='PBT':
                schedule3 = st.multiselect('Horaire', ['Lundi 18h-19h','Mercredi 15h30-16h30', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule3)
                if schedule3 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            elif course3 =='Pilates':
                schedule3 = st.multiselect('Horaire', ['Lundi 9h-10h','Lundi 20h45-21h45','Mercredi 9h-10h','Jeudi 20h-21h','Vendredi 9h-10h', 'Je voudrais un autre horaire'])
                courses_qtd +=len(schedule3)
                if schedule3 == 'Je voudrais un autre horaire':
                    st.text_input ("Suggérer l'horaire")
            else:
                course3="0"
                schedule3="0"
        except:
            course3="0"
            schedule3="0"
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
        registration =30
        total = price+registration
        st.write(f'Total {total}€ ({price}€ des cours + {registration}€ adhésion)')
        installments = st.selectbox("Le paiement du cours sera effectué avec", ('1 chèque', '2 chèques', '3 chèques', '4 chèques', '5 chèques', '6 chèques', '7 chèques', '8 chèques', '9 chèques', '10 chèques')) 
        installments = installments.split(' ')[0]

        st.write(" Découvrez notre planning et nos tarifs a attitudecorpsetdanses.com/tarifs-et-planning")

        certificat_medical = st.file_uploader("Téléverser le Certificat Médical")
        if certificat_medical is not None:
                certificat_dassurance = st.file_uploader("Téléverser le Certificat d’assurance extra-scolaire ou assurance civil")
                if certificat_dassurance is not None:
                    st.write("")
                    daccord = st.multiselect("Pour l’abonnement annuel à Attitude Corps et Danses de la saison 2021/2022 je ne pourrai en aucun cas faire opposition à mes chèques ( voir article L131-35 du code monétaire et financier) ou en demander la restitution en cas d’arrêt de ma part.", ["Je suis d'accord", "Je suis pas d'accord"])

                    autorise_image = st.multiselect("J'autorise l'autorisation de droit à l'image et/ou à la voix pour la promotion de l'Attitude Corps et Danses.", ["Oui", "Non"])
                    reconnais_pris = st.multiselect("Je reconnais avoir pris connaissance du règlement intérieur *, des conditions générales d’inscriptions* de l’Association Attitude Corps et Danses, d’avoir présenté un certificat médical de non-contre indication à la pratique de la danse et d’avoir présenté un certificat d’assurance extra-scolaire ou assurance civil.* (*Règlement intérieur/ conditions générales disponibles sur: https://attitudecorpsetdanses.com/reglement-interieur/*).", ["Oui", "Non"])

                    
                    submitted = st.button("Envoyer")

    except:
        pass
except:
    pass
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
        st.write("Quelque chose s'est mal passé. Réessayez plus tard!")
    try:
        mySql_insert_query0 = f"""UPDATE elevesdf set name = '{name}', birthday='{birthday}', age='{age}', address='{address}', city='{city}', cpode='{pcode}',lat='{lat}',long='{lon}', mail='{mail}', telephone = '{telephone}', legal_representative= '{legal_representative}' where `name` = '{name}'"""
        engine.execute(mySql_insert_query0)
        st.write ('Vos informations ont été mises à jour !')
    except: 
        mySql_insert_query1 = f"""INSERT INTO elevesdf (name, birthday, age, address, city, pcode, lat, `long`, mail, telephone, legal_representative) VALUES ('{name}', '{birthday}', {age}, '{address}', '{city}', {pcode},{lat}, {lon}, '{mail}', '{telephone}', '{legal_representative}')"""
        engine.execute(mySql_insert_query1)
    mySql_insert_query2 = f"""INSERT INTO coursdf23 (name, course, schedule, course2, schedule2, course3, schedule3) VALUES  ('{mail}', '{course}', '{schedule}','{course2}', '{schedule2}','{course3}', '{schedule3}'); """
    
    def convert_binary(filename):
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData
    def insert_file(id, mail, file,):
        try:
            sql_blob_query = """ INSERT INTO medical23
                            (id, mail, file) VALUES (%s,%s,%s)"""

            fileconverted = convert_binary(file)
            blob_tuple = (id, name, fileconverted, file)
            result = cursor.execute(sql_blob_query, blob_tuple)
            connection.commit()

        except:
            st.write('error')

    insert_file(1, f"{mail}", {certificat_medical})
    insert_file(2, f"{mail}", {certificat_dassurance})
    
    
    
    
    mySql_insert_query4 = f"""INSERT INTO paimentsdf23 (name, registration, installments, total) VALUES  ('{mail}', '{registration}', '{installments}', '{total}');"""
    engine.execute(mySql_insert_query2)
    engine.execute(mySql_insert_query4)
    st.write ("S'il vous plaît, attendez! !")
    courses = pd.read_sql_query("""SELECT name, course from coursdf22 union all select name, course2 from coursdf22 union all select name, course3 from coursdf22""",conn_addr)
    courses_filled=[]
    name_filled=[]
    for row in range(len(courses['course'])):
        if courses['course'].iloc[row] !='0' and courses['course'].iloc[row]  != "":
            courses_filled.append(courses['course'].iloc[row])
            name_filled.append(courses['name'].iloc[row])
    course_filled = pd.DataFrame(zip(courses_filled, name_filled))
    course_filled.columns = ['course', 'name']
    course_filled.to_sql('course_filled', conn_addr, if_exists='replace', index=False)
    st.write ('Vos informations ont été reçues !')
    connection.close()  
    server.stop()

    my_email= os.getenv('my_email')
    mail_password= os.getenv('mail_password')

    msg=MIMEText(f"""{name} , 
    votre inscription à Attitude Corps et Danses a été reçue! En cas de problème concernant les informations ou les fichiers fournis, nous vous contacterons !
     Rendez-vous en classe !""")
    msg['Subject']= f" {name}, votre inscription à Attitude Corps et Danses !"
    msg['From']= my_email
    msg["To"]= f'{mail}, {my_email}'
    mail_server = smtplib.SMTP_SSL('smtp.gmail.com' ,465)
    mail_server.ehlo()
    mail_server.login(my_email, mail_password)
    mail_server.sendmail(msg["From"], msg["To"], msg.as_string())

    mail_server.close()

    st.title("Merci! Rendez-vous en classe !")
    




