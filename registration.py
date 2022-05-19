import streamlit as st
import pandas as pd
import re
import os, os.path
import datetime
from sshtunnel import SSHTunnelForwarder
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import pymysql
pymysql.install_as_MySQLdb()

st.image(('logo.png'))

st.title('Inscrivez-vous')
st.sidebar.title('Réservez un cours')

with st.form("Inscrivez-vous"):

    name= st.text_input ("Nom e prénom d'élève")
    birthday=st.text_input("Date de naissance (jj/mm/aa)")
    address = st.text_input ("Addresse")
    city = st.text_input ("Ville")
    pcode = st.text_input ("Postal / Zip Code", key = int)
    mail = st.text_input ("Email")
    telephone =st.text_input('Téléphone (example: +3306XXXXXXXX)')
    legal_representative =st.text_input ("Représentant légal de l’inscrit (Pour les mineurs)")

    courses_qtd = 0
    course = st.selectbox("Cours",('Sélectionnez votre cours', 'Classique','Moderne','Contemporain','Barre à Terre','PBT + Ballet Fitness','PBT','Pilates'))
    try:
        if course == 'Classique':
            course == st.selectbox("Cours", ('Sélectionnez votre cours Classique','Classique 1','Classique 2','Classique Moyen','Classique Interm. – Avancé','Classique Avancé','Pointes','Éveil','Préparatoire'))
        try:
            if course == 'Carte de 10 cours':
                carte_10_cours = st.multiselect('Cours', ['Sélectionnez vos cours', 'Classique 1','Classique 2','Classique Moyen','Classique Interm. – Avancé','Classique Avancé','Pointes','Éveil','Préparatoire','Moderne','Contemporain','Barre à Terre','PBT + Ballet Fitness','PBT','Pilates'])
                courses_qtd +=4
        except:
            pass
        if course == 'Classique 1':
            courses_qtd +=1
            schedule = st.multiselect('Horaire', ['Mercredi 14h15-15h30', 'Je voudrais un autre horaire'])
            if schedule == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course == 'Classique 2':
            courses_qtd +=1
            schedule = st.multiselect('Horaire', ['Mercredi 17h45-19h15', 'Je voudrais un autre horaire'])
            if schedule == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course =='Classique Moyen':
            courses_qtd +=1
            schedule = st.multiselect('Horaire', ['Lundi 10h-11h30','Mardi 18h-19h30','Vendredi 10h-11h30','Vendredi 19h15-20h45', 'Je voudrais un autre horaire'])
            if schedule == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course =='Classique Interm. – Avancé':
            courses_qtd +=1
            schedule = st.multiselect('Horaire', ['Mercredi 19h30-21h','Jeudi 18h30-20h', 'Je voudrais un autre horaire'])
            if schedule == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course =='Classique Avancé':
            courses_qtd +=1
            schedule = st.multiselect('Horaire', ['Mardi 19h30-21h','Samedi 10h30-12h', 'Je voudrais un autre horaire'])
            if schedule == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course =='Pointes':
            courses_qtd +=1
            schedule = st.multiselect('Horaire', ['Vendredi 20h45-21h30', 'Je voudrais un autre horaire'])
            if schedule == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course =='Éveil':
            courses_qtd +=1
            schedule = st.multiselect('Horaire', ['Mardi 17h-17h45', 'Je voudrais un autre horaire'])
            if schedule == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course =='Préparatoire':
            courses_qtd +=1
            schedule = st.multiselect('Horaire', ['Lundi 17h-18h', 'Je voudrais un autre horaire'])
            if schedule == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course =='Moderne':
            courses_qtd +=1
            schedule = st.multiselect('Horaire', ['Avertissez-moi lorsque les cours sont disponibles'])
        elif course =='Contemporain':
            courses_qtd +=1
            schedule = st.multiselect('Horaire', ['Vendredi 18h-19h15', 'Je voudrais un autre horaire'])
            if schedule == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course =='Barre à Terre':
            courses_qtd +=1
            schedule = st.multiselect('Horaire', ['Lundi 12h15-13h15','Mardi 9h-10h','Samedi 12h-13h', 'Je voudrais un autre horaire'])
            if schedule == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course =='PBT + Ballet Fitness':
            courses_qtd +=1
            schedule = st.multiselect('Horaire', ['Jeudi 9h30-10h30', 'Je voudrais un autre horaire'])
            if schedule == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course =='PBT':
            courses_qtd +=1
            schedule = st.multiselect('Horaire', ['Lundi 18h-19h','Mercredi 15h30-16h30', 'Je voudrais un autre horaire'])
            if schedule == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course =='Pilates':
            courses_qtd +=1
            schedule = st.multiselect('Horaire', ['Lundi 9h-10h','Lundi 20h45-21h45','Mercredi 9h-10h','Jeudi 20h-21h','Vendredi 9h-10h', 'Je voudrais un autre horaire'])
            if schedule == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
    except:
        pass   
    with st.expander("Plus de cours"):
        course2 = st.selectbox("Cours 2",('Sélectionnez votre cours', 'Classique','Moderne','Contemporain','Barre à Terre','PBT + Ballet Fitness','PBT','Pilates'))
        try:
            if course2 == 'Classique':
                course2 == st.selectbox("Cours 2",('Sélectionnez votre cours', 'Classique 1','Classique 2','Classique Moyen','Classique Interm. – Avancé','Classique Avancé','Pointes','Éveil','Préparatoire'))
        except:
            pass
        if course2 == 'Classique 1':
            courses_qtd +=1
            schedule2 = st.multiselect('Horaire', ['Mercredi 14h15-15h30', 'Je voudrais un autre horaire'])
            if schedule2 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course2 == 'Classique 2':
            courses_qtd +=1
            schedule2 = st.multiselect('Horaire', ['Mercredi 17h45-19h15', 'Je voudrais un autre horaire'])
            if schedule2 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course2 =='Classique Moyen':
            courses_qtd +=1
            schedule2 = st.multiselect('Horaire', ['Lundi 10h-11h30','Mardi 18h-19h30','Vendredi 10h-11h30','Vendredi 19h15-20h45', 'Je voudrais un autre horaire'])
            if schedule2 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course2 =='Classique Interm. – Avancé':
            courses_qtd +=1
            schedule2 = st.multiselect('Horaire', ['Mercredi 19h30-21h','Jeudi 18h30-20h', 'Je voudrais un autre horaire'])
            if schedule2 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course2 =='Classique Avancé':
            courses_qtd +=1
            schedule2 = st.multiselect('Horaire', ['Mardi 19h30-21h','Samedi 10h30-12h', 'Je voudrais un autre horaire'])
            if schedule2 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course2 =='Pointes':
            courses_qtd +=1
            schedule2 = st.multiselect('Horaire', ['Vendredi 20h45-21h30', 'Je voudrais un autre horaire'])
            if schedule2 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course2 =='Éveil':
            courses_qtd +=1
            schedule2 = st.multiselect('Horaire', ['Mardi 17h-17h45', 'Je voudrais un autre horaire'])
            if schedule2 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course2 =='Préparatoire':
            courses_qtd +=1
            schedule2 = st.multiselect('Horaire', ['Lundi 17h-18h', 'Je voudrais un autre horaire'])
            if schedule2 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course2 =='Moderne':
            courses_qtd +=1
            schedule2 = st.multiselect('Horaire', ['Avertissez-moi lorsque les cours sont disponibles'])
        elif course2 =='Contemporain':
            courses_qtd +=1
            schedule2 = st.multiselect('Horaire', ['Vendredi 18h-19h15', 'Je voudrais un autre horaire'])
            if schedule2 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course2 =='Barre à Terre':
            courses_qtd +=1
            schedule2 = st.multiselect('Horaire', ['Lundi 12h15-13h15','Mardi 9h-10h','Samedi 12h-13h', 'Je voudrais un autre horaire'])
            if schedule2 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course2 =='PBT + Ballet Fitness':
            courses_qtd +=1
            schedule2 = st.multiselect('Horaire', ['Jeudi 9h30-10h30', 'Je voudrais un autre horaire'])
            if schedule2 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course2 =='PBT':
            courses_qtd +=1
            schedule2 = st.multiselect('Horaire', ['Lundi 18h-19h','Mercredi 15h30-16h30', 'Je voudrais un autre horaire'])
            if schedule2 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course2 =='Pilates':
            courses_qtd +=1
            schedule2 = st.multiselect('Horaire', ['Lundi 9h-10h','Lundi 20h45-21h45','Mercredi 9h-10h','Jeudi 20h-21h','Vendredi 9h-10h', 'Je voudrais un autre horaire'])
            if schedule2 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")     
        course3 = st.selectbox("Cours 3",('Sélectionnez votre cours','Classique','Moderne','Contemporain','Barre à Terre','PBT + Ballet Fitness','PBT','Pilates'))
        try:
            if course3 == 'Classique':
                course3 == st.selectbox("Cours 3",('Sélectionnez votre cours','Classique 1','Classique 2','Classique Moyen','Classique Interm. – Avancé','Classique Avancé','Pointes','Éveil','Préparatoire'))
        except:        
            pass
        if course3 == 'Classique 1':
            courses_qtd +=1
            schedule3 = st.multiselect('Horaire', ['Mercredi 14h15-15h30', 'Je voudrais un autre horaire'])
            if schedule3 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course3 == 'Classique 2':
            courses_qtd +=1
            schedule3 = st.multiselect('Horaire', ['Mercredi 17h45-19h15', 'Je voudrais un autre horaire'])
            if schedule3 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course3 =='Classique Moyen':
            courses_qtd +=1
            schedule3 = st.multiselect('Horaire', ['Lundi 10h-11h30','Mardi 18h-19h30','Vendredi 10h-11h30','Vendredi 19h15-20h45', 'Je voudrais un autre horaire'])
            if schedule3 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course3 =='Classique Interm. – Avancé':
            courses_qtd +=1
            schedule3 = st.multiselect('Horaire', ['Mercredi 19h30-21h','Jeudi 18h30-20h', 'Je voudrais un autre horaire'])
            if schedule3 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course3 =='Classique Avancé':
            courses_qtd +=1
            schedule3 = st.multiselect('Horaire', ['Mardi 19h30-21h','Samedi 10h30-12h', 'Je voudrais un autre horaire'])
            if schedule3 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course3 =='Pointes':
            courses_qtd +=1
            schedule3 = st.multiselect('Horaire', ['Vendredi 20h45-21h30', 'Je voudrais un autre horaire'])
            if schedule3 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course3 =='Éveil':
            courses_qtd +=1
            schedule3 = st.multiselect('Horaire', ['Mardi 17h-17h45', 'Je voudrais un autre horaire'])
            if schedule3 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course3 =='Préparatoire':
            courses_qtd +=1
            schedule3 = st.multiselect('Horaire', ['Lundi 17h-18h', 'Je voudrais un autre horaire'])
            if schedule3 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course3 =='Moderne':
            courses_qtd +=1
            schedule3 = st.multiselect('Horaire', ['Avertissez-moi lorsque les cours sont disponibles'])
        elif course3 =='Contemporain':
            courses_qtd +=1
            schedule3 = st.multiselect('Horaire', ['Vendredi 18h-19h15', 'Je voudrais un autre horaire'])
            if schedule3 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course3 =='Barre à Terre':
            courses_qtd +=1
            schedule3 = st.multiselect('Horaire', ['Lundi 12h15-13h15','Mardi 9h-10h','Samedi 12h-13h', 'Je voudrais un autre horaire'])
            if schedule3 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course3 =='PBT + Ballet Fitness':
            courses_qtd +=1
            schedule3 = st.multiselect('Horaire', ['Jeudi 9h30-10h30', 'Je voudrais un autre horaire'])
            if schedule3 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course3 =='PBT':
            courses_qtd +=1
            schedule3 = st.multiselect('Horaire', ['Lundi 18h-19h','Mercredi 15h30-16h30', 'Je voudrais un autre horaire'])
            if schedule3 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")
        elif course3 =='Pilates':
            courses_qtd +=1
            schedule3 = st.multiselect('Horaire', ['Lundi 9h-10h','Lundi 20h45-21h45','Mercredi 9h-10h','Jeudi 20h-21h','Vendredi 9h-10h', 'Je voudrais un autre horaire'])
            if schedule3 == 'Je voudrais un autre horaire':
                st.text_input ("Suggérer l'horaire")

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

                    
                    submitted = st.form_submit_button("Envoyer")
                    if submitted == True:
                        st.title("Merci! Rendez-vous en classe !")
    except:
        pass
    try:
            submitted2 = st.form_submit_button("Envoyer")
            if submitted2 == True:
                if courses_qtd == 0:
                    st.write("Remplissez l'intégralité du formulaire pour le soumettre !")
                if certificat_medical is None:
                    st.write("Remplissez l'intégralité du formulaire pour le soumettre !")
                if daccord != "Je suis d'accord" and autorise_image != 'Oui' and reconnais_pris != "Oui":
                    st.write("Remplissez l'intégralité du formulaire pour le soumettre !")
                    
    except:
        pass

