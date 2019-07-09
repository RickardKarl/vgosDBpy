#import prettytable
from prettytable import PrettyTable as PT
from netCDF4 import Dataset
import pandas as pd
from numpy.random import uniform

from vgosDBpy.data.combineYMDHMS import combineYMDHMwithSec
from vgosDBpy.data.PathParser import findCorrespondingTime

import os


"""
wierd name, Takes in a path to netCDf file and a name to a variable in it
returns an table containing the index, time and data for the given variable.
"""
def read_var_content_float64(seekedData, pathToNetCDF):
    timePath = findCorrespondingTime(pathToNetCDF)
    Time= combineYMDHMwithSec(timePath)
    with Dataset(pathToNetCDF,"r", format="NETCDF4_CLASSIC") as nc:
        data = nc.variables[seekedData][:]
        table = PT()
        table.field_names = [seekedData, "Index", "Time", "Data"]
        for i in range(len(data)):
            table.add_row([" ", i, Time[i], data[i]])
        table.get_string(title= seekedData)
        return table
"""
Retuns the header of a net cdfFile
"""
def read_var_content_S1(seekedData,pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format= "NETCDF4_CLASSIC") as nc:
        data= nc.variables[seekedData][:]
        head = " "
        if len(data[:][0]) != 1:
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

def read_var_content_S1_header(seekedData, pathToNetCDF):
    header = ""
    if seekedData == 'Stub':
        header.append("File name : " + read_var_content_S1(seekedData, pathToNetCDF))
    if seekedData == 'CreateTime':
        header.append("File Created: " + read_var_content_S1(seekedData, pathToNetCDF))
    if seekedData == 'CreatedBy':
        header.append("Author : " + read_var_content_S1(seekedData, pathToNetCDF))
    if seekedData == 'Stub':
        header.append("File name: " + read_var_content_S1(seekedData, pathToNetCDF))


"""
Not really relevant for now I think
"""
def read_var_content(seekedData,pathToNetCDF,Time,dtype):
    #if dtype == "float64":
    #    return read_var_content_float64(seekedData,pathToNetCDF,Time)
    if dtype == "S1":
        return read_var_content_S1(seekedData, pathToNetCDF)
    else:
        return read_var_content_float64(seekedData,pathToNetCDF, Time)


