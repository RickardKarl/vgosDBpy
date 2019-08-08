"""
contains methods to get name of variables to print
"""
from netCDF4 import Dataset

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
