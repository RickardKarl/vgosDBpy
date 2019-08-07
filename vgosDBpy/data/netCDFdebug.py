from vgosDBpy.data.readNetCDF import get_netCDF_variables, get_dtype_netCDF, getDataFromVar
from netCDF4 import Dataset


def get_dimensions(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        dims= []
        for var in vars:
            dims.append(nc.variables[var].get_dims()[0].name)
    return dims

def get_length(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        lengths= []
        for var in vars:
            lengths.append(len(nc.variables[var][:]))
    return lengths

def get_content(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        content= []
        for var in vars:
            content.append(getDataFromVar(pathToNetCDF,var))
    return content

def print_name_dtype_dim_length(pathToNetCDF):
    vars = get_netCDF_variables(pathToNetCDF)
    dtypes = get_dtype_netCDF(pathToNetCDF)
    dims = get_dimensions(pathToNetCDF)
    lengths =get_length(pathToNetCDF)
    content = get_content(pathToNetCDF)
    U = []
    print(len(vars)+ len(dims)+ len(dtypes) + len(lengths))
    #with Dataset(pathToNetCDF, 'r', format='NETCDF4_CLASSIC') as nc:
        #c=0
        #for var in vars:
            #if str(dims[0]).strip() != 'NumScans' :
                #U.append(nc.variables[var].Units)
            #print(var)
            #    c += 1
    s = ""
    j=0
    print(len(U))
    for i in range(0, len(vars)):
        print(vars[i])
        print(dtypes[i])
        print(dims[i])
        print(lengths[i])
        print(content[i])
        #if str(dims[i]).strip() == 'NumScans':
        #    print(U[j])
        #    j+= 1
        print("#####################")
    print(s)
