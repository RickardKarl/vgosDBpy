from netCDF4 import Dataset

from vgosDBpy.data.combineYMDHMS import combineYMDHMwithSec,findCorrespondingTime
from vgosDBpy.data.convertDimensionName import get_folder_name, get_correct_dimension_name
"""
___________________________________________________________________________________________
Functions to create plot
___________________________________________________________________________________________
"""


"""
returns an array cotaning an array of the data sored in an variable
input:
    pathToNetCDF: [string]
    var: [string]
output:
    y: [array[var_dtype]]
"""
def get_data_to_plot(pathToNetCDF,var):
    with Dataset(pathToNetCDF, 'r') as nc:
        marker= is_multdim_var(pathToNetCDF, var)
        if marker != -1:
            y = _getDataFromVar_multDim(pathToNetCDF,var) #if matrix stored in variable, all data read in
        else:
            y = _getDataFromVar_table(pathToNetCDF,var)
        return y

"""
creates the title for a plot on the form 'Sation_name + date_of_Session'
input:
    path[string]
output:
    stting

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

"""
Checks how the data inte specific variable should be displayed and chooses propriate get_function for the data
input:
    pathToNetCDF: [string]
    var: [string]
output:
    y: [array[data_array[var_dtype]]]
"""
def get_data_to_table(pathToNetCDF, var):
    dtype = get_dtype_var(pathToNetCDF, var)
    dims_len = _get_len_dims(pathToNetCDF, var)
    dim = get_dimension_var(pathToNetCDF,var)
    if var.strip() == 'Baseline':
        y = _get_dataBaseline(pathToNetCDF)
    elif var.strip() == 'QualityCode':
        y = _get_QualityCode_table(pathToNetCDF,var)
    elif var.strip() == 'Dis-OceanLoad':
        y= _get_dis_oceanLoad(pathToNetCDF)
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

"""
Returns True if a variable has dtype NumObs, NumScans or NumStation <==> show in Variable Table
"""
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
Returns a variables dtype
input:
    path: [string]
    var[stirng]
output:
    dtype
"""
def get_dtype_var(path, var):
    with Dataset(path, "r") as nc:
        return nc.variables[var].dtype



"""
Returns a variables dtype as a string
input:
    path: [string]
    var[stirng]
output:
    string
"""
def get_dtype_var_str(path, var):
    with Dataset(path,'r') as nc:
        return str(nc.variables[var].dtype)


"""
returns the name of the first dimension of a netCDF variable
input:
    pathToNetCDF: [str]
    var: [str]
output:
    dimension: [str]
"""
def get_dimension_var(pathToNetCDF, var):
    with Dataset(pathToNetCDF, "r") as nc:
        dimension = nc.variables[var].get_dims()[0].name
    return dimension

"""
returns the number of dimensions stored in a netCDF files varibale
output:
    [int]
"""
def _get_len_dims(path, var):
    with Dataset(path, 'r') as nc:
        dims = nc.variables[var].get_dims()
        return len(dims)

"""
checks if a variable in a netCDF file has several columns on data
input:
    path [string]
    var[string]
output:
    marker: [int]
"""
def is_multdim_var(path,var):
    marker = -1
    c=0
    with Dataset(path, 'r') as nc:
        if len(nc.variables[var.strip()].get_dims()) > 1:
            marker = c
        c += 1
    return marker



"""
checks if the dimension of a variable in a netCDF file is 'NumScans'
input:
    path [string],
    var[string]
output:
    boolean
"""
def is_Numscans(path, var):
    with Dataset(path, 'r') as nc:
        dimensions = nc.variables[var].get_dims()
        for dim in dimensions:
            name = dim.name.lower().strip()
            if name.strip() == get_correct_dimension_name(path):
                return True
    return False


"""
checks if the dimension of a variable in a netCDF file is 'NumStation'
input:
    path [string]
    var[string]
output:
    boolean
"""
def is_NumsSation(path,var):
    with Dataset(path, 'r') as nc:
        dimensions = nc.variables[var].get_dims()
        for dim in dimensions:
            name = dim.name.lower().strip()
            if name.strip() == 'NumStations':
                return True
    return False



"""
checks if the dimension of a variable in a netCDF file is 'NumObs'
input:
    path [string]
    var[string]
output:
    boolean
"""
def is_NumObs(path, var):
    folder= get_folder_name(path)
    if folder != 'Observables':
        return False
    with Dataset(path, 'r') as nc:
        dimensions = nc.variables[var].get_dims()
        for dim in dimensions:
            name = dim.name.lower().strip()
            if name.strip() == get_correct_dimension_name(path):
                return True
    return False

"""
___________________________________________________________________________________________
Functions to get characteristics of netCDF file
___________________________________________________________________________________________
"""

"""
returns the first dtype for all variables in a netCDF files
input:
    pathToNetCDF: [string]
output:
    dtype: [array[string]]
"""
def get_dtype_netCDF(pathToNetCDF):
    with Dataset(pathToNetCDF, "r") as nc:
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


"""
returns the data stored in the first column in a netCDF files variable
input:
    path: [string]
    var[string]
output:
    [array]
"""
def getDataFromVar(path, var):
    with Dataset(path, "r") as nc:
        return(nc.variables[var][:])


