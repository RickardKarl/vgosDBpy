# tableFunction
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from vgosDBpy.data.PathParser import findCorrespondingTime
from vgosDBpy.data.combineYMDHMS import combineYMDHMwithSec
from vgosDBpy.data.readNetCDF import getDataFromVar
from vgosDBpy.data.getRealName import get_name_to_print as name, get_unit_to_print as unit


class Tablefunction():
    time_label = 'Time [Y-M-D H:M:S]'
    def __init__(self):
        self.data = {}
        self.header = []

    def tableFunctionGeneral(self,paths,vars): # USE THISONE
        self.data_reset()
        timePath = findCorrespondingTime(paths[0])
        if timePath != '':
            time =  combineYMDHMwithSec(timePath)
            self.data['Time'] = time
        c = 0
        for path in paths:
            y = getDataFromVar( path, vars[c] )
            self.data[ name ( path, vars[c] ) ] = y
            c = c + 1
        return self.data

    def append_table(self, paths, vars):
        y = getDataFromVar(paths[-1],vars[-1])
        self.data[name(paths[-1], vars[-1])] = y
        return self.data

    def append_header(self, paths, vars):
        self.header.append( name(paths[-1],vars[-1]) + unit(paths[-1], vars[-1]))
        return self.header

    def return_header_names(self,paths, vars):
        self.header_reset()
        if 'Time' in self.data:
            self.header.append(Tablefunction.time_label)
        for i in range(0,len(paths)) :
            n = name(paths[i],vars[i])
            u = unit(paths[i],vars[i])
            self.header.append(n + u)
        return self.header

    def header_reset(self):
        self.header=[]

    def data_reset(self):
        self.data = {}

"""
class Table():
    def __init__(self):
        self.data = {}
        self.default_time = 1
        self.header = ""

    def create_table(self, paths, vars): # USE THISONE'
        default_time = j
        if default_time == 1:
            timePath = findCorrespondingTime(paths[0])
            time =  combineYMDHMwithSec(timePath)
            self.data['Time'] = time
        c=0
        for path in paths:
            y = getDataFromVar( path, vars[c] )
            self.data [ name ( path, vars[c] ) ] = y
            c = c + 1
            #data.update( { name( paths[i],vars[i] ) : y } )
        return data

    def reset_table():
        self.table = {}

    def get_table():
        return self.table

    def append_table(self, path, var):
        y= getDataFromVar(path, var)
        self.data[name(path,var)] = y

    def reset_header():
        self.header = []

    def create_header_names(paths, vars):
        self.reset_header()
        if default_time == 1 :
            self.header.append('Time [Y-M-D H:M:S]')
        for i in range(0,len(paths)) :
            n = name(paths[i],vars[i])
            u = unit(paths[i],vars[i])
            self.header.append(n + u)

    def append_header(path,var):
        n = name(path, var)
        u = unit(path, var)
        self.header.append(n+u)

    def get_header():
        return self.header

    def append_table(old_data,path_new, var_new):
        y = getDataFromVar(path_new, var_new)
        data.update( {name(path_new,var_new) : y} )

    def set_default_time(time_int = 1):
        self.default_time =  time_int

    def get_default_time():
        return self.default_time
"""
"""
Default: shows path´s var against time using a QT tableWidget
returns a tableWidget to be handled somwhere else..
"""
"""
def tableFunction(path, var): # NOT USED ANYMORE USE GENERAL
    timePath = findCorrespondingTime(path)
    time = combineYMDHMwithSec(timePath)
    y = getDataFromVar(path, var)
    data = {}
    data ['Time'] = time
    data [name(path,var)] = y
    #data = {'Time':time , name(path,var): y }
    return data

def tableFunction2data (path1, var1, path2, var2): # NOT USED ANYMORE USE GENERAL
    timePath = findCorrespondingTime(path1)
    time = combineYMDHMwithSec(timePath)
    y1 = getDataFromVar(path1, var1)
    y2 = getDataFromVar(path2, var2)
    data = {'Time': time , name(path1,var1) : y1, name(path2, var2) : y2 }
    return data
"""

"""
Takes in two arrays[], one containing paths and one names of variable, order so that the indexes agree
"""


#def append_table(old_data,path_new, var_new):
#    y = getDataFromVar(path_new, var_new)
#    data.update( { name(path_new,var_new) : y } )
#    return data






"""
def tableFunction2data(path1, var1, path2, var2):
    fig, ax = plt.subplots()
        # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    timePath = findCorrespondingTime(path1)
    time = combineYMDHMwithSec(timePath)
    y1 = getDataFromVar(path1, var1)
    y2 = getDataFromVar(path2, var2)
    index = list(range(0,len(time)))

    data = {'Index': index , 'Time':time , name(path1,var1): y1, name(path2, var2):y2 }
    #col = ['Index', 'Time', name(var)]
    df = pd.DataFrame(data)
    ax.table(cellText=df.values, colLabels=df.columns, loc='center')
    fig.tight_layout()
    plt.show()

"""
