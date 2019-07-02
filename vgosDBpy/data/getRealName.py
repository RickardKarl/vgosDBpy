"""
contains methods to get name of variables to print
"""
from netCDF4 import Dataset

def get_name_to_print(path, var):
        if var == 'AtmPres':
            return "Pressure "
        elif var == 'TempC':
            return "Temperature " #" [" +unit+ "]"
        elif var == 'RealHum':
            return "Humidity "#"[" +unit+ "]"
        elif var == 'Cal-Cabel':
            return "Cal-Cabel  "#"[" +unit+ "]"
        else:
            return var

def get_unit_to_print(path,var):
    with Dataset(path, "r", format="NETCDF4") as nc:
        unit=nc.variables[var].Units
        if var == 'AtmPres':
            return  "[" +unit+ "]"
        elif var == 'TempC':
            return " [" +unit+ "]"
        elif var == 'RealHum':
            return " [" +unit+ "]"
        elif var == 'Cal-Cabel':
            return " [" +unit+ "]"
        else:
            return var
