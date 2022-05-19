The cleaning process is documented below with the exception of sensible data, such as students personal information, due to confidentiality, security and privacy issues.

#ETL Proccess
## Extracting available data
### Prior data
When the school provided the PDF documents, which were extracted from a free online form builder for school applications, my first action was to take a look in the very first pages of the first document and understand it. I realized that, instead of organized tables with information about the students, all data was stored in form-based PDFs. It was very look alike a printed document filled by each student separately. The main goal of keeping those documents were just records of students inscriptions, with no strategic business intent for that data.

Therefore, I've proposed a different pipeline for that data, that not only could escalate, enabling larger volumes of data, but also that allowed the school to catalogue, clean, filter, manipulate and analyze all that value informations to find the best business solutions.

###  Proposing a new way to store data
So, for a better comprehension of the available data, i've tried to create an organized table with all subscriptions information. Regardless any particularity of each student, they all filled the same form for submission, so I could easily identify the fields despite there was no obvious separators between fields. I've created lists to store these informations, according to the fields filled in the inscription form, and gathered them as columns of a dataframe.

## Transforming data
### Checking columns:
I started to clean the date, column by column. When it was possible, I've used automatic methods, but sometimes I had to contact administrative staff and other sources of research (such as Google search) to correct data errors or complete missing data fields. Some of them, such as birthday or address, were not possible to find, so it remained blank or, in case of calculating age, it was filled with the mean value.

Beside correcting typos, removing duplicates and filling blank fields, I also made data normalization to allow me to identify matches to apply functions properly and help me establishing standards for a consistent CRUD experience. Fields with multiple information, such as address, were split into various (address, city, postal code, etc.) for the benefit of a better analysis later. From the address field, I've extracted the latitude and longitude information. It was necessary to locate each student in the map graphic and estimate their distance from school.

Cleaning classes information was the most challenging step of the ETL. Many fields had typos or were filled improperly. The classes schedule also were non standardized as they've changed as enrollments were made and students requested minor time adjustments. Thus, there was no uniformity between courses and their respective schedules. I've mapped all those changes and left no blank field. Students that were enrolled in only one class, the fields referring to the second and third courses were filled with 0. These fields were replaced with null values, for later application in graphics.

The original dataframe was split into three: the first with the students personal information, the second containing data regarding their classes attended, and finally a last one with payment information. To the Students Dataframe, it was inserted four new columns (age, latitude, longitude and if the person lives in Toulouse or not). Those fields, extracted from other columns information, made easier to analyze personal data, as it would require less computer processing and make the process faster.

##  Exporting data
###  Setting data to export
Before saving and exporting data to the Database, I've created two additional dataframes based on the course and payments tables. They have the same columns, but no data attached and will be will be filled in the enrollment process for the next academic year. These enrollments will be made via a form that will automatically enter the data. All dataframes were saved as CSV files on my local environment before being uploaded to the MySQL server.

## Connecting to MySQL server through SSH Tunnel
I've chosen not to have my Database Server locally on my computer, since this database must be available for the web application and clients on the internet. Also, processing power and scalability are more reliable in cloud servers. 

Using Plataform As A Service (PAAS) on cloud, such as AWS Relational Database Service (RDS) or similar, would be more expensive due to their advanced features on scaling/backup/availability. Given the small size of this project, volume of data and probable growth of the database for the next year, would not justify the extra investment. Thus, the chosen solution was to use a virtual private server (VPS) that guarantees benefits over the location, and availabilty and is considerably cheaper than PAAS services mentioned above.

In order to increase the security of the DB server, its public access was disabled, and an SSH Tunnel was used to create a secure connection from the local computer to the remote server. I developed an extra function to first open an encrypted SSH tunnel and then use this connection to be able to reach the DB server.

Finally, once the connection is set, the process of uploading tables (creating or replacing them (if they already existed on the DB)), as well as extracting updated data for analysis was possible from both from my local computer and  also using the developed web applications.

# Web Applications
## CRUD Web Application
 Aiming to improve the ETL proccess from now on, it was developed a new registration form on a custom web application made with the library Streamlit. All the string fields were splitted and many examples of how each field should be filled were given, so there are less chances of inadequate filling. The classes and schedule choice, the most unpatterned fields, are now multiselect widgets.

After extracting all data, with this optmized process aiming to reduce the work of cleansing data, the application openas a SSH tunnel and connects to MySQL server. Then, it automatically updates all tables of the TB. The students table, which keeps information from all students, regardless if they are former students or not, search for the name provided. If there is already someone with that name in the table, it just updates its data. If its a newbie, it inserts a new row.

In the beggining of each school year, a new table is set for courses and payments. So, the information provided is inserted as a new role on the respective table of that year.

## Data Analysis Web Application
Also connected to the DB server, this application 