"""
returns the data stored in the first column in a netCDF file
input:
    path: [string]
    var[string]
output:
    [array[data_array]]
"""
def _getDataFromVar_table(path, var):
     return_data = []
     with Dataset(path, "r") as nc:
         return_data.append(nc.variables[var][:])
         return(return_data)

"""
Return data from NetCDF variable with dtype S1
input:
    path: [string]
    var[string]
output:
    [array[data_array]]
"""
def _get_S1_tableData(pathToNetCDF, var):
    return_data = []
    data = []
    with Dataset(pathToNetCDF, "r") as nc:
        data= nc.variables[var][:]
        for line in data:

            temp = ''
            for letter in line:

                temp += letter.decode('ASCII')
            data.append(temp)
        return_data.append(data)
    return return_data


"""
Return data from NetCDF variable with dtype S1 and dimension NumStation
input:
    path: [string]
    var[string]
output:
    [array[data_array]]
"""
def _get_NumStation_S1_table(pathToNetCDF,var):
    table = []
    return_data  = []
    with Dataset(pathToNetCDF, 'r') as nc:
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



"""
Return data from the NetCDF varibale QualityCode
input:
    path: [string]
    var[string]
output:
    [array[data_array]]
"""
def _get_QualityCode_table(pathToNetCDF,var):
    return_data = []
    data_arr = []
    with Dataset(pathToNetCDF, "r") as nc:
        data= nc.variables[var][:]
        for line in data:
            temp = ''
            temp += line.decode('ASCII')
            data_arr.append(temp)
        return_data.append(data_arr)
    return return_data



"""
Return data from NetCDF variable with data stored in matrix instead of array
input:
    path: [string]
    var[string]
output:
    [array[data_array]]
"""
def _getDataFromVar_multDim(pathToNetCDF, var):
    return_data = []
    with Dataset(pathToNetCDF, 'r') as nc:
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


"""
Return data from the NetCDF variable Baseline
input:
    path: [string]
output:
    [array[data_array]]
"""
def _get_dataBaseline(pathToNetCDF):
    baseline_table = []
    return_data  = []
    with Dataset(pathToNetCDF, 'r') as nc:
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


def _get_dis_oceanLoad(pathToNetCDF):
    disOcean_table = []
    return_data  = []
    with Dataset(pathToNetCDF, 'r') as nc:
        dimensions= nc.variables['Dis-OceanLoad'].get_dims()
        content = getDataFromVar(pathToNetCDF, 'Dis-OceanLoad')
        length = []
        for dim in dimensions:
            length.append(len(dim))

        temp = ''
        for i in range(length[0]):
            temp = ''
            for j in range(length[1]):
                for k in range(length[2]):
                    temp += str(content[i,j,k])
                temp += '    '
            disOcean_table.append(temp)
        return_data.append(disOcean_table)
    return return_data

#### Functions below returns strings instead of arrays ####


"""
returns data from netCDF file as a text string
input:
    pathToNetCDF: [string]
output:
    info: [string]
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
returns a string of the information in a netCDF-file variabel with dimension S1
input:
    pathToNetCDF:[string]
    var[string]
output:
    head: [string]
"""
def get_var_content_S1(var,pathToNetCDF):
    with Dataset(pathToNetCDF, "r") as nc:

        dimensions = nc.variables[var].get_dims()
        lengths = []
        for dim in dimensions:
            lengths.append(len(dim))

        data= getDataFromVar(pathToNetCDF, var)

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

"""
returns a string of the information in a netCDF-file variabel
input:
    pathToNetCDF:[string]
    var[string]
output:
    head: [string]
"""
def get_var_content_constant(pathToNetCDF, var):
    name = var
    with Dataset(pathToNetCDF, 'r') as nc:
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
Takes is an list of netCDF varibales and checks if any of them store a matrix insted of an array
input:
    paths: [array]
    vars: [array]
output:
    market: int
"""
def is_multdim_var_list(paths, vars):
    for i in range(0,len(paths)):
        path= paths[i]
        var=vars[i]
        marker = -1
        c=0
        with Dataset(path, 'r') as nc:
            if len(nc.variables[var.strip()].get_dims()) > 1:
                marker = c
            c += 1
    return marker


"""
Returns a list of all varibales stored in a netCDF file
input:
    pathToNetCDF: [string]
output:
    variables [array]
"""
def get_netCDF_variables(pathToNetCDF):
    with Dataset(pathToNetCDF, "r") as nc:
        vars= nc.variables
        variables= []
        for var in vars:
            variables.append(var)
    return variables


"""
Return true if no variable is of dtype S1
input:
    paths:[array[string]],
    vars[array[string]]
output:
    boolean
"""
def not_S1(paths, vars):
    for i in range(len(paths)):
        with Dataset(paths[i], 'r') as nc:
            dtype = nc.variables[vars[i]].dtype.name
            if dtype.strip() == 'S1':
                return False
    return True


"""
input:
    pathToNetCDF:[string]
    var[string]
output:
    boolean
"""
def is_string(pathToNetCDF,var):
    dtype = get_dtype_var(pathToNetCDF, var)
    if dtype == 'S1':
        return True
    else:
        return False
