# Reads dimensions from a netcdf file
from prettytable import PrettyTable as PT
from netCDF4 import Dataset
import pandas as pd
from numpy.random import uniform
from combineYMDHMS import combineYMDHMwithSec
import os

def read_netCDF_dimension(pathToNetCDF):
    with Dataset(pathToNetCDF, "r", format="NETCDF4_CLASSIC") as nc:
        dims= nc.dimensions
        dimensions= []
        for dim in dims:
            dimensions.append(dim)
    return dimensions

 def print_ncattr(key):
        """
        Prints the NetCDF file attributes for a given key

        Parameters
        ----------
        key : unicode
            a valid netCDF4.Dataset.variables key
        """
        try:
            print "\t\ttype:", repr(nc_fid.variables[key].dtype)
            for ncattr in nc_fid.variables[key].ncattrs():
                print '\t\t%s:' % ncattr,\
                      repr(nc_fid.variables[key].getncattr(ncattr))
        except KeyError:
            print "\t\tWARNING: %s does not contain variable attributes" % key

print "NetCDF dimension information:"
for dim in nc_dims:
    print "\tName:", dim
    print "\t\tsize:", len(nc_fid.dimensions[dim])
    print_ncattr(dim)
path = "./../../../../Files/10JAN04XU/KOKEE/FeedRotation.nc"

#path= "./../../../../Files/10JAN04XU/Head.nc"

pathTime = "./../../../../Files/10JAN04XU/KOKEE/TimeUTC.nc"
dims_in_file  = read_netCDF_dimension(path)
print(dims_in_file)
