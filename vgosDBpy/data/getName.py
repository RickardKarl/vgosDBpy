"""
contains methods to get name of variables to print
"""
from netCDF4 import Dataset
import os

# returns the name to print instead of the shortname that is the variable name
def get_name_to_print(var):
        if var == 'AtmPres':
            return "Pressure"
        elif var == 'TempC':
            return "Temperature "
        elif var == 'RelHum':
            return "Humidity "
        elif var == 'Cal-Cabel':
            return "Cal-Cabel "
        elif var == 'Time':
            return 'Time'
        else:
            return var

def get_unit_to_print(path,var):
    with Dataset(path, "r", format="NETCDF4") as nc:
        if var == 'Time':
            return '[M:D:H]'
        try:
            unit = nc.variables[var].Units
        except:
            unit = '-'
        return "  ["+unit+"]"

def create_wrp_path(path):
    path=path.strip()
    wrp_path= ''

    if path.startswith('.') or path.startswith('/'):
        wrp_path = path
    else:
        year_number = path[0:1]
        if year_number.isdigit():
            if int(year_number) >= 79:
                year = '19'+year_number
            else:
                year ='20'+year_number

            wrp_path= './500/vgosDBpy/'+year+'/'+path

    if os.path.isfile(wrp_path):
        return wrp_path
    # Else return new file name
    else:
        print('Incorrect wrapper format')
        return ''


def createFullPath(wrp_path, str):

    path_split= wrp_path.split("/")
    # Create path to the actual folder by removing last item in path
    base_path = path_split[0:-1]
    base_path= '/'.join(base_path)

    if str.startswith('/'):
        path_to_file= base_path+str
    else:
        path_to_file = base_path+'/'+str
    return path_to_file
