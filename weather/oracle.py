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
# all_the_forecasts = []

# # takes a list(latLongs) of lats & longs and returns the forecasts in a list(all_the_forecasts)
# for temp_lat_long in latLongs:
# 	tempForecast = forecast.daily_forecast_by_lat_lon(temp_lat_long[0], temp_lat_long[1])
# 	all_the_forecasts.append(tempForecast)

#I COULD POSSIBLY USE THIS TO RETURN READABLE DATA, FOR NOW, I SAY NO
# for datapoint in tempForecast:
#     print datapoint.date.strftime('%a'),
#     print datapoint.conditions,
#     print datapoint.min_temp.value,
#     print datapoint.max_temp.value
def get_forecast(latitude, longitude):
	return forecast.daily_forecast_by_lat_lon(latitude, longitude)


def get_forecasts(latLongs):
	all_the_forecasts = []

	for temp_lat_long in latLongs:
		tempForecast = forecast.daily_forecast_by_lat_lon(temp_lat_long[0], temp_lat_long[1])
		all_the_forecasts.append(tempForecast)

	return all_the_forecasts

# ADD A METHOD THAT CHECKS AN ARRAY/DB FOR REQUESTS IT HAS ALREADY PROCESSED WITHIN SOME TIME FRAME, AND JUST USE THOSE RESULTS