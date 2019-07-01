# create combination of data and name

from readNetCDF import read_var_content, possible_to_plot
from prettytable import PrettyTable as PT
from netCDF4 import Dataset
import pandas as pd
from numpy.random import uniform
from combineYMDHMS import combineYMDHMwithSec
import os

class plotMap():

    map = {}
    def __init__(self):


    def insertToMap (self, path, names):
        """
        Takes in a path to a netCDF file and the names of the arrays in the file that one wants to plot.
        Checks if all dimensions are the same. before calling plot. Otherwise says that they are not the same.
        """
        #path = "./../../../../Files/10JAN04XU/KOKEE/Met.nc"
        #names = possible_to_plot(path)
        #node = Node.__init__(name,path)
        with Dataset(path, "r", format= "NETCDF4_CLASSIC") as nc:
            vars= nc.variables
            for var in vars:
                if var not in list(self.map) and var in names :
                    self.map[name] = nc.variables[var][:]

    def removeFromMap (self, name):
        if name in self.map :
            del self.map[name]

    def getMap(self):
        return self.map

    def getMapKeys(self):
        return list(self.map)

    def getMapValues(self):
        data=[]
        for name in list(self.map):
            data.append(self.map[name])
        return data
    def getKeyValue(self,name):
        return self.map[name]

class Node():
    name = ""
    path = ""

    def __init__(self, name, path):
        self.name = names
        self.path = pathh

    def getName():
        return names
    def getPath():
        return path
