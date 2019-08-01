import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import pandas as pd
from matplotlib.dates import DateFormatter as DF
from netCDF4 import Dataset

from vgosDBpy.data.PathParser import findCorrespondingTime
from vgosDBpy.data.combineYMDHMS import combineYMDHMwithSec
from vgosDBpy.data.readNetCDF import getDataFromVar, header_info_to_plot, read_netCDF_variables, getDataFromVar_multDim, is_TimeDim2, is_multdim_var, is_possible_to_plot,get_data_to_plot
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
class AxisItem():
    def __init__(self):
        self.path  = ''
        self.var = ''
        self.data = ''
        self.isEmpty = True

    def createAxisItem(self,path,var,data):
        self.path  = path
        self.var = var
        self.data = data
        self.isEmpty = False

    def get_axis_lable(self):
        return name(self.path,self.var)+unit(self.path,self.var)

    def empty(self):
        self.path  = ''
        self.var = ''
        self.data = ''
        self.isEmpty = True

    def getPath(self):
        return self.path
    def getVar(self):
        return self.var
    def getData(self):
        return self.data


class Plotfunction_class():

    def __init__(self):
        self.data = []
        self.axis = []
        self.x = AxisItem()
        self.y1 = AxisItem()
        self.y2 = AxisItem()
        self.y = []
        self.place = 0

        self.length_axis = -1

    def clear(self):
        self.data = []
        self.axis = []
        self.x = AxisItem()
        self.y1 = AxisItem()
        self.y2 = AxisItem()
        self.y = []
        self.place = 0
        self.length_axis = -1

    def _clear_axis(self):
        self.axis = []
        self.length_axis = -1

    def _clear_data(self):
        self.data= []

    def _getX(self):
        return  self.x

    def _getY(self):
        return self.y

    def _createAxis(self,fig):
        self.axis.append(fig.add_subplot(1,1,1) )
        self.length_axis = 0

     # instantiate a second y-axis that shares the same x-axis
    def _appendAxis(self):
        self.axis.append(self.axis[0].twinx())
        self.length_axis = 1

    def add_to_x_axis(self,path, var, data):
        self.x.createAxisItem(path,var,data)

    def add_to_y_axis(self,path,var,data):
        if self.y1.isEmpty == True:
            self.y1.createAxisItem(path,var,data)
        elif self.y2.isEmpty == True:
            self.y2.createAxisItem(path,var,data)

    def _add_time_to_xAxis(self,path,var='Time',data= []):
        timePath = findCorrespondingTime(path)
        time_data = []
        time = combineYMDHMwithSec(timePath)
        for t in time:
            time_data.append(t)
        self.add_to_x_axis(path,'Time',time_data)

    def _add_index_to_xAxis(self,path,data):
        nbrIdx = len(data) + 1
        idx = range(1,nbrIdx)
        self.add_to_x_axis(path,'Index', idx)

    def _append_data(self):
        #for itm in self.y1:
        if self.y1.isEmpty == False:
            self.data.append(pd.Series(self.y1.getData(), index = self.x.getData() ) )
        #for im in self.y2:
        if self.y2.isEmpty == False:
            self.data.append(pd.Series(self.y2.getData(), index = self.x.getData() ) )

    # method called from outside
    def plotFunction(self,paths,vars,fig,state):

        #clears all info
        self.clear()
        nbr = len(paths)
        self.place = 0
        if default_time(state) is True and checkIfTimeAvailable(paths, vars) is True :
            plot_to_time = True
        else :
            plot_to_time = False

        """
        So far we are not working with aither data or axis just creating x, y1, y2
        """
        # First find which data that should be x-axis
        # possible options is time, index or data form path.

        if nbr == 1 and plot_to_time is False:
            Temp = get_data_to_plot(paths[0],vars[0])
            self._add_index_to_xAxis(paths[0],Temp)
            self.add_to_y_axis(paths[0],vars[0],Temp)
        else:
            if plot_to_time is True :
                self._add_time_to_xAxis(paths[0])
            else:
                Temp = get_data_to_plot(paths[0],vars[0])
                self.add_to_x_axis(paths[0], vars[0], Temp)
                self.place = 1


            # now we have data stored in x

            # find the data to store in y1 and y2 or just y1

            for i in range(self.place, len(paths) ):
                path = paths[i]
                var = vars[i]
                Temp = get_data_to_plot(path,var)
                #for t in Temp: # might later not be necessary
                self.add_to_y_axis(path,var,Temp)

        """
        now we move on the defining axis and data using x, y1, y2
        """
        # use x, y1 and y2 to generate the axis and sata

        # first handle y1 meaning working with axis[0]
        if self.y1.isEmpty == False:
            self._createAxis(fig)
            color = 'tab:red'
            self.axis[0].set_xlabel(self.x.get_axis_lable())
            self.axis[0].set_ylabel(self.y1.get_axis_lable())
            self.axis[0].plot(self.x.getData(), self.y1.getData(), color=color)
            self.axis[0].tick_params(axis=self.y1.getVar(), labelcolor=color)

        if self.y2.isEmpty == False:
            self._appendAxis() # instantiate a second axes that shares the same x-axis
            color = 'tab:blue'
            self.axis[1].plot(self.x.getData(), self.y2.getData(), color=color)
            self.axis[1].set_ylabel(self.y2.get_axis_lable())
            self.axis[1].tick_params(axis=self.y2.getVar(), labelcolor=color)

        #plt.title(header_info_to_plot(path1)+ "\nPlot " +name(paths[1],vars[1]) + "and " + name(paths[2], vars[2]) + " against " +name(paths[0], vars[0]))
        self._append_data()
        return self.axis, self.data


    #def addToPlotFuntion(self,paths,vars,fig,state):




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

def default_time(state):
    if state == 1:
        return True
    else:
        return False
