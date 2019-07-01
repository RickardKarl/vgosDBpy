import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import pandas as pd
from matplotlib.dates import DateFormatter as DF
import os
from vgosDBpy.data.PathParser import findCorrespondingTime
from vgosDBpy.data.combineYMDHMS import combineYMDHMwithSec
from vgosDBpy.data.readNetCDF import getDataFromVar

# default plot mot tiden
def PlotToRickard(path, var):
    timePath = findCorrespondingTime(path)
    time = combineYMDHMwithSec(timePath)
    y = getDataFromVar(path, var)
    if len(time) == len(y):
        plt.title("plot " + var + " versus Time ")
        plt.plot(time,y)
        plt.show()
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
        ax1.plot(time, y1, color=color)
        ax1.tick_params(axis=var1, labelcolor=color)
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:blue'
        #ax2.set_ylabel('sin', color=color)  # we already handled the x-label with ax1
        ax2.plot(time, y2, color=color)
        ax2.tick_params(axis=var2, labelcolor=color)
            #plt.plot(xAxis,yAxis)
        plt.title("Plot" +var1 + "and " + var2 + "over time ")
        plt.show()
    else:
        print("Dimensions do not agree")


"""
    def swapAxis(xAxis, yAxis, isTime):
        plotFunc(yAxis,xAxis, isTime)

    def swapAxis2(xAxis, yAxis1, yAxis2, isTime):
        plot2Axis(yAxis2, xAxis,yAxis1, isTime)
"""
