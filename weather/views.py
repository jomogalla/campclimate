# from django.db.models import Q


#Could not decode to UTF-8 column 'phone' with text '303.697.6159CHARACTER' it was character that caused problemos
#serached for boulder co @ 35

import oracle

import re

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from django.shortcuts import render_to_response

from django.template.loader import render_to_string

from django.utils import simplejson

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

class BigWeatherForm(forms.Form):
	zipcode = forms.DecimalField(max_digits=5)
	distance = forms.DecimalField()
	population = forms.DecimalField()


def index(request):
	debug = []
	debug.append('False')
	city_set = []
	if request.method == 'GET':
		form = WeatherForm(request.GET)
		if form.is_valid():
			sample_zip = request.GET['location']
			max_distance = int(request.GET['distance'])
			debug.append('max_distance: ' + str(max_distance))

			# switch here to use either the city or the zipcode
			debug.append('is_this_an_int: ' + str(is_this_an_int(sample_zip)))
			if len(str(sample_zip)) == 5 and is_this_an_int(sample_zip):
				try:
					center_location = Zips.objects.get(zipcode=sample_zip)
				except ObjectDoesNotExist:
					notification = 'No zipcode found :('
					return render_to_response('./index.html', {'form': form,'notification':notification, 'debug':debug})
			else:
				# assume we werent given a zipcode, so parse it as a city
				parsed_zip = re.findall(r'\w+', sample_zip)
				city_name = ' '.join(parsed_zip[0:-1])
				state_name = parsed_zip[-1]
				debug.append(parsed_zip)
				debug.append(city_name)
				debug.append(state_name)
				try:
					center_location = City.objects.get(name__iexact=city_name, state__iexact=state_name)
				except ObjectDoesNotExist:
					notification = 'No city found :('
					return render_to_response('./index.html', {'form': form,'notification':notification, 'debug':debug})
				# add 3rd except for multiple cites, return links to all of them! 
				# then do the search for the one they select!
			max_lat = center_location.latitude + max_distance/69.09
			min_lat = center_location.latitude - max_distance/69.09
			max_long = center_location.longitude + max_distance/69.09
			min_long = center_location.longitude - max_distance/69.09

			city_set = list(City.objects.filter(longitude__range=(min_long,max_long)).filter(latitude__range=(min_lat,max_lat)))

			# trim down the city list to a circle, and build the distance list
			city_distances = []
			approvedcity_set = []
			debug.append('cities before: ' + str(len(city_set)))
			for city in city_set:
				temp_distance = calculate_distance(center_location, city)
				debug.append(city.name + ': ' + str(temp_distance))
				# debug.append(city.name + '- lat:' + str(city.longitude)  + ' long:' + str(city.latitude))
				if temp_distance < float(max_distance):
					approvedcity_set.append(city)
					city_distances.append(int(temp_distance))

			debug.append('cities after: ' + str(len(approvedcity_set)))
			debug.append('city distances: ' + str(len(city_distances)))

			all_the_forecasts = []
			for city in city_set:
				tempForecast = oracle.get_forecast(city.latitude, city.longitude)
				#getting the day of the week for dates
				for datapoint in tempForecast:
					datapoint.day = datapoint.date.strftime('%A')
				#add forecast to forecast list
				all_the_forecasts.append(tempForecast)

			zipped = [{'city': t[0], 'weather': t[1], 'distance': t[2]} for t in zip(approvedcity_set, all_the_forecasts, city_distances)]
			# zipped = [{'city': t[0], 'distance':t[1], 'weather': t[2]} for t in zip(city_set, city_distances, all_the_forecasts)]
			# debug.append(str(len(city_set)) + ' cities')
			return render_to_response('./index.html', {'city_list':city_set,"citylist_length":len(city_set), 'forecasts':all_the_forecasts, 'form': form, 'zipped': zipped, 'debug':debug})
		else:
			debug.append('form data is invalid')
			form = WeatherForm(request.GET)
			return render_to_response('./index.html', {'form': form, 'debug':debug})

	else:
		debug.append('no GET request data')
		form = WeatherForm()
		return render_to_response('./index.html', {'form': form, 'debug':debug})

def get_me_weather(request, latitude, longitude):
	message = {"weatherHTML": ""}
	if request.is_ajax():
		forecast = oracle.get_forecast(latitude, longitude)
		weatherHTML = render_to_string('./forecast.html', {'weather':forecast})
		message['weatherHTML'] = weatherHTML
		json = simplejson.dumps(message)
		return HttpResponse(json, mimetype='application/json')

