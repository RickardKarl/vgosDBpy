import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import pandas as pd
from matplotlib.dates import DateFormatter as DF

from vgosDBpy.data.PathParser import findCorrespondingTime
from vgosDBpy.data.combineYMDHMS import combineYMDHMwithSec
from vgosDBpy.data.readNetCDF import getDataFromVar
from vgosDBpy.data.getRealName import get_name_to_print as name, get_unit_to_print as unit
"""

from PathParser import findCorrespondingTime
from combineYMDHMS import combineYMDHMwithSec
from readNetCDF import getDataFromVar
from getRealName import get_name_to_print as name
"""
import os

# default plot mot tiden
def PlotToRickard(path, var):
    timePath = findCorrespondingTime(path)
    time = combineYMDHMwithSec(timePath)
    y = getDataFromVar(path, var)

    if len(time) == len(y):
        plt.title("Plot " + name(path,var) + " versus Time ")
        plt.plot(time,y)

        #myFmt = md.DateFormatter("%H:%M:%S")
        #plt.xticks( rotation= 80 )
        #plt.xlabel.set_major_formatter(myFmt)

        plt.xlabel('Time H:M:S')
        plt.ylabel(name(path,var)+unit(path,var))
        plt.show()
        plt.tight_layout()
    else:
        print("Dimensions do not agree")

def PlotToRickard2yAxis(path1, var1, path2, var2):
    timePath = findCorrespondingTime(path1)
    time= combineYMDHMwithSec(timePath)
    y1 = getDataFromVar(path1, var1)
    y2 = getDataFromVar(path2, var2)
    if len(time) == len(y1) and len(time) == len(y2):
        fig, ax1 = plt.subplots()
        color = 'tab:red'
        ax1.set_xlabel('time')
        ax1.set_ylabel(name(path1,var1)+ unit(path1,var1))
        ax1.plot(time, y1, color=color)
        ax1.tick_params(axis=var1, labelcolor=color)
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:blue'
        #ax2.set_ylabel('sin', color=color)  # we already handled the x-label with ax1
        ax2.plot(time, y2, color=color)
        ax2.set_ylabel(name(path2,var2)+ unit(path2,var2))
        ax2.tick_params(axis=var2, labelcolor=color)
            #plt.plot(xAxis,yAxis)
        plt.title("Plot " +name(path1,var1) + "and " + name(path2, var2) + " over time ")
        plt.show()
        plt.tight_layout()
    else:
        print("Dimensions do not agree")


"""
    def swapAxis(xAxis, yAxis, isTime):
        plotFunc(yAxis,xAxis, isTime)

    def swapAxis2(xAxis, yAxis1, yAxis2, isTime):
        plot2Axis(yAxis2, xAxis,yAxis1, isTime)
"""
