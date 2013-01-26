
#            http://www.uscampgrounds.info/

# Didn't know where else to put this soooo here are the ammenities codes
# RV HOOKUPS:  (Some campgrounds listed with only "E" hookups may actually have additional hookups but we don't have specific data)
# NH=no hookups
# E, WE, WES=Water  Electric Sewer

# SANITARY DUMP: 
# DP=dump
# ND=no dump 

# MAX RV LENGTH: (may not be very accurate - call ahead if you have a long rig.) 
# 32ft=32 feet

# TOILETS: 
# FT=flush
# VT=vault 
# FTVT=some FT, some VT
# PT=pit
# NT= no toilets

# DRINKING WATER: 
# DW=drinking water at campground
# NW=no drinking water(bring your own) 

# SHOWERS: 
# SH=showers
# NS=no showers 

# RESERVATIONS: 
# RS=accepts reservations
# NR=no reservations
# Blank = unknown Reservations=no data on this 
# (Reservation phone and web site are always listed (if we have them) so you can check about reservations)

# PETS: 
# PA=pets allowed
# NP=no pets allowed 

# FEE: 
# L$=free or under $12

import csv

uneditedlist = ['NORTHWEST_CAMP.csv', 'BIGSKY_CAMP.csv', 'SOUTHWEST_CAMP.csv', 'CALIFORNIA_CAMP.csv', 'HOGBELT_CAMP.csv', 'CORNBELT_CAMP.csv', 'NORTHEAST_CAMP.csv', 'SOUTH_CAMP.csv']

edited = open('editedCamps.txt', 'w')

linecount = 0

for unedited in uneditedlist:
	with open('./campData/' + unedited, 'rb') as csvfile:
		campreader = csv.reader(csvfile)
		for row in campreader:
			linecount = linecount+1
			
			# print '**********CAMPGROUND NUMBER ' + str(linecount) + '**********'
			
			# adding a unique identifier
			edited.write(str(linecount))
			edited.write(',')


			# latitude
			edited.write(row[1])
			edited.write(',')
			# print row[1]

			#longitude
			edited.write(row[0])
			edited.write(',')
			# print row[0]

			# code
			edited.write(row[-9])
			edited.write(',')
			# print row[-9]

			# name
			edited.write(row[-8])
			edited.write(',')
			# print row[-8]

			# type
			edited.write(row[-7])
			edited.write(',')
			# print row[-7]

			# phone numbers
			# edited.write(row[-6].replace(' ', '').replace('-','.'))
			edited.write(row[-6].replace(' ', '').replace('\u00a0',''))
			edited.write(',')
			# print row[-6]

			# open dates
			edited.write(row[-5])
			edited.write(',')
			# print row[-5]

			# comments
			edited.write(row[-4])
			edited.write(',')
			# print row[-4]

			# number of sites
			edited.write(row[-3].replace(' ', ''))
			edited.write(',')
			# print row[-3]

			# elevation
			edited.write(row[-2].replace(' ', ''))
			edited.write(',')
			# print row[-2]

			# amenities
			edited.write(row[-1])
			edited.write('\n')
			# print row[-1]
			# print '\n'

print str(linecount) + ' lines processed'