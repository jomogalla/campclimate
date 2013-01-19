# -*- coding: utf-8 -*-

unedited = open('Gaz_places_national.txt')
edited = open('editedplacesNONUTF.txt', 'w')
linecount = 0	

for line in unedited:
	if linecount != 0:
		line = line.replace(',',' -')
		tempLine = line.split()
		#geoID
		edited.write(tempLine[1])
		edited.write(',')
		#city		
		# cityName = unicode(' '.join(tempLine[3:-11]))
		cityName = ' '.join(tempLine[3:-11])
		cityName = cityName.replace('á', 'a')
		cityName = cityName.replace('é', 'e')
		cityName = cityName.replace('í', 'i')
		cityName = cityName.replace('ó', 'o')
		cityName = cityName.replace('ü', 'u')
		cityName = cityName.replace('ñ', 'n')

		edited.write(cityName)
		edited.write(',')
		#state
		edited.write(tempLine[0])
		edited.write(',')
		#population
		edited.write(tempLine[-8])
		edited.write(',')
		#latitude
		edited.write(tempLine[-2])
		edited.write(',')
		#longitude
		edited.write(tempLine[-1])
		edited.write('\n')

	linecount = linecount + 1

print "places prepared for SQLITE"
print linecount, "lines processed"
	
