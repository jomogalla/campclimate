#Python script that prepares the census data for SQLITE
python campShrink.py

#Safety's sake
#sqlite3 woofwoof "create table if not exists weather_city (geoid INTEGER PRIMARY KEY, latitude DOUBLE, longitude DOUBLE);"

sqlite3 woofwoof "delete from weather_campground;"


#imports the census data
sqlite3 -separator ',' woofwoof ".import editedCamps.txt weather_campground"
