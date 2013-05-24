from django.conf.urls import patterns, include, url
from weather.views import index, camp, camp_experiment, get_me_weather

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pyWeather.views.home', name='home'),
    # url(r'^pyWeather/', include('pyWeather.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    ('^$', index),
    ('^camp/', camp),
    ('^camp_exp/', camp_experiment),
    ('^weather/(-?\d+?\.\d+)/(-?\d+?\.\d+)/', get_me_weather),
    # (r'^(?P<zipcode>\d)/$', index),
    # (r'(?P<zipcode>\d)/', index),
    # (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/favicon.ico'}),

)
