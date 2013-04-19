import pygrib
import matplotlib.pyplot as plt
import numpy as np
from numpy import ma
from mpl_toolkits.basemap import Basemap
for grb in pygrib.open('../sampledata/ecmwf_tigge.grb'):
    if grb['parameterName'] == 'Soil moisture':
        fld = grb['values']
        lats,lons = grb.latlons()
        break

#from ncepgrib2 import Grib2Decode
#grbs = Grib2Decode('../sampledata/ecmwf_tigge.grb')
#grbx = grbs[14]
#fld = grbx.data()
#lats,lons = grbx.grid()

llcrnrlon = lons[0,0]
llcrnrlat = lats[0,0]
urcrnrlon = lons[-1,-1]
urcrnrlat = lats[-1,-1]
m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
            urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
            resolution='l',projection='cyl')
CS = m.contourf(lons,lats,fld,15,cmap=plt.cm.jet)
plt.colorbar(shrink=0.6)
m.drawcoastlines()
# draw parallels
delat = 30.
circles = np.arange(-90.,90.+delat,delat)
m.drawparallels(circles,labels=[1,0,0,0])
# draw meridians
delon = 60.
meridians = np.arange(0,360,delon)
m.drawmeridians(meridians,labels=[0,0,0,1])
plt.title(grb['parameterName']+' on ECMWF Reduced Gaussian Grid')
plt.show()
