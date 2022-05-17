import streamlit as st
import pandas as pd
import re
import os, os.path
import datetime

st.image(('logo.png'))

st.title('Inscrivez-vous')
st.sidebar.title('Réservez un cours')

with st.form("Inscrivez-vous"):

    name= st.text_input ("Nom e prénom d'élève")
    birthday=st.text_input("Date de naissance")
    address = st.text_input ("Addresse")
    city = st.text_input ("Ville")
    pcode = st.text_input ("Postal / Zip Code", key = int)
    mail = st.text_input ("Email")
    st.write('example@example.com')
    telephone =st.text_input('Téléphone')
    st.write("S'il vous plaît entrer un numéro de téléphone valide")
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

#mySql_insert_query = """INSERT INTO 'elevesdf' (Id, Name, Price, Purchase_date) VALUES (15, 'Lenovo ThinkPad P71', 6459, '2019-08-14') """
#mySql_insert_query = """INSERT INTO 'coursdf' (Id, Name, Price, Purchase_date) VALUES  (15, 'Lenovo ThinkPad P71', 6459, '2019-08-14') """
#mySql_insert_query = """INSERT INTO 'classesdf' (Id, Name, Price, Purchase_date) VALUES (15, 'Lenovo ThinkPad P71', 6459, '2019-08-14') """
#mySql_insert_query = """INSERT INTO 'paimentsdf' (Id, Name, Price, Purchase_date) VALUES  (15, 'Lenovo ThinkPad P71', 6459, '2019-08-14') """


