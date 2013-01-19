import sys
import os

import noaa
from noaa import exceptions
from noaa import forecast
from noaa import utils

# latitude = 45.5236
# longitude = -122.6750


# latLong = latitude, longitude
# latLongs = []

# latLongs.append(latLong)
# allTheForecasts = []

# # takes a list(latLongs) of lats & longs and returns the forecasts in a list(allTheForecasts)
# for tempLatLong in latLongs:
# 	tempForecast = forecast.daily_forecast_by_lat_lon(tempLatLong[0], tempLatLong[1])
# 	allTheForecasts.append(tempForecast)

#I COULD POSSIBLY USE THIS TO RETURN READABLE DATA, FOR NOW, I SAY NO
# for datapoint in tempForecast:
#     print datapoint.date.strftime('%a'),
#     print datapoint.conditions,
#     print datapoint.min_temp.value,
#     print datapoint.max_temp.value
def getForecast(latitude, longitude):
	return forecast.daily_forecast_by_lat_lon(latitude, longitude)


def getForecasts(latLongs):
	allTheForecasts = []

	for tempLatLong in latLongs:
		tempForecast = forecast.daily_forecast_by_lat_lon(tempLatLong[0], tempLatLong[1])
		allTheForecasts.append(tempForecast)

	return allTheForecasts

# ADD A METHOD THAT CHECKS AN ARRAY/DB FOR REQUESTS IT HAS ALREADY PROCESSED WITHIN SOME TIME FRAME, AND JUST USE THOSE RESULTS