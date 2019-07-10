'''
    Author: Rickard Karlsson
'''
import netCDF4 as nc
import matplotlib.pyplot as plt


'''
TODO:

UPDATING DATA:
Update attributes
Update dimensions
Make sure variables exist in in netCDF file

EDITING DATA:
How to edit data?


MUST KEEP THE FORMAT WHEN CREATING A NEW netCDF file
'''

def get_netCDF_variable(file_name_path, variable_name):
    '''
    Returns data from one netCDF variables

    file_name_path [string] path to netCDF file of interest
    variable_name [string] name of variable in netCDF files
    '''
    with nc.Dataset(file_name_path) as file:
        variable = file[variable_name][:]

    return variable

 def create_new_nc_file(pathToNetCDF, variables):
     new_name = NewVersionName(pathToNetCDF)
    update_netCDF_variable(pathToNetCDF, newname, vairables)

def update_netCDF_variable(file_name_path, new_file_name_path, variables):
    '''
    Updates a existing variable data in a netCDF file and creates
    a new netCDF file which contains the updated variable

    file_name_path [string] path to netCDF file which will be rewritten
    new_file_name_path [string] path to new netCDF file that is rewritten
    variables [dict] {variable name: updated variable}
    '''

    # Open the current netCDF file and create a new one
    with nc.Dataset(file_name_path) as src, nc.Dataset(new_file_name_path, "w") as dst:

        # Copy global attributes
        dst.setncatts(src.__dict__)

        # Copy dimensions
        for name, dimension in src.dimensions.items():
            dst.createDimension(
                name, (len(dimension) if not dimension.isunlimited() else None))

        # Copy variables/data except for the updated ones
        for name, variable in src.variables.items():
            instance = dst.createVariable(name, variable.datatype,
                                        variable.dimensions)
            if name not in variables.keys():
                dst[name][:] = src[name][:]

            else:
                dst[name][:] = variables[name]

            # Copy variable attributes
            dst[name].setncatts(src[name].__dict__)