"""
return an array containing all the variabls name for an netCDf file
"""
def read_netCDF_variables(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        variables= []
        for var in vars:
            variables.append(var)
    return variables


"""
Returns a long string containing all the information stored in "S1" datatype vairbales in a netCDF file
"""
def read_netCDF_vars_info(pathToNetCDF):
    info = ""
    vars = read_netCDF_variables(pathToNetCDF)
    dtypes = find_dtype(pathToNetCDF)
    for i in range(len(dtypes)):
        if dtypes[i] == "S1":
            info += read_var_content_S1(vars[i], pathToNetCDF) + "\n"
    return info

"""
Reads in the data type for alla variables in a netCDF file and returns as an vector
"""
def find_dtype(pathToNetCDF):
        with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
            vars= nc.variables
            dtype= []
            for var in vars:
                #for ncattr in var.ncattrs():
                    #print(var.getncattr(ncattr))
                dtype.append(nc.variables[var].dtype)
        return dtype

def find_dimensions(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        dims= []
        for var in vars:
            #for ncattr in var.ncattrs():
                #print(var.getncattr(ncattr))
            dims.append(nc.variables[var].get_dims()[0].name)
    return dims

def find_length(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        lengths= []
        for var in vars:
            #for ncattr in var.ncattrs():
                #print(var.getncattr(ncattr))
            lengths.append(len(nc.variables[var][:]))
    return lengths
def find_content(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        content= []
        for var in vars:
            #for ncattr in var.ncattrs():
                #print(var.getncattr(ncattr))
            content.append(getDataFromVar(pathToNetCDF,var))
    return content

"""
returns all variables in a netCDF file that can be plotted versus time, mening they have same Dimensions
and data type is not S1
"""

def possible_to_plot(pathToNetCDF):
    #pathh = "./../../../../Files/10JAN04XU/KOKEE/Met.nc"

    dtypes = find_dtype(pathToNetCDF)
    vars = read_netCDF_vars(pathToNetCDF)
    timePath = findCorrespondingTime(pathToNetCDF)
    plotVars = []
    i=0;
    for i in range(len(dtypes)):#type in dtypes:
        if dtypes[i] != "S1" and len(vars[i]) == len(time):
            plotVars.append(vars[i])
    return plotVars

"""
currently only returning true if dimension is numscan
"""

"""
return an array of the data assosiated with an variable
"""

def header_info_to_plot(path):
    #get date of session
    timePath = findCorrespondingTime(path)
    time = combineYMDHMwithSec(timePath)
    date = time[1].date()

    station = read_var_content_S1("Station", path)
    return ( station + "   " + str(date) )


def print_name_dtype_dim_length(pathToNetCDF):
    vars = read_netCDF_variables(pathToNetCDF)
    dtypes = find_dtype(pathToNetCDF)
    dims = find_dimensions(pathToNetCDF)
    lengths = find_length(pathToNetCDF)
    content = find_content(pathToNetCDF)
    s=""
    for i in range(0, len(vars)):
        print(vars[i])
        print(dtypes[i])
        print(dims[i])
        print(lengths[i])
        print(content[i])
        print("#####################")
    print(s)
#det get_info_from_var()

#path = "./../../Files/10JAN04XU/Apriori/Antenna.nc"
#print(read_netCDF_vars_info(path))

#path= "./../../../../Files/10JAN04XU/KOKEE/Met.nc"
#pathTime = "./../../../../Files/10JAN04XU/KOKEE/TimeUTC.nc"
#YMDHMS= combineYMDHMwithSec(pathTime)
#vars_in_file  = read_netCDF_variables(path)
#dtypes = find_dtype(path)
#print(vars_in_file)
#print(dtypes)


"""
#####################Methods assosiatedwith specifik var##############################
"""
def getDataFromVar(path, var):
    with Dataset(path, "r", format="NETCDF4_CLASSIC") as nc:
        return(nc.variables[var][:])

def read_netCDF_dimension_for_var(var_name, pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        var = nc.variables[var_name]
        dim_name = var.get_dims()[0].name
    return dim_name

def get_dtype_for_var(path, var):
    with Dataset(path, "r", format = "NETCDF4_CLASSIC" ) as nc:
        return nc.variables[var].dtype

def is_possible_to_plot(path, var):
    #dtypes = find_dtype(pathToNetCDF)
    #vars = read_netCDF_vars(pathToNetCDF)
    #timePath = findCorrespondingTime(pathToNetCDF)
    #plotVars = []
    #with Dataset(path, "r", format="NETCDF4_CLASSIC") as nc:
    dimension = read_netCDF_dimension_for_var(var, path)
    data_type = get_dtype_for_var(path,var)
    if dimension == "NumScans" and data_type != "S1" :
        return True
    else:
        return False
    #for i in range(len(dtypes)):#type in dtypes:
    #    if dtypes[i] != "S1" and len (vars[i]) == len(time):
    #        plotVars.append(vars[i])
    #return plotVars

#print(vars_in_file)
#print(read_netCDF_vars_info(path))

#print(dtypes)
#print(vars_in_file)

#for i in range(len(vars_in_file)):
#with Dataset(path, "r", format="NETCDF4_CLASSIC") as nc:
     #print(len(nc.variables[vars_in_file[12]]))
     #print(len(nc.variables[vars_in_file[13]]))
#     if dtypes[i] == "S1":
    #else:
#print(vars_in_file[StationList])
    #print(nc.variables["StationList"][:])
        #if vars_in_file[i]!= "StationList":
#        print((read_var_content(vars_in_file[i], path, YMDHMS, dtypes[i])))
