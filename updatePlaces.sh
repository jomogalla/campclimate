#Python script that prepares the census data for SQLITE
python plshrink.py

#Safety's sake
#sqlite3 woofwoof "create table if not exists weather_city (geoid INTEGER PRIMARY KEY, latitude DOUBLE, longitude DOUBLE);"

sqlite3 woofwoof "delete from weather_city;"


#imports the census data
sqlite3 -separator ',' woofwoof ".import editedplaces.txt weather_city"
