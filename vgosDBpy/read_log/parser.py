import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def printFile(file_path, number_of_lines):
    with open(file_path,'r') as src:
        i = 0
        for line in src:
            if i < number_of_lines:
                print(line)
            else:
                break


def readMetData(file_path):
    '''
    Read meteorologic data from log files
    '''
    Time = []
    Temp = []
    AtmPres = []
    RelHum = []

    with open(file_path,'r') as src:
        for line in src:
            # Split string
            line = line.split('.')
            date = line[0:2]
            time_stamp = line[2]
            data = '.'.join(line[3:])

            # Check if correct string (weather data contains /wx/ in line)
            if '/wx/' in data:
                data = data.split('/')[-1].strip().split(',')
                data = list(map(float, data))
                Time.append(createTimeStamp(date,time_stamp))
                Temp.append(data[0])
                AtmPres.append(data[1])
                RelHum.append(data[2])


    # Turn data into time series
    time_index = pd.DatetimeIndex(Time)
    Temp = pd.Series(Temp, index = time_index, name = 'Temp')
    AtmPres = pd.Series(AtmPres, index = time_index, name = 'AtmPres')
    RelHum = pd.Series(RelHum, index = time_index, name = 'RelHum')

    return {'Temp':Temp, 'AtmPres': AtmPres, 'RelHum': RelHum,
    'Time': time_index}

def readCableCal(file_path):
    '''
    Read cal-cable data from log files
    '''
    Time = []
    CableCal = []

    with open(file_path,'r') as src:
        for line in src:
            # Split string
            line = line.split('.')
            date = line[0:2]
            time_stamp = line[2]
            data = '.'.join(line[3:])

            if '/cable/' in data:
                Time.append(createTimeStamp(date, time_stamp))

                data = data.split('/')[-1]
                CableCal.append(float(data))

        time_index = pd.DatetimeIndex(Time)
        CableCal = pd.Series(CableCal, index = time_index, name = 'CableCal')

        return {'CableCal': CableCal, 'Time': time_index}


def mergeSeries(series1, series2, timedelta = pd.Timedelta(seconds = 10), left_index = True):
    '''
    Merge two series with similar timestamps

    NOT WORKING
    '''
    # Setup of variables
    index1 = series1.index
    index2 = series2.index
    len1 = len(index1)
    len2 = len(index2)
    min_len = min(len1,len2)
    max_len = max(len1,len2)

    print('Starting merging')
    merged = False
    while not merged:
        bool_arr_min = np.zeros((min_len))
        bool_arr_max = np.zeros((max_len))

        for i in range(min_len):
            for j in range(i+1, max_len):
                if len1 > len2:
                    if abs(index1[j] - index2[i]) < timedelta:
                        bool_arr_min[i] = True
                        bool_arr_max[j] = True
                else:
                    if abs(index1[i] - index2[j]) < timedelta:
                        bool_arr_min[i] = True
                        bool_arr_max[j] = True

        if len(bool_arr_min[bool_arr_min == True]) == len(bool_arr_max[bool_arr_max == True]):
            merged = True
            print('Merge succesful with largest time difference between series is', timedelta.seconds, 'seconds')
        elif timedelta < pd.Timedelta(milliseconds = 1):
            print('Merge failed')
            return 0
        else:
             timedelta = timedelta - pd.Timedelta(seconds = 1)

    print('Returning merge for equal timestamps within ' + str(timedelta))

    if len1 < len2:
        return None
    else:
        return None
    return merged_series

def createTimeStamp(date, time_stamp):

    time_stamp = list(map(int, time_stamp.strip().split(':')))
    date = list(map(int, date))
    time = pd.Timestamp(year = date[0], month = 1, day = 1, hour = time_stamp[0], minute = time_stamp[1], second = time_stamp[2])
    time = time + pd.Timedelta(days = date[1])
    return time
