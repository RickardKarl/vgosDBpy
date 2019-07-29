from netCDF4 import Dataset
import pandas as pd
from numpy.random import uniform
import os
import matplotlib.pyplot as plt
import numpy as np


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
    if timePath != '':
        time = combineYMDHMwithSec(timePath)
        date = time[1].date()
        station = read_var_content_S1("Station", path) # Station is name of data that one seeks.
        return ( station + "   " + str(date) )
    else:
        return ('')

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
    if dimension.strip() == "NumScans" or dimension.strip() == 'NumObs' and data_type != "S1"  :
        return True
    else:
        return False

def is_Numscans(path, var):
    with Dataset(path, 'r', format = 'NETCDF4_CLASSIC') as nc:
        dimensions = nc.variables[var].get_dims()
        for dim in dimensions:
            name = dim.name
            if name.strip() == 'NumScans':
                return True
    return False

def is_NumsSation(path,var):
    with Dataset(path, 'r', format = 'NETCDF4_CLASSIC') as nc:
        dimensions = nc.variables[var].get_dims()
        for dim in dimensions:
            name = dim.name
            if name.strip() == 'NumStation':
                return True
    return False

def is_NumObs(path, var):
    with Dataset(path, 'r', format = 'NETCDF4_CLASSIC') as nc:
        dimensions = nc.variables[var].get_dims()
        for dim in dimensions:
            name = dim.name
            if name.strip() == 'NumObs':
                return True
    return False

def is_numScan_or_NumObs(path, var):
    if is_Numscans(path,var):
        return True
    if is_NumObs(path,var):
        return True
    return False

def show_in_table(path,var):
    if is_Numscans(path,var):
        return True
    elif is_NumObs(path,var):
        return True
    elif is_NumsSation(path,var):
        return True
    else :
        return False
def read_all_dimensions_for_var(path, var):
    with Dataset(path, 'r', format = 'NETCDF4_CLASSIC') as nc:
        return nc.variables[var].get_dims()
"""
Takes in: path to netCDF file amd name of var in file
Returns: True is varibale has dtype != S1 but is not plottable
Internal calls:
                get_dtype_for_var(path, var)
                read_netCDF_dimension_for_var(path,var)
"""
def is_var_constant(path, var):
    dtype = get_dtype_for_var(path, var)
    if is_numScan_or_NumObs(path,var):
        return False
    else:
        if dtype != 'S1':
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
    for i in range(len(vars)):
        if not is_numScan_or_NumObs(pathToNetCDF, vars[i]):
            if dtypes[i] == 'S1' :
                #if not is_numScan_or_NumObs(pathToNetCDF, vars[i]):
                info += vars[i] +':'+  read_var_content_S1(vars[i], pathToNetCDF) + "\n \n"
            else:
                info += read_var_content_constant(pathToNetCDF, vars[i]) + '\n \n '

    return info
"""
def read_netCDF_data_info(pathToNetCDF):
    info= ''
    vars= read_netCDF_variables(pathToNetCDF)
    dtypes = find_dtype(pathToNetCDF)
    first = True
    i = 0
    for var in vars:
        # currently nor accepting 'Stublen'
        if  not is_numScan_or_NumObs(pathToNetCDF, var) and dtypes[i] is not 'S1':
            if i == 0:
                info = '\n \nVALUES STORED IN FILE: \n'
            info += read_var_content_constant(pathToNetCDF, var) + '\n \n'
        i += 1
    return info
"""

def not_S1(paths, vars):
    for i in range(len(paths)):
        with Dataset(paths[i], 'r', format = 'NETCDF4_CLASSIC') as nc:
            dtype = nc.variables[vars[i]].dtype.name
            if dtype.strip() == 'S1':
                return False
    return True

