from netCDF4 import Dataset
import pandas as pd
import os

"""
Takes in a path to a TimeUTC.nc file and combines the YMDHM data
with the second to create a YMDHMS format.
Uses panda to create Timestamp.
"""
def combineYMDHMwithSec(timeFilePath):
    with Dataset(timeFilePath,"r", format="NETCDF4_CLASSIC") as time :

        seconds = time.variables["Second"]
        YMDHM = time.variables["YMDHM"]
        if len(seconds) != len(YMDHM):
            return null

        YMDHMS = []

        for i in range(len(YMDHM)):
            YMDHMS.append(pd.Timestamp(int(YMDHM[i][0]),int(YMDHM[i][1]),int(YMDHM[i][2]),int(YMDHM[i][3]),int(YMDHM[i][4]),int(seconds[i])))
    return YMDHMS

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
        y = get_data_to_plot(path,vars[c])
        if len(time_data) != len(y[0]):
            return False
        c += 1
    return True

def default_time(state):
    if state == 1:
        return True
    else:
        return False

def findCorrespondingTime(path):
    time_path = ""
    if os.path.isfile(path):
        parts = path.split("/")
        parts[-1] = 'TimeUTC.nc'
        time_path = '/'.join(parts)
        if os.path.isfile(time_path):
            return time_path
        else:
             return ""