try:
    if submitted == True:
        name= name.title()
        date = parser.parse(birthday)
        birthday=date.strftime('%d-%m-%Y')
        address = address.title()
        city = city.title()
        pcode = pcode
        mail = mail.lower()
        legal_representative =legal_representative.title()
        course = course.lower()
        schedule = schedule.lower()
        course2=course2.lower()
        schedule2=schedule2.lower()
        course3=course3.lower()
        schedule3=schedule3.lower()

        certificat_dassurance
        certificat_medical
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
                
    db_server= '127.0.0.1'
    user='tete'
    db_port = '3306'
    password = 'frida2202'
    ip = 'localhost'
    db_name = 'attitude'        
    server = SSHTunnelForwarder(('138.197.99.33', 4242), ssh_username="tete", ssh_password="frida", remote_bind_address=('127.0.0.1', 3306))
    server.start()
    port = str(server.local_bind_port)
    conn_addr = 'mysql://' + user + ':' + password + '@' + db_server + ':' + port + '/' + db_name
    engine = create_engine(conn_addr)
    connection = engine.connect()


    try:
        mySql_insert_query0 = """UPDATE elevesdf set `Nom et prénom d'élève` = {name}, `Date de naissance`={birthday}, `Adresse`={address}, `Cité`={city}, `Code Postale`={pcode}, `E-mail`={mail}, `Téléphone` = {telephone}, `Représentant légal de l’inscrit (pour les mineurs)= {legal_representative} where `Nom et prénom d'élève` = {name}"""
        engine.execute(mySql_insert_query0)
    except: 
        mySql_insert_query1 = """INSERT INTO 'elevesdf' (`Nom et prénom d'élève`, `Date de naissance`, `Adresse`, `Cité`, `Code Postale`, `E-mail`, `Téléphone`, `Représentant légal de l’inscrit (pour les mineurs)`) VALUES ({name}, {birthday}, {address}, {city}, {pcode}, {mail}, {telephone}. {legal_representative}) """
        engine.execute(mySql_insert_query1)
    mySql_insert_query2 = """INSERT INTO 'coursdf23' (`Nom et prénom d'élève`, `Cours`, `Horaire`, `Cours 2`, `Horaire 2`, `Cours 3`, `Horaire 3`) VALUES  ({mail}, {course}, {schedule},{course2}, {schedule2},{course3}, {schedule3}) """
    mySql_insert_query3 = """INSERT INTO 'classesdf23' (`nom`, `classique 1`,`pointes`, `classique interm. – avancé`,`éveil`,`classique 2`,`pbt`,`préparatoire`,`moderne`,`pilates`,`classique moyen`,`classique avancé`,`contemporain`,`barre à terre`,`pbt + ballet fitness`,`initiation`) VALUES ({classes_student}) """
    mySql_insert_query4 = """INSERT INTO "paimentsdf23" (`Nom et prénom d'élève`, `Adhésion`, `Paiement fractionné`, `Paiement Total`) VALUES  ({mail}, {registration}, {installments}, {total})"""
    engine.execute(mySql_insert_query2)
    engine.execute(mySql_insert_query3)
    engine.execute(mySql_insert_query4)
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
    connection.close()  
    server.stop()
except:
    pass
    




