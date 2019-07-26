import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import pandas as pd
from matplotlib.dates import DateFormatter as DF
from netCDF4 import Dataset

from vgosDBpy.data.PathParser import findCorrespondingTime
from vgosDBpy.data.combineYMDHMS import combineYMDHMwithSec
from vgosDBpy.data.readNetCDF import getDataFromVar, header_info_to_plot, read_netCDF_variables, getDataFromVar_multDim,  getDataFromVar_multDim_first
from vgosDBpy.data.getRealName import get_name_to_print as name, get_unit_to_print as unit
"""
from PathParser import findCorrespondingTime
from combineYMDHMS import combineYMDHMwithSec
from readNetCDF import getDataFromVar
from getRealName import get_name_to_print as name
"""
import os
from datetime import datetime


"""
ALWYAS CALL THIS METHOD FROM OUTSIDE THIS FILE
"""
def plot_generall (paths, vars, fig, state): # generall function tahta is always called from other function then calls the other functions.
    # need to check if the variables tried to plot have several objects in paths
    """
    c = 0
    marker = -1
    for path in paths:
        with Dataset(path, 'r', format='NETCDF4_CLASSIC') as nc:
            if len(nc.variables[vars[c].strip()].get_dims()) > 1:
                marker = c
                length = len(nc.variables[vars[c].strip()].get_dims())
                c += 1
    """
    marker = is_multdim_var(paths, vars)
    print(marker)
    if len(paths) != len(vars): # controll
        return
    if default_time(state) is True and checkIfTimeAvailable(paths, vars) is True :
        return ( plot_time(paths, vars,fig, marker) )
    else:
        return ( plot_no_time(paths, vars, fig, marker) )
    #else: # Have to handel this
    #    return OBS_plot(paths, vars, fig)
"""
def all_paths_same_length(paths, vars):
    for path in
"""
def is_multdim_var(paths, vars):
    marker = -1
    c=0
    for path in paths:
        with Dataset(path, 'r', format='NETCDF4_CLASSIC') as nc:
            if len(nc.variables[vars[c].strip()].get_dims()) > 1:
                marker = c
            c += 1
    return marker

def checkIfTimeAvailable(paths,vars):
    c = 0
    for path in paths:
        timePath = findCorrespondingTime(path)
        if timePath is "":
            return False
        time_data = []
        time = combineYMDHMwithSec(timePath)
        for t in time:
            time_data.append(t)
        y = getDataFromVar(path,vars[c])
        if len(time_data) != len(y):
            return False
        c += 1
    return True

def plot_no_time(paths, vars, fig, marker = -1):
    if len(paths) == 2:
        return ( plot_two_vars(paths, vars, fig, marker) )
    elif len(paths) == 3:
        return ( plot_three_vars(paths, vars, fig, marker) )
    elif len(paths) == 1:
        return plot_one_var(paths, vars, fig, marker)

def plot_time(paths, vars, fig, marker = -1):
    if len(paths) == 1:
        return ( plot_var_time(paths[0], vars[0], fig, marker) )
    elif  len(paths) == 2:
        return ( plot_two_var_time(paths, vars, fig, marker) )

def plot_one_var (paths, vars, fig, marker = -1):
    if marker != -1:
        y = detDataFromVar_multdim_first(paths[0],vars[0])
    else:
        y = getDataFromVar(paths[0],vars[0])

    x = range(1,len(y)+1)
    axis = []
    data = []
    axis.append(fig.add_subplot(1,1,1))
    axis[0].plot(x,y)
    axis[0].set_title(header_info_to_plot(paths[0]) + '\n' + 'Plot' + name(paths[0], vars[0]) )
    axis[0].set_xlabel('Index')
    axis[0].set_ylabel(name(paths[0],vars[0])+unit(paths[0],vars[0]))
    data.append( pd.Series(y,index=x) )
    return axis, data


def plot_two_vars(paths, vars, fig, marker = -1):

    # retrive data to plot
    if marker == 0 :
        x = detDataFromVar_multdim_first(paths[0],vars[0])
    else:
        x = getDataFromVar(paths[0], vars[0])
    if marker == 1:
        y = detDataFromVar_multdim_first(paths[1],vars[1])
    else:
        y = getDataFromVar(paths[1], vars[1])
    axis = []
    data = []
    #create figure
    axis.append(fig.add_subplot(1,1,1))
    axis[0].plot(x,y)
    axis[0].set_title(header_info_to_plot(paths[0]) + '\n' + 'Plot' + name(paths[0], vars[0]) + 'versus ' + name(paths[1], vars[1] ) )
    #ax.plot(x,y)
    axis[0].set_xlabel(name(paths[0],vars[0])+unit(paths[0],vars[0]))
    axis[0].set_ylabel(name(paths[1],vars[1])+unit(paths[1],vars[1]))
    data.append( pd.Series(y,index=x) )
    return axis, data

def plot_three_vars (paths,vars,fig, marker = -1) :
    #retrive data
    axis = []
    data= []

    #get data
    if marker == 0:
        x = detDataFromVar_multdim_first(paths[0],vars[0])
    else:
        x = getDataFromVar(paths[0], vars[0])

    if marker == 1:
        y1 = detDataFromVar_multdim_first(paths[1],vars[1])
    else:
        y1 = getDataFromVar(paths[1], vars[1])

    if marker == 2:
        y2 = detDataFromVar_multdim_first(paths[2],vars[2])
    else:
        y2 = getDataFromVar(paths[2], vars[2])

    axis.append(fig.add_subplot(1,1,1))

    #first y-axis
    color = 'tab:red'
    axis[0].set_xlabel(name(paths[0],vars[0])+unit(paths[0],vars[0]))
    axis[0].set_ylabel(name(paths[1],vars[1])+unit(paths[1],vars[1]))
    axis[0].plot(x, y1, color=color)
    axis[0].tick_params(axis=vars[1], labelcolor=color)

    #second y-axis
    axis[1] = axis[0].twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    axis[1].plot(x, y2, color=color)
    axis[1].set_ylabel(name(paths[2],vars[2])+unit(paths[2],vars[2]))
    axis[1].tick_params(axis=vars[2], labelcolor=color)
    plt.title(header_info_to_plot(path1)+ "\nPlot " +name(paths[1],vars[1]) + "and " + name(paths[2], vars[2]) + " against " +name(paths[0], vars[0]))
    data.append( pd.Series(y1, index = x) )
    data.append( pd.Series(y2, index = x) )
    return axis, data