def find_dtype(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        dtype= []
        for var in vars:
            dtype.append(nc.variables[var].dtype)
    return dtype

def get_dtype_var(path, var):
    with Dataset(path,'r', format = 'NETCDF4_CLASSIC') as nc:
        return str(nc.variables[var].dtype)

#only used inside this file

"""
Takes in: path to netCDF file and the name of the variable that one is looking for.
Retuns the header of a netCDF file, meaning all the S1 vars as a long string.
Internal Calls:
                non
"""
def read_var_content_S1(seekedData,pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format= "NETCDF4_CLASSIC") as nc:

        dimensions = nc.variables[seekedData].get_dims()
        lengths = []
        for dim in dimensions:
            lengths.append(len(dim))

        data= getDataFromVar(pathToNetCDF, seekedData)

        head = " "

        if len(lengths) == 2:
            for i in range(len(data)):
                data_row = data[:][i]

                for column in data_row:
                    letter = column.decode('ASCII')
                    head += letter

        elif len(lengths) == 3:
            for i in range(lengths[0]):
                for j in range(lengths[1]):
                    for k in range(lengths[2]):
                        letter = data[i,j,k].decode('ASCII')
                        head += letter
        else: # meining defualt 1
            for column in data:
                letter = column.decode('ASCII')
                head += letter
        return head

def read_var_content_constant(pathToNetCDF, var):
    name = var
    with Dataset(pathToNetCDF, 'r', format = 'NETCDF4_CLASSIC') as nc:
        data= nc.variables[var][:]
        head = name +": \n"
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
        dtype = nc.variables[var].dtype
        if dtype.name.strip() != 'S1':
            #return nc.variables[var].Units
                return 'UNITTTTTT'
        else:
             return ''

def get_data_to_table(pathToNetCDF, var):
    dtype = get_dtype_for_var(pathToNetCDF, var)
    dims_len = get_len_dims(pathToNetCDF, var)
    dim = read_netCDF_dimension_for_var(pathToNetCDF,var)
    #print('Dims='+ str(dims))
    print(dtype)
    #print('vs')
    #print(get_dtype_for_var(pathToNetCDF,var))
    #print(var)
    if var.strip() == 'Baseline':
        print('enter 1')
        y = get_dataBaseline(pathToNetCDF)
    elif dim.strip() == 'NumStation' and dtype == 'S1':
        y = get_NumStation_S1_table(pathToNetCDF, var)
    elif dims_len != 1:
        y = getDataFromVar_multDim(pathToNetCDF, var)
        print('enter 2')
    elif dtype == 'S1' :
        print('enter 3')
        y = get_S1_tableData(pathToNetCDF, var)
    #elif dtype == 'bytes8':
    #    y =  get_bytes8_tableData(pathToNetCDF, var)
    #    print('enter 4')
    else:
        y = getDataFromVar_table(pathToNetCDF, var)
        print('enter 5')
    print(len(y))
    print(len(y[0]))
    #return y[0]
    return y


def get_S1_tableData(pathToNetCDF, var):
    return_data = []
    data = []
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        data= nc.variables[var][:]
        for line in data:
            temp = ''
            for letter in line:
                temp += letter.decode('ASCII')
            data.append(temp)
        return_data.append(data)
    return return_data
#def get_NumStation_table

def get_NumStation_S1_table(pathToNetCDF,var):
    table = []
    return_data  = []
    with Dataset(pathToNetCDF, 'r', format= 'NETCDF4_CLASSIC') as nc:
        dimensions= nc.variables[var].get_dims()
        content = getDataFromVar(pathToNetCDF,var)
        length = []
        for dim in dimensions:
            length.append(len(dim))
        for i in range(length[0]):#len(dimensions[0]):
            temp = ''
            for j in range(length[1]):
            #for k in range(length[2]):
                #print(k)
                temp += content[i,j].decode('ASCII')
            temp += '  '
            table.append(temp)
            return_data.append(table)
    return return_data

def get_bytes8_tableData(pathToNetCDF, var):
    return_data = []
    data = []
    with Dataset(pathToNetCDF, 'r', forma = 'NETCDF4_CLASSIC') as nc:
        data_var = nc.variables[var][:]
        for line in data :
            temp = ''
            for byte in line:
                temp += str(byte)
            data.append(temp)
        return_data.append(data)
    return return_data

def getDataFromVar_table(path, var):
    return_data = []
    with Dataset(path, "r", format="NETCDF4_CLASSIC") as nc:
        return_data.append(nc.variables[var][:])
        print(return_data)
        return(return_data)

def getDataFromVar_multDim(pathToNetCDF, var):
    return_data = []
    with Dataset(pathToNetCDF, 'r', format= 'NETCDF4_CLASSIC') as nc:
        length = len(nc.variables[var.strip()].get_dims())
        for i in range (0,length):
            dtype = nc.variables[var.strip()][:,[i]].dtype
            print(nc.variables[var.strip()][:,[i]].dtype)
            if dtype == 'S1':
                data_var= nc.variables[var][:,[i]]
                data= []
                for line in data_var:
                    temp = ''
                    for letter in line:
                        temp += letter.decode('ASCII')
                    data.append(temp)
                return_data.append(data)
            else:#item  =str(nc.variables[var.strip()][:,[i]]) + '*'
                return_data.append(nc.variables[var.strip()][:,[i]])
        return return_data

def getDataFromVar_multDim_first(pathToNetCDF, var):
    with Dataset(pathToNetCDF, 'r', format= 'NETCDF4_CLASSIC') as nc:
        return np.squeeze(np.asarray(nc.variables[var.strip()][:,[0]]))

def get_dataBaseline(pathToNetCDF):
    baseline_table = []
    return_data  = []
    with Dataset(pathToNetCDF, 'r', format= 'NETCDF4_CLASSIC') as nc:
        dimensions= nc.variables['Baseline'].get_dims()
        content = getDataFromVar(pathToNetCDF, 'Baseline')
        length = []
        for dim in dimensions:
            length.append(len(dim))
            #print(len(dim))

        temp = ''
        for i in range(length[0]):#len(dimensions[0]):
            temp = ''
            for j in range(length[1]):
                for k in range(length[2]):
                    #print(k)
                    temp += content[i,j,k].decode('ASCII')
                temp += '  '
            baseline_table.append(temp)
        return_data.append(baseline_table)
    return return_data




def get_len_dims(path, var):
    with Dataset(path, 'r', format= 'NETCDF4_CLASSIC') as nc:
        dims = nc.variables[var].get_dims()
        return len(dims)
def generall_get_table_data(path, var):
    jj= 9

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
def getDataFromVar_multDim(pathToNetCDF, var):
    return_data = []
    data = []
    with Dataset(pathToNetCDF, 'r', format= 'NETCDF4_CLASSIC') as nc:
        length = len(nc.variables[var.strip()].get_dims())
        for i in range(0, length):
            return_data.append(nc.variables[var.strip()][:,[i]])

        for i in range (0,length):
            temp = []
            data.append(nc.variables[var.strip()][:,[i]])
            r= nc.variables[var.strip()][:,[i]]
            print(len(r))
            #for i in range(0,len(r)):
                #temp.append(return_data[i,[j]])
                #temp.append(r[i])
            #data.append(temp)
        print(len(data))
        y1 = data[0][:]
        y2 = data[1][:]
        print(y1)
        print(y2)
    plt.plot(y1,y2)
    plt.show()

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
