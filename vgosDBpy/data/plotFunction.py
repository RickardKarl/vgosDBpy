import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import pandas as pd
from matplotlib.dates import DateFormatter as DF

from vgosDBpy.data.PathParser import findCorrespondingTime
from vgosDBpy.data.combineYMDHMS import combineYMDHMwithSec
from vgosDBpy.data.readNetCDF import getDataFromVar, header_info_to_plot
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
    if len(paths) != len(vars): # controll
        return

    if default_time(state) is False:
            plot_no_time(paths, vars, fig)
    else:
        plot_time(paths, vars, fig)

def plot_no_time(paths, vars, fig):
    if len(paths) == 2:
        plot_two_vars(paths, vars, fig)
    elif: len(paths) == 3:
        plot_three_vars(paths, vars, fig)

def plot_two_vars(paths, vars, fig):

    # retrive data to plot
    x = getDataFromVar(paths[0], vars[0])
    y = getDataFromVar(paths[1], vars[1])

    #create figure
    ax = fig.add.subplot(1,1,1)
    ax.set_title(header_info_to_plot(paths[0]) + '\n' + 'Plot' + name(paths[0], vars[0]) + 'versus ' + name(paths[1], vars[1] )
    ax.plot(x,y)
    ax.set_xlabel(name(paths[0],vars[0])+unit(paths[0],vars[0]))
    ax.set_ylabel(name(paths[1],vars[1])+unit(paths[1],vars[1]))

    return ax, pd.Series(y, index = x)

def plot_three_vars(paths, vars, fig):

    #retrive data
    x = getDataFromVar(paths[0], vars[0])
    y1 = getDataFromVar(paths[1], vars[1])
    y2 = getDataFromVar(paths[2], vars[2])

    ax1 = fig.add_subplot(1,1,1)
    color = 'tab:red'
    ax1.set_xlabel(name(paths[0],vars[0])+unit(paths[0],vars[0]))
    ax1.set_ylabel(name(paths[1],vars[1])+unit(paths[1],vars[1]))
    ax1.plot(x, y1, color=color)
    #plt.xticks( rotation= 80 )
    ax1.tick_params(axis=vars[1], labelcolor=color)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    #ax2.set_ylabel('sin', color=color)  # we already handled the x-label with ax1
    ax2.plot(x, y2, color=color)
    ax2.set_ylabel(name(paths[2],vars[2])+unit(paths[2],vars[2]))
    ax2.tick_params(axis=vars[2], labelcolor=color)
        #plt.plot(xAxis,yAxis)
    plt.title(header_info_to_plot(path1)+ "\nPlot " +name(paths[1],vars[1]) + "and " + name(paths[2], vars[2]) + " against " +name(paths[0], vars[0]))

    return ax1, ax2


# default plot mot tiden
def plotVariable(path, var, figure):
    ax = figure.add_subplot(1,1,1)
    timePath = findCorrespondingTime(path)
    time_plot= []

    y = getDataFromVar(path, var)
    if timePath != "":
        time = combineYMDHMwithSec(timePath)
        #time_plot=[]
        for t in time:
            time_plot.append( t.time() )
        ax.set_title(header_info_to_plot(path)+ "\n " + "Plot " + name(path,var) + " versus Time " )
    else:
        time_plot = range(0,len(y))
        ax.set_title(header_info_to_plot(path)+ "\n " + "Plot " + name(path,var) )

    if len(time) == len(y):
        #plt.title("Plot " + name(path,var) + " versus Time ")
        #plt.title(header_info_to_plot(path)+ "\n "  "Plot " + name(path,var) + " versus Time " )

        #myFmt = md.DateFormatter("%H:%M:%S")
        plt.xticks( rotation= 80 )
        #ax.xaxis.set_major_formatter(myFmt);

        #myFmt = md.DateFormatter("%H:%M:%S")
        #plt.xticks( rotation= 80 )
        #plt.xlabel.set_major_formatter(myFmt)

        ax.plot(time_plot,y)
        ax.set_xlabel('Time H:M:S')
        ax.set_ylabel(name(path,var)+unit(path,var))
        #plt.show()
        #plt.tight_layout()

        return ax, pd.Series(y, index = time_plot)
    else:
        print("Dimensions do not agree")


def plotVariable2yAxis(path1, var1, path2, var2, fig):
    timePath = findCorrespondingTime(path1)
    time= combineYMDHMwithSec(timePath)

    time_plot= []
    i=0
    for t in time:
        time_plot.append( t.time() )
    y1 = getDataFromVar(path1, var1)
    y2 = getDataFromVar(path2, var2)
    if len(time) == len(y1) and len(time) == len(y2):
        ax1 = fig.add_subplot(1,1,1)
        color = 'tab:red'
        ax1.set_xlabel('Time H:M:S')
        ax1.set_ylabel(name(path1,var1)+ unit(path1,var1))
        ax1.plot(time_plot, y1, color=color)
        plt.xticks( rotation= 80 )
        ax1.tick_params(axis=var1, labelcolor=color)
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:blue'
        #ax2.set_ylabel('sin', color=color)  # we already handled the x-label with ax1
        ax2.plot(time_plot, y2, color=color)
        ax2.set_ylabel(name(path2,var2)+ unit(path2,var2))
        ax2.tick_params(axis=var2, labelcolor=color)
            #plt.plot(xAxis,yAxis)
        plt.title(header_info_to_plot(path1)+ "\nPlot " +name(path1,var1) + "and " + name(path2, var2) + " over time ")

        return ax1, ax2
    else:
        print("Dimensions do not agree")

def default_time(state):

"""
    def swapAxis(xAxis, yAxis, isTime):
        plotFunc(yAxis,xAxis, isTime)

    def swapAxis2(xAxis, yAxis1, yAxis2, isTime):
        plot2Axis(yAxis2, xAxis,yAxis1, isTime)
"""
