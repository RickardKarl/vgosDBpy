#import prettytable
from prettytable import PrettyTable as PT
from netCDF4 import Dataset
import pandas as pd
from numpy.random import uniform
import os

def read_var_content_float64(seekedData, pathToNetCDF, Time):
    with Dataset(pathToNetCDF,"r", format="NETCDF4_CLASSIC") as nc:
        data = nc.variables[seekedData][:]
        table = PT()
        table.field_names = [seekedData, "Index", "Time", "Data"]
        for i in range(len(data)):
            table.add_row([" ", i, Time[i], data[i]])
        table.get_string(title= seekedData)
        return table

def read_var_content_S1(seekedData,pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format= "NETCDF4_CLASSIC") as nc:
        data= nc.variables[seekedData][:]
        head = " "
        if len(data[:][1]) != 1:
            for i in range(len(data)):
                data_row = data[i]
                for column in data_row:
                    letter = column.decode('ASCII')
                    head += letter
        else:
            for column in data:
                letter = column.decode('ASCII')
                head += letter
        return head


def read_var_content(seekedData,pathToNetCDF,Time,dtype):
    #if dtype == "float64":
    #    return read_var_content_float64(seekedData,pathToNetCDF,Time)
    if dtype == "S1":
        return read_var_content_S1(seekedData, pathToNetCDF)
    else:
        return read_var_content_float64(seekedData,pathToNetCDF, Time)


def read_netCDF_vars(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        variables= []
        for var in vars:
            variables.append(var)
    return variables

def read_netCDF_vars_info(pathToNetCDF):
    info = ""
    vars = read_netCDF_vars(pathToNetCDF)
    dtypes = find_dtype(pathToNetCDF)
    for i in range(len(vars)):
        if dtypes[i] == "S1":
            info += read_var_content_S1(vars[i], pathToNetCDF) + "\n"
    return info


def find_dtype(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        dtype= []
        for var in vars:
            #for ncattr in var.ncattrs():
                #print(var.getncattr(ncattr))
            dtype.append(nc.variables[var].dtype)
    return dtype


def read_netCDF_dimension_for_var(var_name, pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        var = nc.variables[var_name]
        dim_name = var.get_dims()[0].name
    return dim_name
    
def possible_to_plot(pathToNetCDF):
    dtypes = find_dtype(pathToNetCDF)
    vars = read_netCDF_vars(pathToNetCDF)
    plotVars = []
    i=0;
    for i in range(len(dtypes)):#type in dtypes:
        if dtypes[i] != "S1":
            plotVars.append(vars[i])

    return plotVars
