# EasyDataAnalyse 

### How to run the project:
```sh
- Clone projektet -> git clone https://github.com/MAHNAZ-KARIMI/EasyDataAnalyse.git

- Cd myproject

- pip3 install virtualenv

- virtualenv .venv 

 if you are in linux -> Cd .venv -> source ./Scripts/activate 
 if you are in terminal-> cd Scripts ->activate.bat> 
 
- pip install -r requirements.txt

- cd myproject -> python manage.py runserver

```  
  
 #### Django project run on: http://127.0.0.1:8000 
  
  
  
 ### How to import data to MYSQL using Docker
 
 Path: myproject\database
  
- docker-compose up

#### Mysql phpMyAdmin run on: http://127.0.0.1:8080

Path: myproject\

- docker cp Luk_Virksomhed_n.csv docker_db_1:/

- winpty docker exec -it docker_db_1 bash

- mysql -u root -p --local-infile

- use ervervsstyrelse;


---------------
### Create table Luk_Virksomhed manually or with this script: 
```sh
CREATE TABLE `Luk_Virksomhed` (`id` VARCHAR(256),`forloebVarighed` VARCHAR(256),`virkStartForloebsId` VARCHAR(256), 
                               `cvr` VARCHAR(256), `cvrIndberet` VARCHAR(256),`RID` VARCHAR(256), `PID` VARCHAR(256),
                               `serverTimeStamp` VARCHAR(256), `formURL` VARCHAR(256),`feltType` VARCHAR(256),
                               `feltId` VARCHAR(256), `feltNavn` VARCHAR(256), `handling` VARCHAR(256));
                               
```


### Importing Csv to mysql
```sh
LOAD DATA LOCAL INFILE 'Luk_Virksomhed_n.csv' INTO TABLE Luk_Virksomhed FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
```
### Modify some columns
```sh
UPDATE `Luk_Virksomhed` SET `handling` = REPLACE(`handling`, '\r', '');
UPDATE Luk_Virksomhed SET `feltType` = 'NONE' WHERE `feltType` = '';
UPDATE Luk_Virksomhed SET `feltId` = 'NONE' WHERE `feltId` = '';
UPDATE Luk_Virksomhed SET `feltNavn` = 'NONE' WHERE `feltNavn` = '';
UPDATE Luk_Virksomhed SET `PID` = 'NONE' WHERE `PID` = '';
UPDATE Luk_Virksomhed SET `RID` = 'NONE' WHERE `RID` = '';

```
-----------------------------

### Importing Csv to Drop-down menu
```sh

Csv files under path: myproject\myapp\analysisfolder\mainfolder\EasyData

```

