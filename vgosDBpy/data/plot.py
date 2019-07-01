import matplotlib.pyplot as plt
from netCDF4 import Dataset


def plot_2(path_x, name_x, path_y, name_y):

    with Dataset(path_x, "r", format= "NETCDF4_CLASSIC") as nc:
        x = data = nc.variables[name_x][:]
    with Dataset(path_y, "r", format= "NETCDF4_CLASSIC") as nc:
        y = data = nc.variables[name_y][:]
    plt.plot(x,y)
    plt.show()
