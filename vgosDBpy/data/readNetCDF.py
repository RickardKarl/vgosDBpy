from netCDF4 import Dataset

from vgosDBpy.data.combineYMDHMS import combineYMDHMwithSec,findCorrespondingTime

"""
___________________________________________________________________________________________
Functions to create plot
___________________________________________________________________________________________
"""
# returns an array cotaning an array of the data sored in an variable
def get_data_to_plot(pathToNetCDF,var):
    with Dataset(pathToNetCDF, 'r', format = 'NETCDF4_CLASSIC') as nc:
        marker= is_multdim_var(pathToNetCDF, var)
        if marker != -1:
            y = _getDataFromVar_multDim(pathToNetCDF,var) #if matrix stored in variable, all data read in
        else:
            y = _getDataFromVar_table(pathToNetCDF,var)
        return y

"""
Takes in a path to a NetCDF file
Returns a header to a plot on the format: Station_name + Date
internal calls:
                read_var_content_S1(seekedData, path)
"""
def header_plot(path):
    #get date of session
    timePath = findCorrespondingTime(path)
    if timePath != '':
        time = combineYMDHMwithSec(timePath)
        date = time[1].date()
        station = get_var_content_S1("Station", path) # Station is name of data that one seeks.
        return ( station + "   " + str(date) )
    else:
        return ('')


"""
___________________________________________________________________________________________
Functions to create table
___________________________________________________________________________________________
"""
#Checks how the data inte specifik variable should be displayed and chooses propriate get_function for the varibles
# returns an array of arrays
def get_data_to_table(pathToNetCDF, var):
    dtype = get_dtype_var(pathToNetCDF, var)
    dims_len = _get_len_dims(pathToNetCDF, var)
    dim = get_dimension_var(pathToNetCDF,var)
    if var.strip() == 'Baseline':
        y = _get_dataBaseline(pathToNetCDF)
    elif var.strip() == 'QualityCode':
        y = _get_QualityCode_table(pathToNetCDF,var)
    elif dim.strip() == 'NumStation' and dtype == 'S1':
        y = _get_NumStation_S1_table(pathToNetCDF, var)
    elif dim.strip() == 'NumObs' and dtype == 'S1':
        y = _get_NumStation_S1_table(pathToNetCDF,var)
    elif dims_len != 1:
        y = _getDataFromVar_multDim(pathToNetCDF, var)
    elif dtype == 'S1' :
        y = _get_S1_tableData(pathToNetCDF, var)
    else:
        y = _getDataFromVar_table(pathToNetCDF, var)
    return y

# check if the variables should be displayed in the table that contains data that
#should be visualised as plot or table
def show_in_table(path,var):
    if is_Numscans(path,var):
        return True
    elif is_NumObs(path,var):
        return True
    elif is_NumsSation(path,var):
        return True
    else :
        return False

"""
___________________________________________________________________________________________
Functions to get characteristics of variable
___________________________________________________________________________________________
"""

"""
Takes in: path to netCDF file and the name of a specific varibale in file
Returns: thr data type of that variable
"""
def get_dtype_var(path, var):
    with Dataset(path, "r", format = "NETCDF4_CLASSIC" ) as nc:
        return nc.variables[var].dtype

# returns the dtype of a variable in a netCDF-file converted to a string
def get_dtype_var_str(path, var):
    with Dataset(path,'r', format = 'NETCDF4_CLASSIC') as nc:
        return str(nc.variables[var].dtype)

"""
Takes in: path to netCDF file and name of specifik variable in netCDF file
returns: that vairbales dimemsions name
"""
def get_dimension_var(pathToNetCDF, var):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        dimension = nc.variables[var].get_dims()[0].name
    return dimension

# returns the number of dimensions stored in a netCDF files varibale
def _get_len_dims(path, var):
    with Dataset(path, 'r', format= 'NETCDF4_CLASSIC') as nc:
        dims = nc.variables[var].get_dims()
        return len(dims)

# checks if a variable in a netCDF file as several columns on data
def is_multdim_var(path,var):
    marker = -1
    c=0
    with Dataset(path, 'r', format='NETCDF4_CLASSIC') as nc:
        if len(nc.variables[var.strip()].get_dims()) > 1:
            marker = c
        c += 1
    return marker

# checks if the dimension of a variable in a netCDF file is 'NumScans'
def is_Numscans(path, var):
    with Dataset(path, 'r', format = 'NETCDF4_CLASSIC') as nc:
        dimensions = nc.variables[var].get_dims()
        for dim in dimensions:
            name = dim.name
            if name.strip() == 'NumScans':
                return True
    return False

# checks if the dimension of a variable in a netCDF file is 'NumStation'
def is_NumsSation(path,var):
    with Dataset(path, 'r', format = 'NETCDF4_CLASSIC') as nc:
        dimensions = nc.variables[var].get_dims()
        for dim in dimensions:
            name = dim.name
            if name.strip() == 'NumStation':
                return True
    return False

# checks if the dimension of a variable in a netCDF file is 'NumObs'
def is_NumObs(path, var):
    with Dataset(path, 'r', format = 'NETCDF4_CLASSIC') as nc:
        dimensions = nc.variables[var].get_dims()
        for dim in dimensions:
            name = dim.name
            if name.strip() == 'NumObs':
                return True
    return False

