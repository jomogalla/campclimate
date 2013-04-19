from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

@dajaxice_register (method='GET')
def dajaxice_example(request):
    return simplejson.dumps({'message':'f ya'})

@dajaxice_register (method='GET')
def getMeWeather(request):
    return simplejson.dumps({'message':'f ya'})