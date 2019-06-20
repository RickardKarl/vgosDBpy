import netCDF4
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pprint

pp = pprint.PrettyPrinter()
session = '10JAN14XE'
path = 'Data/' + session + '/'
wrp_file1 = session + '_V005_iGSFC_kall.wrp'
wrp_file2 = session + '_V005_iGSFC_kngs.wrp'

wrapper1 = open(path+wrp_file1,'r')
wrapper2 = open(path+wrp_file2,'r')

stations_dir = {}
stations = []
for line in wrapper1:
    if line.startswith('Begin Station'):
        station_name = line.split(' ')[2].rstrip()
        stations.append(station_name)
        stations_dir[station_name] = [f for f in listdir(path + station_name + '/') if isfile(join(path + station_name + '/', f))]

#pp.pprint(stations_dir)

for i in stations:
    nc_file = netCDF4.Dataset(path + i + '/' + 'Cal-Cable.nc', "r", format="NETCDF4")
    cal_cable = nc_file['Cal-Cable'][:]
    plt.plot(cal_cable)
    #plt.show()
