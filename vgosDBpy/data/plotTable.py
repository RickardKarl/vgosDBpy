# tableFunction

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
import os


"""

"""
Default: shows path´s var against time.
"""
def tableFunction(path, var):
    """
    fig, ax = plt.subplots()

    # hide axes
    fig.patch.set_visible(False)
    #ax.axis('off')
    ax.axis('tight')

    #collect all data
    timePath = findCorrespondingTime(path)
    time = combineYMDHMwithSec(timePath)
    y = getDataFromVar(path, var)
    index = list(range(0,len(time)))

    data = {'Index': index , 'Time':time , name(path,var): y }
    """
    plt.set_visible(False)
    plt.axis('off')
    plt.axis('tight')
    timePath = findCorrespondingTime(path)
    time = combineYMDHMwithSec(timePath)
    y = getDataFromVar(path, var)
    index = list(range(0,len(time)))
    data = {'Index': index , 'Time':time , name(path,var): y }
    df = pd.DataFrame(data)
    def display_():
        pd.set_option("display.max_rows", None)
        from IPython.core.display import display
        display(df)
    plt.table(cellText=df.values, colLabels=df.columns, loc='center')
    #display_()
    #fig.tight_layout()

    plt.show()

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
