# from django.db.models import Q


#Could not decode to UTF-8 column 'phone' with text '303.697.6159CHARwasHEREbutWAScausingISSUES'
#serached for boulder co @ 35

import oracle

import re

from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render_to_response

# from django.shortcuts import render_to_response
# import models
from models import City
from models import Weather
from models import Zips
from models import Campground

from django import forms
from django.http import HttpResponse
from django.template import Context, loader

class WeatherForm(forms.Form):
	location = forms.CharField(error_messages={'required': 'required'})
	distance = forms.DecimalField(error_messages={'required': 'required'})
	# lessgreater = forms.BooleanField()

class bigWeatherForm(forms.Form):
	zipcode = forms.DecimalField(max_digits=5)
	distance = forms.DecimalField()
	population = forms.DecimalField()


def index(request):
	debug = []
	debug.append('False')
	citySet = []
	if request.method == 'GET':
		form = WeatherForm(request.GET)
		if form.is_valid():
			sampleZip = request.GET['location']
			maxDistance = int(request.GET['distance'])
			debug.append('maxdistance: ' + str(maxDistance))

			# switch here to use either the city or the zipcode
			debug.append('isThisAnInt: ' + str(isThisAnInt(sampleZip)))
			if len(str(sampleZip)) == 5 and isThisAnInt(sampleZip):
				try:
					centerLocation = Zips.objects.get(zipcode=sampleZip)
				except ObjectDoesNotExist:
					notification = 'No zipcode found :('
					return render_to_response('./index.html', {'form': form,'notification':notification, 'debug':debug})
			else:
				# assume we werent given a zipcode, so parse it as a city
				parsedZip = re.findall(r'\w+', sampleZip)
				cityName = ' '.join(parsedZip[0:-1])
				stateName = parsedZip[-1]
				debug.append(parsedZip)
				debug.append(cityName)
				debug.append(stateName)
				try:
					centerLocation = City.objects.get(name__iexact=cityName, state__iexact=stateName)
				except ObjectDoesNotExist:
					notification = 'No city found :('
					return render_to_response('./index.html', {'form': form,'notification':notification, 'debug':debug})
				# add 3rd except for multiple cites, return links to all of them! 
				# then do the search for the one they select!
			maxLat = centerLocation.latitude + maxDistance/69.09
			minLat = centerLocation.latitude - maxDistance/69.09
			maxLong = centerLocation.longitude + maxDistance/69.09
			minLong = centerLocation.longitude - maxDistance/69.09

			citySet = list(City.objects.filter(longitude__range=(minLong,maxLong)).filter(latitude__range=(minLat,maxLat)))

			# trim down the city list to a circle, and build the distance list
			cityDistances = []
			approvedCitySet = []
			debug.append('cities before: ' + str(len(citySet)))
			for city in citySet:
				tempDistance = calculateDistance(centerLocation, city)
				debug.append(city.name + ': ' + str(tempDistance))
				# debug.append(city.name + '- lat:' + str(city.longitude)  + ' long:' + str(city.latitude))
				if tempDistance < float(maxDistance):
					approvedCitySet.append(city)
					cityDistances.append(int(tempDistance))

			debug.append('cities after: ' + str(len(approvedCitySet)))
			debug.append('city distances: ' + str(len(cityDistances)))

			allTheForecasts = []
			for city in citySet:
				tempForecast = oracle.getForecast(city.latitude, city.longitude)
				#getting the day of the week for dates
				for datapoint in tempForecast:
					datapoint.day = datapoint.date.strftime('%A')
				#add forecast to forecast list
				allTheForecasts.append(tempForecast)

			zipped = [{'city': t[0], 'weather': t[1], 'distance': t[2]} for t in zip(approvedCitySet, allTheForecasts, cityDistances)]
			# zipped = [{'city': t[0], 'distance':t[1], 'weather': t[2]} for t in zip(citySet, cityDistances, allTheForecasts)]
			# debug.append(str(len(citySet)) + ' cities')
			return render_to_response('./index.html', {'city_list':citySet,"citylist_length":len(citySet), 'forecasts':allTheForecasts, 'form': form, 'zipped': zipped, 'debug':debug})
		else:
			debug.append('form data is invalid')
			form = WeatherForm(request.GET)
			return render_to_response('./index.html', {'form': form, 'debug':debug})

	else:
		debug.append('no GET request data')
		form = WeatherForm()
		return render_to_response('./index.html', {'form': form, 'debug':debug})


	# #GET THE CITIES
	# #DB ISSUE!!! latitudes & longitudes are crosswired...
	
	# #trim cities to cities in a circle(now theyre in a square)

	# #GET THE WEATHER	
	# allTheForecasts = []

	# # for city in squareCitySet:
	# # 	tempForecast = oracle.getForecast(city.longitude, city.latitude)
	# # 	allTheForecasts.append(tempForecast)

	# #need to simplify the weather array for STUPID TEMPLATES
	# #http://stackoverflow.com/questions/3132706/traversing-multiple-lists-in-django-template-in-same-for-loop