def camp(request):
	city_set = []
	if request.method == 'GET':
		form = WeatherForm(request.GET)
		if form.is_valid():
			sample_zip = request.GET['location']
			max_distance = int(request.GET['distance'])
			# debug.append('max_distance: ' + str(max_distance))
			
			# switch here to use either the city or the zipcode
			if len(str(sample_zip)) == 5 and is_this_an_int(sample_zip):
				try:
					center_location = Zips.objects.get(zipcode=sample_zip)
				except ObjectDoesNotExist:
					notification = 'You sure that\'s a real zipcode?'
					return render_to_response('./camp.html', {'form': form,'notification':notification})
			else:
				# assume we werent given a zipcode, so parse it as a city
				parsed_zip = re.findall(r'\w+', sample_zip)
				city_name = ' '.join(parsed_zip[0:-1])
				state_name = parsed_zip[-1]

				# BUG: searching for a city when there is another in the same state...possible major rewrite required to handle searching with extra data(no more jQuery hack)
				try:
					center_location = City.objects.get(name__iexact=city_name, state__iexact=state_name)
				#in case we get nothing 
				except ObjectDoesNotExist:
					try:	
						# concatenates the city and state name, if a city is two words, it mixes things up, this fixes that
						if len(state_name) > 2 and len(city_name) != 0:
							state_name = city_name + ' ' +state_name
						possibleCityList = City.objects.filter(name__iexact=state_name)
						if len(possibleCityList) != 0:
							notification = 'I didn\'t catch the state. Here\'s a list of cities to start with: ' 
							return render_to_response('./camp.html', {'form': form, 'notification':notification, 'possibleCityList':possibleCityList})
						else:
							notification = 'I can\'t find '
							notification += state_name
							return render_to_response('./camp.html', {'form': form, 'notification':notification})
					except ObjectDoesNotExist:
						notification = 'I can\'t seem to find that city'
						return render_to_response('./camp.html', {'form': form,'notification':notification})
				# in case we have two cities with the same name in the same state
				except MultipleObjectsReturned:
					# we get cities & populations but, cant specify the search based on the cities GEOid or location
					possibleCityList = City.objects.filter(state__iexact=state_name).filter(name__iexact=city_name)
					notification = 'I got multiple cities with that name: clicking these will just mess with things...sorry'
					sameCities = True
					return render_to_response('./camp.html', {'form': form,'notification':notification, 'sameCities':sameCities, 'possibleCityList':possibleCityList})
				# Handling Non UTF data that python hates
				except OperationalError:
					notification = 'I\'ve encountered non-UTF data. And am notifying my superiors\n Sorry about this'
					return render_to_response('./camp.html', {'form': form,'notification':notification})

			# gives us a minimum and maximum to search in, it would look like a square centered around center_location
			max_lat = center_location.latitude + max_distance/69.09
			min_lat = center_location.latitude - max_distance/69.09
			max_long = center_location.longitude + max_distance/69.09
			min_long = center_location.longitude - max_distance/69.09

			camp_set = list(Campground.objects.filter(longitude__range=(min_long,max_long)).filter(latitude__range=(min_lat,max_lat)))

			# trim down the city list to a circle, and build the distance list
			camp_distances = []
			approvedcamp_set = []
			for campground in camp_set:
				temp_distance = calculate_distance(center_location, campground)

				if temp_distance < float(max_distance):
					approvedcamp_set.append(campground)
					camp_distances.append(int(temp_distance))

			#format the campground type to be human friendly
			for campground in approvedcamp_set:
				campground = camp_humanizer(campground)

			all_the_forecasts = []
			for campground in approvedcamp_set:
				tempForecast = oracle.get_forecast(campground.latitude, campground.longitude)
				#getting the day of the week for dates
				for datapoint in tempForecast:
					datapoint.day = datapoint.date.strftime('%A')
				#add forecast to forecast list
				all_the_forecasts.append(tempForecast)

			zipped = [{'campground': t[0], 'weather': t[1], 'distance': t[2]} for t in zip(approvedcamp_set, all_the_forecasts, camp_distances)]

			# no campgrounds were returned....
			if len(approvedcamp_set) > 0:
				return render_to_response('./camp.html', {"camplist_length":len(approvedcamp_set), 'forecasts':all_the_forecasts, 'form': form, 'zipped': zipped})
			else:
				notification = 'Search farther...'
				return render_to_response('./camp.html', {'form': form,'farther':notification})
		else:
			form = WeatherForm(request.GET)
			return render_to_response('./camp.html', {'form': form})

	else:
		form = WeatherForm()
		return render_to_response('./camp.html', {'form': form})