"""
___________________________________________________________________________________________
Functions to get characteristics of netCDF file
___________________________________________________________________________________________
"""
def get_dtype_netCDF(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        dtype= []
        for var in vars:
            dtype.append(nc.variables[var].dtype)
    return dtype

"""
___________________________________________________________________________________________
Functions to read content of variable
___________________________________________________________________________________________
"""

#returns the data stored in the first column in a netCDF files variable
def getDataFromVar(path, var):
    with Dataset(path, "r", format="NETCDF4_CLASSIC") as nc:
        return(nc.variables[var][:])

#returns the data stored in the first column in a netCDF files variable stored one element in an array
def _getDataFromVar_table(path, var):
     return_data = []
     with Dataset(path, "r", format="NETCDF4_CLASSIC") as nc:
         return_data.append(nc.variables[var][:])
         return(return_data)


def _get_S1_tableData(pathToNetCDF, var):
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


def _get_NumStation_S1_table(pathToNetCDF,var):
    table = []
    return_data  = []
    with Dataset(pathToNetCDF, 'r', format= 'NETCDF4_CLASSIC') as nc:
        dimensions= nc.variables[var].get_dims()
        content = getDataFromVar(pathToNetCDF,var)
        length = []

        for dim in dimensions:
            length.append(len(dim))
        for i in range(length[0]):
            temp = ''
            for j in range(length[1]):
                temp += content[i,j].decode('ASCII')
            temp += '  '
            table.append(temp)
        return_data.append(table)
        return return_data

def _get_QualityCode_table(pathToNetCDF,var):
    return_data = []
    data_arr = []
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        data= nc.variables[var][:]
        for line in data:
            temp = ''
            temp += line.decode('ASCII')
            data_arr.append(temp)
        return_data.append(data_arr)
    return return_data

def _getDataFromVar_multDim(pathToNetCDF, var):
    return_data = []
    with Dataset(pathToNetCDF, 'r', format= 'NETCDF4_CLASSIC') as nc:
        length = len(nc.variables[var.strip()].get_dims())
        length2 = len(nc.variables[var][0,:])
        for i in range (0,length2):
            dtype = nc.variables[var.strip()][:,[i]].dtype
            if dtype == 'S1':
                data_var= nc.variables[var][:,[i]]
                data= []
                for line in data_var:
                    temp = ''
                    for letter in line:
                        temp += letter.decode('ASCII')
                    data.append(temp)
                return_data.append(data)
            else:
                return_data.append(nc.variables[var.strip()][:,[i]])
        return return_data

def _get_dataBaseline(pathToNetCDF):
    baseline_table = []
    return_data  = []
    with Dataset(pathToNetCDF, 'r', format= 'NETCDF4_CLASSIC') as nc:
        dimensions= nc.variables['Baseline'].get_dims()
        content = getDataFromVar(pathToNetCDF, 'Baseline')
        length = []
        for dim in dimensions:
            length.append(len(dim))

        temp = ''
        for i in range(length[0]):
            temp = ''
            for j in range(length[1]):
                for k in range(length[2]):
                    temp += content[i,j,k].decode('ASCII')
                temp += '  '
            baseline_table.append(temp)
        return_data.append(baseline_table)
    return return_data



#### Functions below returns strings instead of arrays ####


"""
Takes in: path to netCDF file
Returns: a long string containing all the information stored in "S1" datatype vairbales in a netCDF file
internal Calls:
            read_netCDF_variables(path)
            find_dtype(path)
            read_var_content_S1(var, path)
"""
def get_netCDF_vars_info(pathToNetCDF):
    info = ""
    vars =get_netCDF_variables(pathToNetCDF)
    dtypes = get_dtype_netCDF(pathToNetCDF)
    for i in range(len(vars)):
        if not is_Numscans(pathToNetCDF,vars[i]) and not is_NumObs(pathToNetCDF,vars[i]):
            if dtypes[i] == 'S1' :
                info += vars[i] +':'+  get_var_content_S1(vars[i], pathToNetCDF) + "\n \n"
            else:
                info += get_var_content_constant(pathToNetCDF, vars[i]) + '\n \n '

    return info


"""
Takes in: path to netCDF file and the name of the variable that one is looking for.
Retuns the header of a netCDF file, meaning all the S1 vars as a long string.
Internal Calls:
                non
"""
def get_var_content_S1(seekedData,pathToNetCDF):
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

def get_var_content_constant(pathToNetCDF, var):
    name = var
    with Dataset(pathToNetCDF, 'r', format = 'NETCDF4_CLASSIC') as nc:
        data= nc.variables[var][:]
        head = name +": \n"
        for column in data:
            letter = str(column)
            head += letter+ '    '
        return head

"""
___________________________________________________________________________________________
Other
___________________________________________________________________________________________
"""
"""
Takes is a path to a netCDF file and a name of a variable and returns the varibales content.
"""
def is_multdim_var_list(paths, vars):
    for i in range(0,len(paths)):
        path= paths[i]
        var=vars[i]
        marker = -1
        c=0
        with Dataset(path, 'r', format='NETCDF4_CLASSIC') as nc:
            if len(nc.variables[var.strip()].get_dims()) > 1:
                marker = c
            c += 1
    return marker


"""
Takes in: Path to NetCDF file
returns: an array containing all the variabls names for the netCDF file
"""
def get_netCDF_variables(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        variables= []
        for var in vars:
            variables.append(var)
    return variables

def not_S1(paths, vars):
    for i in range(len(paths)):
        with Dataset(paths[i], 'r', format = 'NETCDF4_CLASSIC') as nc:
            dtype = nc.variables[vars[i]].dtype.name
            if dtype.strip() == 'S1':
                return False
    return True
