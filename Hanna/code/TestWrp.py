# test to learn what a wrapper is
from numpy.random import uniform

import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import pandas as pd
# to formate x axis date
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import os
from netCDF4 import Dataset
location="./Files/10JAN04XK"
filename= "./Files/10JAN04XK/10JAN04XK_V005_iGSFC_kall.wrp"
file = open(filename, "r")
line= file.readline()
while (line is not "Default_Dir"):
    for line in file:
        print(line)
    #    a=2




lookingfor="Met";

if lookingfor is "Met":
    path=location+"/KOKEE/met.nc"
    str= "./Files/10JAN04XU/KOKEE/"+lookingfor+".nc"
    #print(str)
    File1=Dataset(str,"r",format="NETCDF4")

"""
# does the file exist?
for line in file :
    while (line is not "Default_Dir"):
        print(line)
    else :
        break


"""

"""
pathToFolder="./Files/10JAN04XK" # for example

#def createWrp (pathToFolder):
    # print header
header = "! This file contains the following: \n! Information contained in NGS cards. \n! Information required for normal solve processing. \n! Other information in the super files. \n! Almost all information from the database "
print(header)

#begin history
print("! Begin History")


# session informaion



"""


"""
for root, dirs, files in os.walk("./Files"):
    level = root.replace("./Files/10JAN04XK", '').count(os.sep)
    indent = ' ' * 4 * (level)
    print('{}{}/'.format(indent, os.path.basename(root)))
    subindent = ' ' * 4 * (level + 1)
    for f in files:
        print('{}{}'.format(subindent, f))
"""
