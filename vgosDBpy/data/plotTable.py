# tableFunction
import sys
import numpy as np
import pandas as pd
import os


from vgosDBpy.data.combineYMDHMS import combineYMDHMwithSec, findCorrespondingTime
from vgosDBpy.data.readNetCDF import get_data_to_table
from vgosDBpy.data.getName import get_name_to_print as name, get_unit_to_print as unit

# called from outside, creates an directory with all information to a table
class Tablefunction():
    time_label = 'Time [Y-M-D H:M:S]'
    time_key = 'Time'
    def __init__(self):
        self.data = {} # key = name of variable, value = array of data
        self.header = [] # Arrat of names of varibles

    # function that is called from other files
    def tableFunctionGeneral(self,paths,vars):
        self.data_reset()
        timePath = findCorrespondingTime(paths[0].strip())
        if os.path.isfile(timePath):
            time =  combineYMDHMwithSec(timePath)
            self.data[Tablefunction.time_key] = time
        c = 0
        for path in paths:
            y = get_data_to_table(path, vars[c])
            if len(y) == 1 :
                self.data[name(vars[c])] = y[0]
            else:
                for i in range(len(y)):
                    self.data[name(vars[c])+' #'+ str(i+1)] = y[i]
            c = c + 1
        return self.data

    # function that is called from other files, adda more columns to a already excisting table
    def append_table(self, paths, vars):
        y = get_data_to_table(paths[-1],vars[-1])
        new_data = {}
        if len(y) == 1 :
            self.data[name(vars[-1])] = y[0]
            new_data[name(vars[-1])] = y[0]

        else:
            for i in range(len(y)):
                self.data[name(vars[-1])+' #'+ str(i+1)] = y[i]
                new_data[name(vars[-1])+' #'+ str(i+1)] = y[i]
        return new_data

    def get_table(self):
        return self.data

    def append_header(self, paths, vars):
        new_data = self.append_table(paths,vars)
        names = list(new_data)
        for name in names :
            self.header.append(name)
        return self.header

    def return_header_names(self):
        self.header_reset()
        names = list(self.data)
        for name in names :
            self.header.append(name)
        return self.header

    def header_reset(self):
        self.header=[]

    def data_reset(self):
        self.data = {}
