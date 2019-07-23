from vgosDBpy.data.readNetCDF import read_netCDF_variables, find_dtype, getDataFromVar
from netCDF4 import Dataset





def find_dimensions(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        vars= nc.variables
        dims= []
        for var in vars:
            #for ncattr in var.ncattrs():
                #print(var.getncattr(ncattr))
            #if str(var).strip() == 'Cal-SlantPathTropWet':
            #    print(len(nc.variables[var].get_dims()))
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

def print_name_dtype_dim_length(pathToNetCDF):
    vars = read_netCDF_variables(pathToNetCDF)
    dtypes = find_dtype(pathToNetCDF)
    dims = find_dimensions(pathToNetCDF)
    lengths = find_length(pathToNetCDF)
    content = find_content(pathToNetCDF)
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
