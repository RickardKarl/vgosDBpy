from netCDF4 import Dataset
import pandas as pd


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
