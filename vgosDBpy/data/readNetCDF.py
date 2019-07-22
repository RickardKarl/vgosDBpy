from netCDF4 import Dataset
import pandas as pd
from numpy.random import uniform
import os

from vgosDBpy.data.combineYMDHMS import combineYMDHMwithSec
from vgosDBpy.data.PathParser import findCorrespondingTime

#Actuallt used functions:

#used from outside this program
"""
Takes is a path to a netCDF file and a name of a variable and returns the varibales content.
"""
def getDataFromVar(path, var):
    with Dataset(path, "r", format="NETCDF4_CLASSIC") as nc:
        return(nc.variables[var][:])

"""
NOT USED FOR NOW BUT WELL
"""
def get_variable(pathToNetCDF, var):
    with Dataset(pathToNetCDF, 'r', format= 'NETCDF4_CLASSIC') as nc:
        return nc.variables[var]

"""
Takes in a path to a NetCDF file
Returns a header to a plot on the format: Station_name + Date
internal calls:
                read_var_content_S1(seekedData, path)
"""
def header_info_to_plot(path):
    #get date of session
    timePath = findCorrespondingTime(path)
    time = combineYMDHMwithSec(timePath)
    date = time[1].date()

    station = read_var_content_S1("Station", path) # Station is name of data that one seeks.
    return ( station + "   " + str(date) )

