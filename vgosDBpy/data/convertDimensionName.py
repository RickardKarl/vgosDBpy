from vgosDBpy.data.combineYMDHMS import findCorrespondingTime
#from vgosDBpy.data.readNetCDF import get_dimension_var
from netCDF4 import Dataset

def get_correct_dimension_name(path):
    time_path = findCorrespondingTime(path)
    dims = get_dimension_var(time_path, 'YMDHM')
    return dims.strip().lower()

def get_folder_name(path):
    splits = path.split('/')
    folder = path[-2].strip().lower()
    return folder

def get_dimension_var(pathToNetCDF, var):
    with Dataset(pathToNetCDF, "r") as nc:
        dimension = nc.variables[var].get_dims()[0].name
    return dimension
