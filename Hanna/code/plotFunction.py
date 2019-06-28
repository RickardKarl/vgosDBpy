import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import pandas as pd
from matplotlib.dates import DateFormatter as DF
import os

def plotFunc( strX,xAxis,strY,yAxis, isTime):
    """
    TODO: write a code so that titel, legends and so on can be
    produces automatically based on some into, path or node
    Also do better code to handle Timestamp labels
    """
    if isTime is 1:
        myFmt = md.DateFormatter("%H:%M:%S")
        plt.xticks( rotation= 80 )
        ax.xaxis.set_major_formatter(myFmt);

    plt.plot(xAxis,yAxis)
    plt.title(" ")
    plt.show()

def plot2Axis(xAxis, yAxis1, yAxis2, isTime):
    if isTime is 1:
         myFmt = md.DateFormatter("%H:%M:%S")
         fig, ax =  plt.subplots()
         plt.xticks( rotation= 80 )
         ax.xaxis.set_major_formatter(myFmt);

    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('time (s)')
    ax1.plot(xAxis, yAxis1, color=color)
    ax1.tick_params(axis='y1', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    #ax2.set_ylabel('sin', color=color)  # we already handled the x-label with ax1
    ax2.plot(xAxis, yAxis2, color=color)
    ax2.tick_params(axis='y2', labelcolor=color)
        #plt.plot(xAxis,yAxis)
        #plt.title(" over obsvervation: 10 JAN 04 KOKEE ")
    plt.show()

    def swapAxis(xAxis, yAxis, isTime):
        plotFunc(yAxis,xAxis, isTime)

    def swapAxis2(xAxis, yAxis1, yAxis2, isTime):
        plot2Axis(yAxis2, xAxis,yAxis1, isTime)