"""
Takes in: Path to NetCDF file
returns: an array containing all the variabls names for an netCDF file
"""
def read_netCDF_variables(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        variables= []
        for var in vars:
            variables.append(var)
    return variables

"""
Takes in: path to netCDF file and name of variable in file
Returns: True of variabele has dismension "NumScans" and d_type != S1
internal calls:
                read_netCDF_dimension_for_var(var, path)
                get_dtype_for_var(path, var)
"""
def is_possible_to_plot(path, var):
    dimension = read_netCDF_dimension_for_var(path, var)
    data_type = get_dtype_for_var(path,var)
    if dimension == "NumScans" and data_type != "S1" :
        return True
    else:
        return False

"""
Takes in: path to netCDF file amd name of var in file
Returns: True is varibale has dtype != S1 but is not plottable
Internal calls:
                get_dtype_for_var(path, var)
                read_netCDF_dimension_for_var(path,var)
"""
def is_var_constant(path, var):
    dtype = get_dtype_for_var(path, var)
    dimensions = read_netCDF_dimension_for_var(path, var)
    print(dimensions)
    #vars = read_netCDF_variables(path)
    if dtype != 'S1' and dimensions != "NumScans" :
        if dimensions != "NumObs":
            return True
    return False

"""
Takes in: path to netCDF file
Returns: a long string containing all the information stored in "S1" datatype vairbales in a netCDF file
internal Calls:
            read_netCDF_variables(path)
            find_dtype(path)
            read_var_content_S1(var, path)
"""
def read_netCDF_vars_info(pathToNetCDF):
    info = ""
    vars = read_netCDF_variables(pathToNetCDF)
    dtypes = find_dtype(pathToNetCDF)
    for i in range(len(dtypes)):
        if dtypes[i] == "S1":
            info += read_var_content_S1(vars[i], pathToNetCDF) + "\n"
    return info

def read_netCDF_data_info(pathToNetCDF):
    info= ''
    vars= read_netCDF_variables(pathToNetCDF)
    first = True
    for var in vars:
        # currently nor accepting 'Stublen'
        if is_var_constant(pathToNetCDF, var):
            if first is True:
                info = '\n \nVALUES STORED IN FILE: \n'
                first = False
            info += read_var_content_constant(pathToNetCDF, var) + '\n \n'
    return info


def find_dtype(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        dtype= []
        for var in vars:
            dtype.append(nc.variables[var].dtype)
    return dtype

def getDataFromVar_multDim(pathToNetCDF, var):
    return_data = []
    data = []
    with Dataset(pathToNetCDF, 'r', format= 'NETCDF4_CLASSIC') as nc:
        length = len(nc.variables[var.strip()].get_dims())
        for i in range(0, length):
            return_data.append(nc.variables[var.strip()][:,[i]])

        for j in range (0,length):
            temp = []
            data.append(nc.variables[var.strip()][:,[0]])
            r= nc.variables[var.strip()][:,[i]]
            print(len(r))
            #for i in range(0,len(r)):
                #temp.append(return_data[i,[j]])
                #temp.append(r[i])
            #data.append(temp)
        print(len(data))


#only used inside this file

"""
Takes in: path to netCDF file and the name of the variable that one is looking for.
Retuns the header of a netCDF file, meaning all the S1 vars as a long string.
Internal Calls:
                non
"""
def read_var_content_S1(seekedData,pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format= "NETCDF4_CLASSIC") as nc:
        data= nc.variables[seekedData][:]
        head = " "
        if len(data[:][0]) != 1:
            for i in range(len(data)):
                data_row = data[:][i]

                for column in data_row:
                    letter = column.decode('ASCII')
                    head += letter
        else:
            for column in data:
                letter = column.decode('ASCII')
                head += letter
        return head

def read_var_content_constant(pathToNetCDF, var):
    name = var
    with Dataset(pathToNetCDF, 'r', format = 'NETCDF4_CLASSIC') as nc:
        data= nc.variables[var][:]
        head = name +": \n"
        #print(head)
        #if len(data[0]) != 1:
        #    for i in range(len(data)):
        #        data_row = data[:][i]
        #
        #        for column in data_row:
        #            letter = str(column)
        #            head += letter
        #            print(head)
        #else:
        for column in data:
            letter = str(column)
            head += letter+ '    '
            #print(head)
        return head

"""
Takes in: path to netCDF file and name of specifik variable in netCDF file
returns: that vairbales dimemsions name
"""
def read_netCDF_dimension_for_var(pathToNetCDF, var):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        dimension = nc.variables[var].get_dims()[0].name
    return dimension

def read_unit_for_var (pathToNetCDF, var):
    with Dataset(pathToNetCDF, 'r', format= 'NETCDF4_CLASSIC') as nc:
        return nc.variables[var].Units

"""
Takes in: path to netCDF file and the name of a specific varibale in file
Returns: thr data type of that variable
"""
def get_dtype_for_var(path, var):
    with Dataset(path, "r", format = "NETCDF4_CLASSIC" ) as nc:
        return nc.variables[var].dtype



#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############

########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############
#########NOT USED############## 15/7 2019"##############

"""

#Takes in: a path to a NetCDF file
#Returns: all variables in a netCDF file that can be plotted versus time, mening they have same Dimension "Numscans" and data type !=  S1
#Internal calls:
#                find_dtype(path)
#                read_netCDF_vars(path)

def possible_to_plot(pathToNetCDF):
    dtypes = find_dtype(pathToNetCDF)
    vars = read_netCDF_vars(pathToNetCDF)
    timePath = findCorrespondingTime(pathToNetCDF)
    plotVars = []
    i=0;
    for i in range(len(dtypes)):#type in dtypes:
        if dtypes[i] != "S1" and len(vars[i]) == len(time):
            plotVars.append(vars[i])
    return plotVars


#wierd name, Takes in a path to netCDf file and a name to a variable in it
#returns an table containing the index, time and data for the given variable.

def read_var_content_float64(seekedData, pathToNetCDF): #NEVER USED, BORDE EJ FUNKA
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

"""
#Not really relevant for now I think

def read_var_content(seekedData,pathToNetCDF,Time,dtype):
    #if dtype == "float64":
    #    return read_var_content_float64(seekedData,pathToNetCDF,Time)
    if dtype == "S1":
        return read_var_content_S1(seekedData, pathToNetCDF)
    else:
        return read_var_content_float64(seekedData,pathToNetCDF, Time)


"""



"""
Reads in the data type for alla variables in a netCDF file and returns as an vector
"""


"""
currently only returning true if dimension is numscan
"""

"""
return an array of the data assosiated with an variable
"""


"""
def get_constants(path):
    dtype = find_dtype(path)
    dimensions = find_dimensions(path)
    vars = read_netCDF_variables(path)

    c = 0
    constants = []
    for var in vars :
        if dtype[c] != 'S1' and dimensions[c] != 'NumScans':
            constants.append(var)
        c += 1
    return constants


def get_constants_content(path):
    constants = get_constants(path)
    content= []
    for cont in constants:
        content.append(getDataFromVar(path, cont))
    return content
"""
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
"""
def get_data_constant(path, var):


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
       print((read_var_content(vars_in_file[i], path, YMDHMS, dtypes[i])))
"""
