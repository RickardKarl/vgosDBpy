import netCDF4
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

station = 'WETTZELL'
path = 'Data/10JAN19XA/' + station + '/'
met_observable = 'TempC' # RelHum, AtmPres, TempC

# Load netCDF files
file_met = netCDF4.Dataset(path + "Met.nc", "r", format="NETCDF4")
file_time = netCDF4.Dataset(path + "TimeUTC.nc", "r", format="NETCDF4")
file_cal_cable = netCDF4.Dataset(path + "Cal-Cable.nc", "r", format="NETCDF4")

# Retrieve different parameters
numScans = len(file_met.dimensions['NumScans'])

# Retrieve pressure
retrieved_data = file_met.variables[met_observable][:]

'''
for var in file_met.variables:
    print(var)
print('\n')
for var in file_time.variables:
    print(var)
'''
# Retrieve time information which needs formatting
YMDHM = file_time.variables['YMDHM'][:]
seconds = file_time.variables['Second'][:].astype(np.int16)

# Formatting dates (YMDHMS)
dates = []
for i in range(numScans):
    dates.append(pd.Timestamp(year = YMDHM[i][0], month = YMDHM[i][1],
                             day = YMDHM[i][2], hour = YMDHM[i][3],
                             minute = YMDHM[i][4], second = seconds[i]))



index = pd.DatetimeIndex(dates)
series_data = pd.Series(retrieved_data, index = index)
series_data = series_data['2010-01-19-17:20':'2010-01-20-17:30']
print(series_data)


series_data.plot(figsize = [10,8])
plt.title(met_observable + ' versus time between ' + str(dates[0]) + ' and ' + str(dates[-1]))
plt.ylabel(met_observable + ' [' + file_met.variables[met_observable].Units + ']')
plt.show()
