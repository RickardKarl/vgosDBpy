# tableFunction
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from vgosDBpy.data.PathParser import findCorrespondingTime
from vgosDBpy.data.combineYMDHMS import combineYMDHMwithSec
from vgosDBpy.data.readNetCDF import getDataFromVar
from vgosDBpy.data.getRealName import get_name_to_print as name

"""
Default: shows path´s var against time using a QT tableWidget
returns a tableWidget to be handled somwhere else..
"""
def tableFunction(path, var):
    timePath = findCorrespondingTime(path)
    time = combineYMDHMwithSec(timePath)
    y = getDataFromVar(path, var)
    data = {'Time':time , name(path,var): y }
    return data

def tableFunction2data (path1, var1, path2, var2):
    timePath = findCorrespondingTime(path1)
    time = combineYMDHMwithSec(timePath)
    y1 = getDataFromVar(path1, var1)
    y2 = getDataFromVar(path2, var2)
    data = {'Time':time , name(path1,var1): y1, name(path2, var2):y2 }
    return data


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
