import netCDF4
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

station = 'WETTZELL'
path = 'Data/10JAN19XA/' + station + '/'

# Load netCDF files
file_cal_cable = netCDF4.Dataset(path + "Cal-Cable.nc", "r", format="NETCDF4")

cal_cable = file_cal_cable.variables['Cal-Cable']
plt.plot(cal_cable[:])
plt.show()
