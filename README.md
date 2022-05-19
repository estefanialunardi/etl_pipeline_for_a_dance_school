The cleaning process is documented below with the exception of sensible data, such as students personal information, due to confidentiality, security and privacy issues.

# Extracting available data
### Prior data
When the school provided those PDF documents, which were extracted from a free online form builder for school applications, my first action was to take a look in the very first pages of the first document and understand it. I realized that, instead of organized tables with information about the students, all data was stored in form-based PDFs. It was very look alike a printed document filled by each student separately. The main goal of keeping those documents were just records of students inscriptions, with no strategic business intent for that data.

Therefore, I've proposed a different pipeline for that data, that not only could escalate, enabling larger volumes of data, but also that allowed the school to catalogue, clean, filter, manipulate and analyze all that value informations to find the best business solutions.

###  Proposing a new way to store data
So, for a better comprehension of the available data, i've tried to create an organized table with all subscriptions information. Regardless any particularity of each student, they all filled the same form for submission, so I could easily identify the fields despite there was no obvious separators between fields.

The inscription form provides lots of information about each student. I created lists to store these informations, according to the fields filled.

All available data was stored in the same folder, and the files' name differ only by the number at the end of them, from 0 to the last.

###  Creating the dataframe
After extracting all the information avaialable on those forms, I've gathered them in a dataframe which columns are the fields from the submission form.

## Transforming data
### Checking columns:
I started to clean the date, column by column. When it was possible, I've used automatic methods, but sometimes I had to contact administrative staff and other sources of research (such as Google search) to correct data errors or complete missing data fields. Some of them, such as birthday or address, were not possible to find, so it remained blank or, in case of calculating age, it was filled with the mean value.

Beside correcting typos, removing duplicates and filling blank fields, I also made data normalization to allow me to identify matches to apply functions properly and help me establishing standards for a consistent CRUD experience. Fields with multiple information, such as address, were split into various (address, city, postal code, etc.) for the benefit of a better analysis later.

From the address field, I've extracted the latitude and longitude information. It was necessary to locate each student in the map graphic and estimate their distance from school.

Cleaning classes information was the most challenging step of the ETL. Many fields had typos or were filled improperly. The classes schedule also were non standardized as they've changed as enrollments were made and students requested minor time adjustments. Thus, there was no uniformity between courses and their respective schedules. I've mapped all those changes and left no blank field. Students that were enrolled in only one class, the fields referring to the second and third courses were filled with 0. These fields were replaced with null values, for later application in graphics.

The original dataframe was split into three: the first with the students personal information, the second containing data regarding their classes attended, and finally a last one with payment information.

To the Students Dataframe, it was inserted four new columns (age, latitude, longitude and if the person lives in Toulouse or not). Those fields, extracted from other columns information, made easier to analyze personal data, as it would require less computer processing and make the process faster.

##  Exporting data¶
###  Setting data to export
Before saving and exporting data to the Database, I've created two additional dataframes based on the course and payments tables. They have the same columns, but no data attached and will be will be filled in the enrollment process for the next academic year. These enrollments will be made via a form that will automatically enter the data.

All dataframes were saved as CSV files on my local environment before being uploaded to the MySQL server.

## Connecting to MySQL server through SSH Tunnel
I've chosen not to connect to the server on localhost, due to issues of security, reliability and processing capacity of the server, in addition to the possibility of having to scale this data.

However, hosting my hosting the server in the cloud would be much more expensive than necessary for the moment, given that the company is small and the volume of data would not justify this investment.

Thus, the chosen alternative was to use a virtual private server (VPS) that guarantees benefits over the location and is considerably cheaper than cloud services.

The most secure option found was to use a SSH tunnel from the local system to the server. So, I've created a function to open that encrypted connection with my server machine and connect to the MySQL server from remote.

Finally, I upload my tables to my database (create or replace, if they existed on the DB).

