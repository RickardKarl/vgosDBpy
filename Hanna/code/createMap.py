# create combination of data and name

from readNetCDF import read_var_content, possible_to_plot
from prettytable import PrettyTable as PT
from netCDF4 import Dataset
import pandas as pd
from numpy.random import uniform
from combineYMDHMS import combineYMDHMwithSec
import os
def createM (path)
    #path = "./../../../../Files/10JAN04XU/KOKEE/Met.nc"
    map = {}
    names = possible_to_plot(path)
    content= []
    with Dataset(path, "r", format= "NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        for var in vars:
            if var in names:
                map[var] = nc.variables[var][:]

    return map
