from numpy.random import uniform

import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import pandas as pd
from plotFunction import plotFunc as pltF
from plotFunction import plot2Axis as pltF2
# to formate x axis date
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import os
#plt.ion()
#import earthpy as et


from netCDF4 import Dataset
from ncdump import ncdump


pathOrigo = "./../Files"
sessionPath = "10JAN04XU"
stationPath = "WETTZELL"
files = []
files.append("Met.nc")
files.append("TimeUTC")
data = []
data.append("AtmPres")
pathMet= pathOrigo+sessionPath+stationPath


metFile = Dataset(pathOrigo+"/10JAN04XU/WETTZELL/Met.nc","r",format="NETCDF4")
timeFile = Dataset(pathOrigo+"/10JAN04XU/WETTZELL/TimeUTC.nc","r",format="NETCDF4")
calCableFile = Dataset(pathOrigo+"/10JAN04XU/WETTZELL/Cal-Cable.nc","r",format="NETCDF4")
#print(calCableFile.variables)
calCable = calCableFile.variables["Cal-Cable"][:]
#print(calCable)
#print(metFile.variables)
#print(metFile.variables["AtmPres"][:])
pressure =  metFile.variables["AtmPres"][:]
seconds = timeFile.variables["Second"][:]
#YMDHM = timeFile.variables["YMDHM"][:]
#print(pressure.nc_inq_vartype)
nc_attrs, nc_dims, nc_vars = ncdump(metFile)

# Plot pressure
#plt.plot(pressure)
#plt.show()


#yearDim = timeFile.createDimension("yearDim",None)
#monthDim = timeFile.createDimension("monthDim",None)
#dayDim = timeFile.createDimension("dayDim",None)
#hourDim = timeFile.createDimension("hourDim",None)
#minuteDim = timeFile.createDimension("minuteDim",None)
#secondDim = timeFile.createDimension("secondDim",None)

#Y = rootgrp.createVariable("yearDim","f8",("yearDim",))
#M = rootgrp.createVariable("yearDim","f8",("yearDim",))
#D = rootgrp.createVariable("yearDim","f8",("yearDim",))
#H = rootgrp.createVariable("yearDim","f8",("yearDim",))
#Min = rootgrp.createVariable("yearDim","f8",("yearDim",))
#S = rootgrp.createVariable("yearDim","f8",("yearDim",))
#YMDHMS = timeFile.createVariable("temp","f4",("yearDim","monthDim","dayDim","hourDim","minuteDim","secondDim"))

#YMDHMS = timeFile.createVariable("year","month","day","hour","miute","second")
YMDHMS = []
for i in range(0,30):
    YMDHMS.append(pd.Timestamp(int(YMDHM[i][0]),int(YMDHM[i][1]),int(YMDHM[i][2]),int(YMDHM[i][3]),int(YMDHM[i][4]),int(seconds[i])))
    timeSF = 1
#pltF(calCable,pressure,0)
print(calCable)
# Define the date format for x lable
#myFmt = md.DateFormatter("%H:%M:%S")
#
#fig, ax =  plt.subplots()

"""
# plot pressure
plt.title("Pressure over time oberavation: 10 JAN 04 KOKEE ")
plt.plot(YMDHMS,pressure)
plt.ylabel('pressure');
"""
# plot calCable
#plt.title("calCable over time obsvervation: 10 JAN 04 KOKEE  ")
#plt.plot(YMDHMS,calCable)
#plt.ylabel('calCable');


#plt.xlabel('time');
#plt.xticks( rotation= 80 )
#ax.xaxis.set_major_formatter(myFmt);
#plt.show()



#index = pd.DatetimeIndex(['2014-07-04', '2014-08-04',
#                          '2015-07-04', '2015-08-04'])
#data = pd.Series([0, 1, 2, 3], index=index)


#time = pd.timedelta_range(0, periods=30, freq='S')
#print(time)

#Month = YMDHM[:][2]
#Day = YMDHM[:][3]
#Hour = YMDHM[:][4]
#Min = YMDHM[:][5]
#print(timeFile.variables)
#
#print(seconds)
#print(YMDHM)
#print(Year)
#print(YMDHM.shape)



#print(time.variables)


metFile.close()
timeFile.close()
