# tableFunction
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import pandas as pd
#import qgrid

from matplotlib.dates import DateFormatter as DF

from vgosDBpy.data.PathParser import findCorrespondingTime
from vgosDBpy.data.combineYMDHMS import combineYMDHMwithSec
from vgosDBpy.data.readNetCDF import getDataFromVar
from vgosDBpy.data.getRealName import get_name_to_print as name
"""
from PathParser import findCorrespondingTime
from combineYMDHMS import combineYMDHMwithSec
from readNetCDF import getDataFromVar
from getRealName import get_name_to_print as name
"""
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView
from PyQt5.QtCore import pyqtSlot




"""
misses header and column names
"""
def createTable(data):
    tableWidget = QTableWidget()
    names = list(data)
    #tableWidget.setVerticalHeaderLabels((names[0], names[1]) )
    #tableWidget.setVerticalHeaderItem(('Row 1',' Row 2'))
    tableWidget.setRowCount(len(data['Time']))
    tableWidget.setColumnCount(len(names))
    tableWidget.setColumnWidth(0, 180) # extra long to fit timeStamp
    for i in range(1,len(names)):
        tableWidget.setColumnWidth(i, 80)
    for i in range(0,len(data[names[0]])):
        for j in range (0,len(names)):
            tableWidget.setItem(i, j, QTableWidgetItem(str(data[names[j]][i])))
    tableWidget.move(0, 0)
    return tableWidget

"""

Default: shows path´s var against time using a QT tableWidget
returns a tableWidget to be handled somwhere else..
"""
def tableFunction(path, var):
    timePath = findCorrespondingTime(path)
    time = combineYMDHMwithSec(timePath)
    y = getDataFromVar(path, var)
    data = {'Time':time , name(path,var): y }
    QTable =  createTable(data)
    return QTable

def tableFunction2data (path1, var1, path2, var2):
    timePath = findCorrespondingTime(path1)
    time = combineYMDHMwithSec(timePath)
    y1 = getDataFromVar(path1, var1)
    y2 = getDataFromVar(path2, var2)
    data = {'Time':time , name(path1,var1): y1, name(path2, var2):y2 }
    QTable = createTable(data)
    return QTable
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
path= './../../../../Files/10JAN04XK/WETTZELL/Met.nc'
var = 'AtmPres'
#tableFunction(path,var)
