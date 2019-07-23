import netCDF4 as nc
import matplotlib.pyplot as plt

from vgosDBpy.data.VersionName import NewVersionName

def get_netCDF_variable(file_name_path, variable_name):
    '''
    Returns data from one netCDF variables

    file_name_path [string] path to netCDF file of interest
    variable_name [string] name of variable in netCDF files
    '''
    with nc.Dataset(file_name_path) as file:
        variable = file[variable_name][:]

    return variable

def update_netCDF_variable(file_name_path, new_file_name_path, variables):
    '''
    Updates a existing variable data in a netCDF file and creates
    a new netCDF file which contains the updated variable

    file_name_path [string] path to netCDF file which will be rewritten
    new_file_name_path [string] path to new netCDF file that is rewritten
    variables [dict] {variable name: updated variable}
    '''

    # Open the current netCDF file
    with nc.Dataset(file_name_path, 'r') as src:
        # Create a new netCDF file with the same format as the old one
        with nc.Dataset(new_file_name_path, "w", format = src.data_model) as dst:

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


def create_netCDF_file(pathToNetCDF, variables):
    '''
    Creates a new netCDF file given the path and the variables,
    generates the new path name

    file_name_path [string] path to netCDF file which will be rewritten
    variables [dict] {variable name: updated variable}
    '''
    new_file_path = NewVersionName(pathToNetCDF)
    update_netCDF_variable(pathToNetCDF, new_file_path, variables)
    print('Creating new netCDF file with the path', new_file_path)
    return new_file_path