def camp(request):
	debug = []
	debug.append('False')
	citySet = []
	if request.method == 'GET':
		form = WeatherForm(request.GET)
		if form.is_valid():
			sampleZip = request.GET['location']
			maxDistance = int(request.GET['distance'])
			debug.append('maxdistance: ' + str(maxDistance))
			
			# switch here to use either the city or the zipcode
			if len(str(sampleZip)) == 5 and isThisAnInt(sampleZip):
				try:
					centerLocation = Zips.objects.get(zipcode=sampleZip)
				except ObjectDoesNotExist:
					notification = 'You sure that\'s a real zipcode?'
					return render_to_response('./camp.html', {'form': form,'notification':notification, 'debug':debug})
			else:
				# assume we werent given a zipcode, so parse it as a city
				parsedZip = re.findall(r'\w+', sampleZip)
				cityName = ' '.join(parsedZip[0:-1])
				stateName = parsedZip[-1]
				debug.append(parsedZip)
				debug.append(cityName)
				debug.append(stateName)
				try:
					centerLocation = City.objects.get(name__iexact=cityName, state__iexact=stateName)
				except ObjectDoesNotExist:
					# EVENTUALLY GIVE US A LIST OF CITIES!!!
					# AND SEARCH FOR ADDITIONAL TERMS TO MATCH, -CITY- ETC
					notification = 'I can\'t seem to find that city'
					return render_to_response('./camp.html', {'form': form,'notification':notification, 'debug':debug})

			maxLat = centerLocation.latitude + maxDistance/69.09
			minLat = centerLocation.latitude - maxDistance/69.09
			maxLong = centerLocation.longitude + maxDistance/69.09
			minLong = centerLocation.longitude - maxDistance/69.09

			campSet = list(Campground.objects.filter(longitude__range=(minLong,maxLong)).filter(latitude__range=(minLat,maxLat)))

			# trim down the city list to a circle, and build the distance list
			campDistances = []
			approvedCampSet = []
			debug.append('campgrounds before: ' + str(len(citySet)))
			for campground in campSet:
				tempDistance = calculateDistance(centerLocation, campground)
				debug.append(campground.name + ': ' + str(tempDistance))
				# debug.append(city.name + '- lat:' + str(city.longitude)  + ' long:' + str(city.latitude))
				if tempDistance < float(maxDistance):
					approvedCampSet.append(campground)
					campDistances.append(int(tempDistance))

			#format the campground type to be human friendly
			for campground in approvedCampSet:
				campground = campHumanizer(campground)

			debug.append('campgrounds after: ' + str(len(approvedCampSet)))
			debug.append('campground distances: ' + str(len(campDistances)))

			allTheForecasts = []
			for campground in approvedCampSet:
				tempForecast = oracle.getForecast(campground.latitude, campground.longitude)
				#getting the day of the week for dates
				for datapoint in tempForecast:
					datapoint.day = datapoint.date.strftime('%A')
				#add forecast to forecast list
				allTheForecasts.append(tempForecast)

			zipped = [{'campground': t[0], 'weather': t[1], 'distance': t[2]} for t in zip(approvedCampSet, allTheForecasts, campDistances)]
			# zipped = [{'city': t[0], 'distance':t[1], 'weather': t[2]} for t in zip(citySet, cityDistances, allTheForecasts)]
			# debug.append(str(len(citySet)) + ' cities')
			if len(approvedCampSet) > 0:
				return render_to_response('./camp.html', {"camplist_length":len(approvedCampSet), 'debug':debug, 'forecasts':allTheForecasts, 'form': form, 'zipped': zipped})
			else:
				notification = 'Search farther...'
				return render_to_response('./camp.html', {'form': form,'notification':notification, 'debug':debug})
		else:
			debug.append('form data is invalid')
			form = WeatherForm(request.GET)
			return render_to_response('./camp.html', {'form': form, 'debug':debug})

	else:
		debug.append('no GET request data')
		form = WeatherForm()
		return render_to_response('./camp.html', {'form': form, 'debug':debug})