def plot_var_time(path, var, fig, marker = -1):

    #retrive time data and if not possible just return
    axis = []
    data = []

    timePath = findCorrespondingTime(path)
    if timePath is "":
        return
    time_data = []
    time = combineYMDHMwithSec(timePath)
    for t in time:
        time_data.append(t)
    #retive y-axis data
    if marker != -1:
        y = getDataFromVar_multDim_first(path, var)
    else:
        y = getDataFromVar(path,var)

    #Create plot
    axis.append( fig.add_subplot(1,1,1) )
    axis[0].set_title(header_info_to_plot(path)+ "\n " + "Plot " + name(path,var) + " versus Time " )
    if len(time_data) == len(y):
        #axis[0].xticks(rotation= 80)
        axis[0].plot(time_data, y)
        axis[0].set_xlabel('Time')
        axis[0].set_ylabel(name(path,var)+unit(path,var))
        #axis[0].set_xticklabels(axis[0].get_xticklabels(), rotation=80)
        data.append(pd.Series(y, index = time_data ))
    else:
        raise ValueError('Time and data do not have same length')
    return axis, data





def plot_two_var_time (paths, vars, fig, marker = -1):

    # Define return arrays'
    axis = []
    data = []

    #try to retrive time data, if can not just return
    timePath = findCorrespondingTime(paths[0])
    time= combineYMDHMwithSec(timePath)
    time_data=[]
    i=0
    for t in time:
        time_data.append(t)
    # retriv y-axis data
    if marker == 0:
        y1 = detDataFromVar_multdim_first(paths[0],vars[0])
    else:
        y1 = getDataFromVar(paths[0], vars[0])

    if marker == 1:
        y2 = detDataFromVar_multdim_first(paths[1],vars[1])
    else:
        y2 = getDataFromVar(paths[1], vars[1])

    if len(time) == len(y1) and len(time) == len(y2):
        axis.append(fig.add_subplot(1,1,1))
        #ax1 = fig.add_subplot(1,1,1)
        color = 'tab:red'
        axis[0].set_xlabel('Time H:M:S')
        axis[0].set_ylabel(name(paths[0],vars[0])+ unit(paths[0],vars[0]))
        axis[0].plot(time_data, y1, color=color)
        #plt.xticks( rotation= 80 )
        axis[0].tick_params(axis=vars[0], labelcolor=color)
        axis.append( axis[0].twinx() )  # instantiate a second y-axis that shares the same x-axis
        color = 'tab:blue'
        axis[1].plot(time_data, y2, color=color)
        axis[1].set_ylabel(name(paths[1],vars[1])+ unit(paths[1],vars[1]))
        axis[1].tick_params(axis=vars[1], labelcolor=color)
        plt.title(header_info_to_plot(paths[0])+ "\nPlot " +name(paths[0],vars[0]) + "and " + name(paths[1], vars[1]) + " over time ")
        data.append(pd.Series(y1, index = time_data))
        data.append(pd.Series(y2, index = time_data))
        return axis, data
    else:
        print("Dimensions do not agree")

def OBS_plot(paths, vars, fig):
    #retrive time data and if not possible just return
    axis = []
    data = []
    Y = getDataFromVar_multDim(paths[0], vars[0])
    y1 = np.squeeze(np.asarray(Y[:][0]))
    y2 = np.squeeze(np.asarray(Y[:][1]))
    timePath = findCorrespondingTime(paths[0])
    if timePath is not "":
        time_data = []
        time = combineYMDHMwithSec(timePath)
        for t in time:
            time_data.append(t)
    else:
        time = range(1, len(y1)+1 )
        time_data = time

    #retive y-axis data

    #y = getDataFromVar(path,var)

    #Create plot
    if len(time) == len(y1) and len(time) == len(y2):
        axis.append(fig.add_subplot(1,1,1))
        #ax1 = fig.add_subplot(1,1,1)
        color = 'tab:red'
        axis[0].set_xlabel('Time H:M:S')
        axis[0].set_ylabel(name(paths[0],vars[0])+ unit(paths[0],vars[0]))
        axis[0].plot(time_data, y1, color=color)
        #plt.xticks( rotation= 80 )
        axis[0].tick_params(axis=vars[0], labelcolor=color)
        axis.append( axis[0].twinx() )  # instantiate a second y-axis that shares the same x-axis
        color = 'tab:blue'
        axis[1].plot(time_data, y2, color=color)
        #axis[1].set_ylabel(name(paths[1],vars[1])+ unit(paths[1],vars[1]))
        #axis[1].tick_params(axis=vars[1], labelcolor=color)
        plt.title(header_info_to_plot(paths[0])+ "\nPlot " +name(paths[0],vars[0]) +" over time ")
        data.append(pd.Series(y1, index = time_data))
        data.append(pd.Series(y2, index = time_data))
    return axis, data


def default_time(state):
    if state == 1:
        return True
    else:
        return False
