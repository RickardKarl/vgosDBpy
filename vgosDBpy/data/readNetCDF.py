from netCDF4 import Dataset

from vgosDBpy.data.combineYMDHMS import combineYMDHMwithSec,findCorrespondingTime
#from vgosDBpy.data.PathParser import findCorrespondingTime

#Actuallt used functions:

#used from outside this program
"""
Takes is a path to a netCDF file and a name of a variable and returns the varibales content.
"""
def getDataFromVar(path, var):
    with Dataset(path, "r", format="NETCDF4_CLASSIC") as nc:
        return(nc.variables[var][:])

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

"""
Takes in: path to netCDF file and name of variable in file
Returns: True of variabele has dismension "NumScans" and d_type != S1
internal calls:
                read_netCDF_dimension_for_var(var, path)
                get_dtype_for_var(path, var)
"""
#def is_possible_to_plot(paths, vars):
#    for i in range(0,len(paths)):
#        path = paths[i]
#        var = vars[i]
#        dimension = read_netCDF_dimension_for_var(path, var)
#        data_type = get_dtype_for_var(path,var)
#        if dimension.strip() == "NumScans" or dimension.strip() == 'NumObs' and data_type != "S1"  :
#            return True
#    return False


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

def is_multdim_var(path,var):
    marker = -1
    c=0
    with Dataset(path, 'r', format='NETCDF4_CLASSIC') as nc:
        if len(nc.variables[var.strip()].get_dims()) > 1:
            marker = c
        c += 1
    return marker

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

#def read_all_dimensions_for_var(path, var):
#    with Dataset(path, 'r', format = 'NETCDF4_CLASSIC') as nc:
#        return nc.variables[var].get_dims()
"""
Takes in: path to netCDF file amd name of var in file
Returns: True is varibale has dtype != S1 but is not plottable
Internal calls:
                get_dtype_for_var(path, var)
                read_netCDF_dimension_for_var(path,var)
"""
#def is_var_constant(path, var):
#    dtype = get_dtype_for_var(path, var)
#    if is_numScan_or_NumObs(path,var):
#        return False
#    else:
#        if dtype != 'S1':
#            return True
#    return False

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
        if not is_numScan_or_NumObs(pathToNetCDF, vars[i]):
            if dtypes[i] == 'S1' :
                #if not is_numScan_or_NumObs(pathToNetCDF, vars[i]):
                info += vars[i] +':'+  get_var_content_S1(vars[i], pathToNetCDF) + "\n \n"
            else:
                info += get_var_content_constant(pathToNetCDF, vars[i]) + '\n \n '

    return info

def not_S1(paths, vars):
    for i in range(len(paths)):
        with Dataset(paths[i], 'r', format = 'NETCDF4_CLASSIC') as nc:
            dtype = nc.variables[vars[i]].dtype.name
            if dtype.strip() == 'S1':
                return False
    return True

def get_dtype_netCDF(pathToNetCDF):
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
            #print(head)
        return head

"""
Takes in: path to netCDF file and name of specifik variable in netCDF file
returns: that vairbales dimemsions name
"""
def get_dimension_var(pathToNetCDF, var):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        dimension = nc.variables[var].get_dims()[0].name
    return dimension
"""
def read_unit_for_var (pathToNetCDF, var):
    with Dataset(pathToNetCDF, 'r', format= 'NETCDF4_CLASSIC') as nc:
        try:
            unit = nc.variables[var].Units
        except:
            unit = '-'
        return "  ["+unit+"]"
"""
def get_data_to_plot(pathToNetCDF,var):
    with Dataset(pathToNetCDF, 'r', format = 'NETCDF4_CLASSIC') as nc:
        marker= is_multdim_var(pathToNetCDF, var)
        if marker != -1:
            y = _getDataFromVar_multDim(pathToNetCDF,var)
        else:
            y = _getDataFromVar_table(pathToNetCDF,var)
        return y

def get_data_to_table(pathToNetCDF, var):
    dtype = get_dtype_for_var(pathToNetCDF, var)
    dims_len = _get_len_dims(pathToNetCDF, var)
    dim = get_dimension_var(pathToNetCDF,var)
    if var.strip() == 'Baseline':
        #print('enter 1')
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
        #print(length)
        for i in range(length[0]): #len(dimensions[0]):
            temp = ''
            for j in range(length[1]):
                temp += content[i,j].decode('ASCII')
            temp += '  '
            #print(temp)
            table.append(temp)
        return_data.append(table)
        #print(len(return_data))
        return return_data

def _getDataFromVar_table(path, var):
    return_data = []
    with Dataset(path, "r", format="NETCDF4_CLASSIC") as nc:
        return_data.append(nc.variables[var][:])
        #print(return_data)
        return(return_data)


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
        #print(length)
        length2 = len(nc.variables[var][0,:])
        #print(length2)
        for i in range (0,length2):
            dtype = nc.variables[var.strip()][:,[i]].dtype
            #print(nc.variables[var.strip()][:,[i]].dtype)
            if dtype == 'S1':
                data_var= nc.variables[var][:,[i]]
                #print(data_var)
                data= []
                for line in data_var:
                    temp = ''
                    for letter in line:
                        temp += letter.decode('ASCII')
                    data.append(temp)
                return_data.append(data)
            else:#item  =str(nc.variables[var.strip()][:,[i]]) + '*'
                #print('Not S1')
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


def _get_len_dims(path, var):
    with Dataset(path, 'r', format= 'NETCDF4_CLASSIC') as nc:
        dims = nc.variables[var].get_dims()
        return len(dims)


"""
Takes in: path to netCDF file and the name of a specific varibale in file
Returns: thr data type of that variable
"""
def get_dtype_for_var(path, var):
    with Dataset(path, "r", format = "NETCDF4_CLASSIC" ) as nc:
        return nc.variables[var].dtype