# bug trimming wrong cities? seems to happen at 20 miles and not at 30 or 10
def calculateDistance(cityA, cityB):
	from math import sin, radians, cos, acos, degrees
	theDistance = (sin(radians(cityA.latitude)) * sin(radians(cityB.latitude)) +	cos(radians(cityA.latitude)) * cos(radians(cityB.latitude)) * cos(radians(cityB.longitude - cityA.longitude)))
	return degrees(acos(theDistance)*69.09)

def isThisAnInt(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def campHumanizer(campground):
	if campground.TYEP == 'NF':
		campground.TYEP = 'National Forest'
	elif campground.TYEP == 'SP':
		campground.TYEP = 'State Park'
	elif campground.TYEP == 'CP':
		campground.TYEP = 'City Park'
	elif campground.TYEP == 'BLM':
		campground.TYEP = 'Bureau of Land Management'
	elif campground.TYEP == 'NP':
		campground.TYEP = 'National Park'
	elif campground.TYEP == 'SRA':
		campground.TYEP = 'State Recreation Area'
	elif campground.TYEP == 'MIL':
		campground.TYEP = 'Military (No Public)'

	#format the amenities to be human friendly
	amenitiesList = campground.amenities.split()
	humanFriendlyAmenities = []
	for amenity in amenitiesList:
		# RV HOOKUPS
		if amenity == 'NH':
			humanFriendlyAmenities.append('Hookups: None')
		elif amenity == 'E':
			humanFriendlyAmenities.append('Hookups: Electric')
		elif amenity == 'W':
			humanFriendlyAmenities.append('Hookups: Water')
		elif amenity == 'S':
			humanFriendlyAmenities.append('Hookups: Sewer')
		elif amenity == 'WE':
			humanFriendlyAmenities.append('Hookups: Water Electric')
		elif amenity == 'ES':
			humanFriendlyAmenities.append('Hookups: Electric Sewer')
		elif amenity == 'WS':
			humanFriendlyAmenities.append('Hookups: Water Sewer')
		elif amenity == 'WES':
			humanFriendlyAmenities.append('Hookups: Water Electric Sewer')
		# Sanitary Dump
		elif amenity == 'DP':
			humanFriendlyAmenities.append('Sanitary Dump')
		elif amenity == 'ND':
			humanFriendlyAmenities.append('No Sanitary Dump')
		# Max RV Length --- 
		### NEEDS ADDRESSING
		### NOT JUST 32 FT but all sorts o' feet. 
		elif amenity == '32ft':
			humanFriendlyAmenities.append('32 feet')
		# Toilets
		elif amenity == 'FT':
			humanFriendlyAmenities.append('Flush Toilets')
		elif amenity == 'VT':
			humanFriendlyAmenities.append('Vault Toilets')
		elif amenity == 'FTVT':
			humanFriendlyAmenities.append('Flush & Vault Toilets')
		elif amenity == 'PT':
			humanFriendlyAmenities.append('Pit Toilets')
		elif amenity == 'NT':
			humanFriendlyAmenities.append('No Toilets')
		elif amenity == 'W':
			humanFriendlyAmenities.append('Water')
		#Drinking Water
		elif amenity == 'DW':
			humanFriendlyAmenities.append('Drinking Water')
		elif amenity == 'NW':
			humanFriendlyAmenities.append('No Drinking Water')
		# Showers
		elif amenity == 'SH':
			humanFriendlyAmenities.append('Showers')
		elif amenity == 'NS':
			humanFriendlyAmenities.append('No Showers')
		#  Reservations
		elif amenity == 'RS':
			humanFriendlyAmenities.append('Accepts Reservations')
		elif amenity == 'NR':
			humanFriendlyAmenities.append('No Reservations')
		# Pets
		elif amenity == 'PA':
			humanFriendlyAmenities.append('Pets Allowed')
		elif amenity == 'NP':
			humanFriendlyAmenities.append('No Pets Allowed')
		# Fee
		elif amenity == 'L$':
			humanFriendlyAmenities.append('Free or under $12')
		else:
			humanFriendlyAmenities.append(str(amenity))

	campground.amenities = humanFriendlyAmenities


# def calculateDistance(cityA, cityB):
# 	from math import sin, radians, cos, acos, degrees
# 	theDistance = (sin(radians(cityA.longitude)) * sin(radians(cityB.longitude)) +	cos(radians(cityA.longitude)) * cos(radians(cityB.longitude)) * cos(radians(cityB.latitude - cityA.latitude)))
# 	return int(degrees(acos(theDistance)) * 69.09)

	# sampleZip = 97306
	# distance = 10

	# centerLocation = Zips.objects.get(zipcode=sampleZip)
	# maxLat = centerLocation.latitude + distance/69.09
	# minLat = centerLocation.latitude - distance/69.09
	# maxLong = centerLocation.longitude + distance/69.09
	# minLong = centerLocation.longitude - distance/69.09

	# squareCitySet = City.objects.filter(longitude__range=(minLat,maxLat)).filter(latitude__range=(minLong,maxLong))
	# # t = loader.get_template('../templates/index.html')
	# # c = Context({'city_list':squareCitySet,"center_lat":centerLocation.latitude, "max_lat":maxLat, "min_lat":minLat, "citylist_length":len(squareCitySet), "forecasts":allTheForecasts})
	# # return HttpResponse(t.render(c))
	# return render_to_response('../templates/index.html', {'city_list':squareCitySet,"citylist_length":len(squareCitySet), "forecasts":allTheForecasts,})
	# # return render_to_response('../templates/index.html', {'city_list':squareCitySet,"center_lat":centerLocation.latitude, "max_lat":maxLat, "min_lat":minLat, "citylist_length":len(squareCitySet), "forecasts":allTheForecasts})

# HERE IS THE CODE FROM BETTERWEATHER THAT GETS THE CITIES, BITCH
#for(int i = 0; i < cityBeans.size(); i++)
# 	cityBeans.get(i).setDistance(calcDistance(centerLoc.getLatitude(), centerLoc.getLongitude(), cityBeans.get(i).getLatitude(), cityBeans.get(i).getLongitude()));
# 	if(cityBeans.get(i).getDistance() > distance){
# 		cityBeans.remove(i);
# 	}
# }
	# private int calcDistance(double latA, double longA, double latB, double longB)
		
	# {
	# 	//supposed to use earthradius in spherical law of cosines
	# 	//but 69.09 is the general distance of a latitude in n. america
	# 	//double earthRadius = 3959;
	# 	//casting to the int below didnt cause the 0 values bug mentioned above

	# 	//the spherical law of cosines
	# 	double theDistance = (Math.sin(Math.toRadians(latA)) *
	# 	Math.sin(Math.toRadians(latB)) +
	# 	Math.cos(Math.toRadians(latA)) *
	# 	Math.cos(Math.toRadians(latB)) *
	# 	Math.cos(Math.toRadians(longB - longA)));
	# 	return (int)(Math.toDegrees(Math.acos(theDistance)) * 69.09);
		
	# }

	# http://www.uscampgrounds.info/default.html
