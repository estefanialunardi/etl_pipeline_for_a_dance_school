![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
[![Made withJupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter)](https://github.com/estefanialunardi/Projeto-Estrada-Real/blob/main/PROJETO%20ESTRADA%20REAL.ipynb)
<img src="https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white" />
<img src="https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=whitehttps://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white" />
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
<img src="https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white" />

[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://github.com/estefanialunardi/) 
[<img src='https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white' />](https://www.linkedin.com/in/estefania-mesquita)

# Data Dance (Or ETL Pipeline for a Ballet School)
<img src="https://user-images.githubusercontent.com/101064720/169435791-1aa00813-e987-4ff1-a4ad-d493f23f1c0e.jpg" width="390" align="right">
Seeking to optimize the data collection system of a ballet school, an ETL pipeline was developed to optimize all company's data processes, ensuring usability and storage in a safe and accessible place.


As there was no systematized process, the entire pipeline was developed from the very beggining according to the requests of the school's administration, seeking solutions that suited the profile of both the students (to provide data) and the administration (for access and analysis of the data).

Thus, a relational database was created, hosted remotely on a Virtual Private Server (VPS), which is powered and accessed by intuitive and user-friendly web applications.

All the code was written in Python, both in Jupyter Notebook, for the primary extraction of data and creation of the base that will be updated by the web applications, and in Visual Studio Code, where these applications were created.

The process is documented in this repository with the exception of sensible data, such as students' personal information, due to confidentiality, security and privacy issues.

# Libraries
<table align="center">
    <tr>
        <td>Pdfplumber</td>
        <td>Requests</td>
        <td>Pandas</td>
        <td>Os</td>
      <td>Sshtunnel</td>
        <td>Dotenv</td>
<td>Selenium</td>
    </tr>
     <tr>
        <td>Dateutil</td>
      <td>SQLAlchemy</td>
        <td>Plotly</td>
        <td>Pymysql</td>
        <td>Streamlit</td>
       <td>Datetime</td>
        <td>Geopy.geocoders</td>
  </tr>
</table>

# ETL Proccess
## Extracting available data
<img src="https://user-images.githubusercontent.com/101064720/169434647-b51bee4e-2508-49c3-9098-656ca5c8274c.jpg" width="300" align="left">

When the school provided the PDF documents, which were extracted from a free online form builder for school applications, my first action was to take a look in the very first pages of the first document and understand it. I realized that, instead of organized tables with information about the students, all data was stored in form-based PDFs. It was very look alike a printed document filled by each student separately. The main purpose of keeping those documents was to keep records of student's enrollments, with no strategic business intent for that data.

Therefore, I've proposed a different pipeline for that data, that not only could escalate, enabling larger volumes of data, but also that allowed the school to catalogue, clean, filter, manipulate and analyze all that value informations to find the best business solutions.

###  Proposing a new way to store data
So, for a better comprehension of the available data, i've tried to create an organized table with all subscriptions information. Regardless any particularity of each student, they all filled out the same form for submission, so I could easily identify the fields despite there was no obvious separators between fields. I've created lists to store these informations, according to the fields filled out in the inscription form, and gathered them as columns of a dataframe.


## Transforming data 

### Checking columns:
<img src="https://user-images.githubusercontent.com/101064720/169436300-9ef13936-7fc3-4a32-bdf4-9c7d68c83076.PNG" width="300" align="right">
I started to clean the date, column by column. When it was possible, I've used automatic methods, but sometimes I had to contact administrative staff and other sources of research (such as Google search) to correct data errors or complete missing data fields. Some of them, such as birthday or address, were not possible to find, so it remained blank or was filled out with the mean value (age field).

Besides correcting typos, removing duplicates and and filling out blank fields, I also made data normalization to allow me to identify matches to apply functions properly and help me establishing standards for a consistent CRUD experience. Fields with multiple information, such as address, were split into various (address, city, postal code, etc.) for the benefit of a better analysis later. From the address field, I've extracted the latitude and longitude information. It was necessary to locate each student in the map graphic and estimate their distance from school.

Cleaning classes information was the most challenging step of the ETL. Many fields had typos or were filled out improperly. The classes schedule also were non standardized as they've changed as registrations were made and students requested minor time adjustments. Thus, there was no uniformity between courses and their respective schedules. I've mapped all those changes and left no blank field. Students that were enrolled in only one class, the fields referring to the second and third courses were filled out with 0. These fields were replaced with null values, for later application in graphics.

The original dataframe was split into three: the first with the students' personal information, the second containing data regarding their classes attended, and finally a last one with payment information. To the Students Dataframe, it was inserted four new columns (age, latitude, longitude and if the person lives in Toulouse or not). Those fields, extracted from other columns information, made easier to analyze personal data, as it would require less computer processing and make the process faster.

##  Exporting data
###  Setting data to export
Before saving and exporting data to the Database, I've created two additional dataframes based on the course and payments tables. They have the same columns, but no data attached and will be will be filled out in the registration process for the next academic year. These registrations will be made via a form that will automatically enter the data. All dataframes were saved as CSV files on my local environment before being uploaded to the MySQL server.

## Connecting to MySQL server through SSH Tunnel
I've chosen not to have my Database Server locally on my computer, since this database must be available for the web application and clients on the internet. Also, processing power and scalability are more reliable in cloud servers. 

Using Plataform As A Service (PAAS) on cloud, such as AWS Relational Database Service (RDS) or similar, would be more expensive due to their advanced features on scaling/backup/availability. Given the small size of this project, volume of data and probable growth of the database for the next year, the extra investment would not be necessary. Thus, the chosen solution was to use a virtual private server (VPS) that guarantees benefits over the location, and availabilty and is considerably cheaper than PAAS services mentioned above.

In order to increase the security of the DB server, its public access was disabled, and an SSH Tunnel was used to create a secure connection from the local computer to the remote server. I developed an extra function to first open an encrypted SSH tunnel and then use this connection to be able to reach the DB server.

Finally, once the connection is set, the process of uploading tables (creating or replacing them (if they already existed on the DB), as well as extracting updated data for analysis is possible from both from my local computer and also using the developed web applications.

# Web Applications
## CRUD Web Application
 <img src="https://user-images.githubusercontent.com/101064720/171775534-65b253f6-1c58-4199-8d9b-0b30187b27ae.gif" width="800" align="center" type="gif">

Aiming to improve the ETL proccess from now on, it was developed a new registration form on a custom web application made with the library Streamlit. All the string fields were splitted and many examples of how each field should be filled out were given, so there are less chances of inadequate filling out. The classes and schedule choice, the most unpatterned fields, are now multiselect widgets.
  
After extracting all data, with this optmized process aiming to reduce the work of cleansing data, the application openas a SSH tunnel and connects to MySQL server. Then, it automatically updates all tables of the TB. The students table, which keeps information from all students, regardless if they are former students or not, search for the name provided. If there is already someone with that name in the table, it just updates its data. If its a new student, it inserts a new row.

In the beggining of each school year, a new table is set for courses and payments. So, the information provided is inserted as a new role on the respective table of that year.

In the same applications, students can schedule their Pilates Classes and enroll in Masterclasses, Stages and Ateliers.

## Data Analysis Web Application
 <img src="https://user-images.githubusercontent.com/101064720/171774736-81055c0a-620b-4a50-a0ea-c32dc2a86d98.gif" width="800" align="center" type="gif">
 
Also connected to the DB server, this application was developed to select, manipulate and analize data. All the queries and specific SQL commands to retrieve the information requested by the school's administration were made directly in Python, using SQLAlchemy library. 

It also allows the user to resarch for specific data from students and update their payment status. It's necessary to log in to access this content.


# Analyzed data
For a better understanding of the school's target audience, questions regarding the students' profile were evaluated - both in personal matters and in their class preferences.

## Who are they?
The most frequent age group is children. 40% of students are under 12 years old. Adolescents (13 to 17) represent 9% of those enrolled. Adults (from 18 to 62 years old) also account for 40% of the total. The other 10% are made up of elderly people up to 75 years old.
<img src="https://user-images.githubusercontent.com/101064720/169437408-e09176e7-072a-4ce9-9837-0ee92ac7f107.gif" width="800" align="center" type="gif">

Although they are the proportionally most significant age group in the school, children are divided between the courses they most attend. Children's classes have an average of 7 students per class(Éveil, Initiation and Préparatoire). Older children also participate in other courses, with teenagers mainly, such as the PBT, Classique 1 and Classique 2.

Among the courses aimed at all age groups, the classes of Classique Moyen and Classique Intermediére are the most attended.

Most students take only one class - children in particular do not tend to take two different courses. Proportionally, the Pointes course is the one that most receives students who take more than one class.

<img src="https://user-images.githubusercontent.com/101064720/169437161-9560caee-65cd-4cd0-9864-bb81593a984f.png" width="750" align="center">

<img src="https://user-images.githubusercontent.com/101064720/169437261-1963e9ce-7019-4719-88ec-b8100547640a.png" width="750" align="center">

## Where do they live?

90% of students live in Toulouse, the city where the school is based. In addition, it is possible to observe that most students live extremely close to the school, some even on the same block.

<img src="https://user-images.githubusercontent.com/101064720/169438360-7fc46527-8574-4a23-b705-a5719d7fc29b.pn" width="750" align="center">

<img src="https://user-images.githubusercontent.com/101064720/169437344-13e64119-610f-491b-98c1-da08547f5a9b.png" width="750" align="center">

## How do they pay?
Students prefer to pay in one or three installments. Those who take three or more courses, in general, pay in one go. In terms of income, the biggest sums come from those who take one or three classes. Proportionally, the 3-lesson package is the most profitable for the school.
<img src="https://user-images.githubusercontent.com/101064720/169438710-d311df41-f48d-47e3-b3db-532c3cfa78f9.jpg" width="750" align="center">
<img src="https://user-images.githubusercontent.com/101064720/169438702-c4b8702c-9ec8-49df-a804-fce821a3803b.jpg" width="750" align="center">

Thank you!




