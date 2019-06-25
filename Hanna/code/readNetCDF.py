#import prettytable
from prettytable import PrettyTable as PT
from netCDF4 import Dataset
import pandas as pd
from numpy.random import uniform
from combineYMDHMS import combineYMDHMwithSec
import os

def read_var_content(seekedData,pathToNetCDF, Time,dtype):
    with Dataset(pathToNetCDF,"r", format="NETCDF4_CLASSIC") as nc:
        vars = nc.variables
        dataCol = vars[seekedData][:]
        if dtype == "float64" :
            table = PT()
            table.field_names= ["Index", "Time", "Data"]
            for i in range(len(dataCol)):
                table.add_row([i , Time[i], dataCol[i]])
            table.get_string(title=seekedData+ "the unit is" )
        elif dtype == "S1" :
            parts = []
            #table.field_names= ["Data",]
            for i in range(len(dataCol)):
                name = dataCol[i]
                parts = name.split("'")
                table.append(parts[1])
            #print(table.get_string(title="Hej"))
        else :
            table =[1]



    return table


def read_netCDF_vars(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        variables= []
        for var in vars:
            variables.append(var)
    return variables


def find_dtype(pathToNetCDF):
        with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
            vars= nc.variables
            dtype= []
            for var in vars:
                dtype.append(nc.variables[var].dtype)
        return dtype


path = "./../Files/10JAN04XU/KOKEE/Met.nc"
pathTime = "./../Files/10JAN04XU/KOKEE/TimeUTC.nc"
YMDHMS= combineYMDHMwithSec(pathTime)
vars_in_file  = read_netCDF_vars(path)
dtypes = find_dtype(path)
print(dtypes)
print(vars_in_file)
#print(iUTCinterval)
#print(read_var_content("CreateTime",path, YMDHMS, dtypes[1]))
for i in range(len(vars_in_file)):
    print((read_var_content(vars_in_file[i], path, YMDHMS, dtypes[-1])))
