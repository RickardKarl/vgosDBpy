from vgosDBpy.data.readNetCDF import get_netCDF_variables, get_dtype_netCDF, getDataFromVar
from netCDF4 import Dataset

#returns the name of the dimension of the first element in a varable
def get_dimensions(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        dims= []
        for var in vars:
            dims.append(nc.variables[var].get_dims()[0].name)
    return dims

# returns the length of the data stored in an netCDF variable
def get_length(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        lengths= []
        for var in vars:
            lengths.append(len(nc.variables[var][:]))
    return lengths

# returns all the content stored in a netCDF file by looping thorugh all variables
def get_content(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        content= []
        for var in vars:
            content.append(getDataFromVar(pathToNetCDF,var))
    return content
# is used as an DEBUG function that will print out information about all vairbales in the netCDF files
def print_name_dtype_dim_length(pathToNetCDF):
    vars = get_netCDF_variables(pathToNetCDF)
    dtypes = get_dtype_netCDF(pathToNetCDF)
    dims = get_dimensions(pathToNetCDF)
    lengths =get_length(pathToNetCDF)
    content = get_content(pathToNetCDF)
    U = []
    print(len(vars)+ len(dims)+ len(dtypes) + len(lengths))

    s = ""
    j=0
    print(len(U))
    for i in range(0, len(vars)):
        print(vars[i])
        print(dtypes[i])
        print(dims[i])
        print(lengths[i])
        print(content[i])
        print("#####################")
    print(s)
