"""
contains methods to get name of variables to print
"""
from netCDF4 import Dataset

def get_name_to_print(path, var):
        if var == 'AtmPres':
            return "Pressure "
        elif var == 'TempC':
            return "Temperature " #" [" +unit+ "]"
        elif var == 'RelHum':
            return "Humidity "#"[" +unit+ "]"
        elif var == 'Cal-Cabel':
            return "Cal-Cabel  "#"[" +unit+ "]"
        else:
            return var

def get_unit_to_print(path,var):
    with Dataset(path, "r", format="NETCDF4") as nc:
        dtype = nc.variables[var].dtype
        #if dtype.name.strip() != 'S1':
            #unit=nc.variables[var].Units.name
        #else:
        #    unit = ''
        #return "  ["+unit+"]"
        return 'UNIT'