def camp_experiment(request):
	city_set = []
	if request.method == 'GET':
		form = WeatherForm(request.GET)
		if form.is_valid():
			sample_zip = request.GET['location']
			max_distance = int(request.GET['distance'])
			
			# BUG: JOHN DAY OR 35 --returns non utf data

			# switch here to use either the city or the zipcode
			if len(str(sample_zip)) == 5 and is_this_an_int(sample_zip):
				try:
					center_location = Zips.objects.get(zipcode=sample_zip)
				except ObjectDoesNotExist:
					notification = 'You sure that\'s a real zipcode?'
					return render_to_response('./camp_experiment.html', {'form': form,'notification':notification})
			else:
				# assume we werent given a zipcode, so parse it as a city
				parsed_zip = re.findall(r'\w+', sample_zip)
				city_name = ' '.join(parsed_zip[0:-1])
				state_name = parsed_zip[-1]
				# BUG: searching two cities...possible major rewrite required to handle searching with extra(no more jQuery hack)
				try:
					center_location = City.objects.get(name__iexact=city_name, state__iexact=state_name)
				except ObjectDoesNotExist:
					try:	
						# concatenates the city and state name, if a city is two words, it mixes things up, this fixes that
						if len(state_name) > 2 and len(city_name) != 0:
							state_name = city_name + ' ' +state_name
						possibleCityList = City.objects.filter(name__iexact=state_name)
						if len(possibleCityList) != 0:
							notification = 'I didn\'t catch the state. Here\'s a list of cities to start with: ' 
							return render_to_response('./camp_experiment.html', {'form': form, 'notification':notification, 'possibleCityList':possibleCityList})
						else:
							notification = 'I can\'t find '
							notification += state_name
							return render_to_response('./camp_experiment.html', {'form': form, 'notification':notification})
					except ObjectDoesNotExist:
						notification = 'I can\'t seem to find that city'
						return render_to_response('./camp_experiment.html', {'form': form,'notification':notification})
				# in case we have two cities with the same name in the same state
				except MultipleObjectsReturned:
					# we get cities & populations but, cant specify the search based on the cities GEOid or location
					possibleCityList = City.objects.filter(state__iexact=state_name).filter(name__iexact=city_name)
					notification = 'I got multiple cities with that name beware: clicking these wont work'
					sameCities = True
					return render_to_response('./camp_experiment.html', {'form': form,'notification':notification, 'sameCities':sameCities, 'possibleCityList':possibleCityList})
				# Handling Non UTF data that python hates
				# except OperationalError:
					# notification = 'I\'ve encountered non-UTF data. And am notifying my superiors\n Sorry about this'
					# return render_to_response('./camp_experiment.html', {'form': form,'notification':notification})


			max_lat = center_location.latitude + max_distance/69.09
			min_lat = center_location.latitude - max_distance/69.09
			max_long = center_location.longitude + max_distance/69.09
			min_long = center_location.longitude - max_distance/69.09

			camp_set = list(Campground.objects.filter(longitude__range=(min_long,max_long)).filter(latitude__range=(min_lat,max_lat)))

			# trim down the city list to a circle, and build the distance list
			camp_distances = []
			approvedcamp_set = []
			for campground in camp_set:
				temp_distance = calculate_distance(center_location, campground)

				if temp_distance < float(max_distance):
					approvedcamp_set.append(campground)
					camp_distances.append(int(temp_distance))

			#format the campground type to be human friendly
			for campground in approvedcamp_set:
				campground = camp_humanizer(campground)

			# all_the_forecasts = []
			# for campground in approvedcamp_set:
				# tempForecast = oracle.get_forecast(campground.latitude, campground.longitude)
				#getting the day of the week for dates
				# for datapoint in tempForecast:
					# datapoint.day = datapoint.date.strftime('%A')
				#add forecast to forecast list
				# all_the_forecasts.append(tempForecast)

			zipped = [{'campground': t[0], 'distance': t[1]} for t in zip(approvedcamp_set, camp_distances)]
			
			if len(approvedcamp_set) > 0:
				return render_to_response('./camp_experiment.html', {"camplist_length":len(approvedcamp_set), 'form': form, 'zipped': zipped})
			else:
				notification = 'Search farther...'
				return render_to_response('./camp_experiment.html', {'form': form,'farther':notification})
		else:
			form = WeatherForm(request.GET)
			return render_to_response('./camp_experiment.html', {'form': form})

	else:
		form = WeatherForm()
		return render_to_response('./camp_experiment.html', {'form': form})


