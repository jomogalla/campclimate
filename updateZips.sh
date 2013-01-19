#Python script that prepares the census data for SQLITE
python zcshrink.py

#Safety's sake
sqlite3 woofwoof "create table if not exists weather_zips (zipcode INTEGER PRIMARY KEY, latitude DOUBLE, longitude DOUBLE);"

sqlite3 woofwoof "delete from weather_zips;"


#imports the census data
sqlite3 -separator ',' woofwoof ".import editedzips.txt weather_zips"
