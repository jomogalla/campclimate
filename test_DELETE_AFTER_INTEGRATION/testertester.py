import oracle

# testList = [(44.942898,-123.035096),(45.523452,-122.676207),(44.052069,-123.086754),(44.058173,-121.31531)]

# returnedWeather = oracle.getForecasts(testList)

# i = 0
# for tempForecast in returnedWeather:
# 	print testList[i]
# 	for datapoint in tempForecast:
# 	    print datapoint.date.strftime('%a'),
# 	    print datapoint.conditions,
# 	    print datapoint.min_temp.value,
# 	    print datapoint.max_temp.value
# 	

tempForecast = oracle.getForecast(44.806944, -121.7875)


for datapoint in tempForecast:
    print datapoint.date.strftime('%a'),
    print datapoint.conditions,
    print datapoint.min_temp.value,
    print datapoint.max_temp.value