def calculate_distance(cityA, cityB):
	from math import sin, radians, cos, acos, degrees
	theDistance = (sin(radians(cityA.latitude)) * sin(radians(cityB.latitude)) +	cos(radians(cityA.latitude)) * cos(radians(cityB.latitude)) * cos(radians(cityB.longitude - cityA.longitude)))
	return degrees(acos(theDistance)*69.09)

def is_this_an_int(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

# FUTURE UPDATE: create a reference dictionary, simplifying this ugly ifelifelifelifelif
def camp_humanizer(campground):
	# print campground.name
	# US Federal Campgrounds
	if campground.TYEP == 'NP':
		campground.TYEP = 'National Park'
	elif campground.TYEP == 'NF':
		campground.TYEP = 'National Forest'
	elif campground.TYEP == 'BLM':
		campground.TYEP = 'Bureau of Land Management'
	elif campground.TYEP == 'TVA':
		campground.TYEP = 'Tennessee Valley Auth'
	elif campground.TYEP == 'COE':
		campground.TYEP = 'Army Corps of Engineers'
	elif campground.TYEP == 'NS':
		campground.TYEP = 'National Seashore'
	elif campground.TYEP == 'NRA':
		campground.TYEP = 'National Recreation Area'
	elif campground.TYEP == 'USFW':
		campground.TYEP = 'US Fish and Wildlife'
	elif campground.TYEP == 'WMA':
		campground.TYEP = 'Wildlife Management Area'
	elif campground.TYEP == 'MIL':
		campground.TYEP = 'Military (No Public)'
	elif campground.TYEP == 'COE':
		campground.TYEP = 'Corps of Engineers'
	elif campground.TYEP == 'BOR':
		campground.TYEP = 'Bureau of Reclamation'
	

	# US State
	elif campground.TYEP == 'SP':
		campground.TYEP = 'State Park'
	elif campground.TYEP == 'SF':
		campground.TYEP = 'State Forest'
	elif campground.TYEP == 'SRA':
		campground.TYEP = 'State Recreation Area'
	elif campground.TYEP == 'SPR':
		campground.TYEP = 'State Preserve'
	elif campground.TYEP == 'SB':
		campground.TYEP = 'State Beach'
	elif campground.TYEP == 'SPR':
		campground.TYEP = 'State Preserve'
	elif campground.TYEP == 'SFW':
		campground.TYEP = 'State Fish & Wildlife'

		# Other
	elif campground.TYEP == 'CP':
		campground.TYEP = 'City Park'
	elif campground.TYEP == 'UTIL':
		campground.TYEP = 'Utility-owned'
	elif campground.TYEP == 'RES':
		campground.TYEP = 'Native American Reservation'
	elif campground.TYEP == 'AUTH':
		campground.TYEP = 'Authority'

	#format the amenities to be human friendly
	amenitiesList = campground.amenities.split()
	humanFriendlyAmenities = []
	for amenity in amenitiesList:
		# RV HOOKUPS
		if amenity == 'NH':
			humanFriendlyAmenities.append('No Hookups')
		elif amenity == 'E':
			humanFriendlyAmenities.append('Electric Hookup')
		elif amenity == 'W':
			humanFriendlyAmenities.append('Water Hookup')
		elif amenity == 'S':
			humanFriendlyAmenities.append('Sewer Hookup')
		elif amenity == 'WE':
			humanFriendlyAmenities.append('Water & Electric Hookups')
		elif amenity == 'ES':
			humanFriendlyAmenities.append('Sewer & Electric Hookups')
		elif amenity == 'WS':
			humanFriendlyAmenities.append('Water & Sewer Hookups')
		elif amenity == 'WES':
			humanFriendlyAmenities.append('Water, Electric, & Sewer Hookups')
		# Sanitary Dump
		elif amenity == 'DP':
			humanFriendlyAmenities.append('Sanitary Dump')
		elif amenity == 'ND':
			humanFriendlyAmenities.append('No Sanitary Dump')
		# Max RV Length --- 
		elif amenity[-2:] == 'ft':
			humanFriendlyAmenities.append(amenity[:-2] + ' feet')
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
			humanFriendlyAmenities.append('Less than $12')
		elif amenity == 'N$':
			humanFriendlyAmenities.append('No Fee')
		else:
			humanFriendlyAmenities.append(str(amenity))

	campground.amenities = humanFriendlyAmenities

