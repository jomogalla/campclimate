mysql -u $1 -p<<EOFMYSQL

USE woofwoof;

DROP TABLE IF EXISTS cities;
DROP TABLE IF EXISTS zipcodes;

CREATE TABLE IF NOT EXISTS cities(id INT PRIMARY KEY AUTO_INCREMENT, city VARCHAR(30), state VARCHAR(30), longitude DOUBLE, latitude DOUBLE);
CREATE TABLE IF NOT EXISTS zipCodes(id INT PRIMARY KEY AUTO_INCREMENT, longitude DOUBLE, latitude DOUBLE);

LOAD DATA LOCAL INFILE 'editedplaces.txt' 
INTO TABLE cities 
FIELDS TERMINATED BY '\t' 
LINES TERMINATED BY '\n' 
(id, city, state, longitude, latitude);

LOAD DATA LOCAL INFILE 'editedzips.txt' 
INTO TABLE zipCodes 
FIELDS TERMINATED BY '\t' 
LINES TERMINATED BY '\n' 
(id, longitude, latitude);

EOFMYSQL
