unedited = open('Gaz_zcta_national.txt')
edited = open('editedzips.txt', 'w')
linecount = 0	

for line in unedited:
	if(linecount != 0):
		tempLine = line.split()
		edited.write(tempLine[0])
		edited.write(',')
		edited.write(tempLine[7])
		edited.write(',')
		edited.write(tempLine[8])
		edited.write('\n')
	linecount = linecount + 1

print "zipcodes prepared for SQLITE3"
print linecount, "lines processed"
	
