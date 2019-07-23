import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from vgosDBpy.read_log.plotter import plotSeries

class LogInfo():

    '''
    Class that parses and saves specific variables from a log-fle
    May plot them if needed
    '''

    available_variables = ['temp', 'atmpres', 'relhum','cablecal']

    def __init__(self, file_path):
        '''
        file_path [str] is the path to the log file
        '''
        self.file_path = file_path
        self.variables = LogInfo.readData(file_path)

    def plotVar(self, var):
        '''
        var [str]
        '''
        series = self.getVarData(var)
        plotSeries(series)


    def getVarData(self,var):
        '''
        var [str]
        '''
        if var.lower() in LogInfo.available_variables:
            return self.variables.get(var)
        else:
            raise ValueError('Variable can not be plotted', var)



    def printFile(number_of_lines):
        with open(self.file_path,'r') as src:
            i = 0
            while i < number_of_lines:
                print(line)
                i += 1


    def readData(file_path):
        '''
        Read met data and cablecal from log files
        '''

        Time = []
        Temp = []
        AtmPres = []
        RelHum = []
        CableCal = []
        Time_CableCal = []

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
                    Time.append(LogInfo.createTimeStamp(date,time_stamp))
                    Temp.append(data[0])
                    AtmPres.append(data[1])
                    RelHum.append(data[2]/100)

                if '/cable/' in data:
                    Time_CableCal.append(LogInfo.createTimeStamp(date, time_stamp))
                    data = data.split('/')[-1]
                    CableCal.append(float(data))


        # Met-data
        time_index = pd.DatetimeIndex(Time)
        Temp = pd.Series(Temp, index = time_index, name = 'temp')
        AtmPres = pd.Series(AtmPres, index = time_index, name = 'atmpres')
        RelHum = pd.Series(RelHum, index = time_index, name = 'relhum')

        # CableCal data
        time_index_cablecal = pd.DatetimeIndex(Time_CableCal)
        CableCal = pd.Series(CableCal, index = time_index_cablecal, name = 'cablecal')
        CableCal = CableCal/240000
        CableCal = CableCal - CableCal.mean()
        CableCal = LogInfo.mergeSeries(CableCal, Temp, return_right = False)

        return {'temp':Temp, 'atmpres': AtmPres, 'relhum': RelHum, 'cablecal': CableCal,
        'time': time_index}


    def mergeSeries(series1, series2, timedelta = pd.Timedelta(seconds = 5), return_left = True,
                    return_right = True):
        '''
        Merge two series with similar timestamps
        '''
        # Setup of variables
        index1 = series1.index
        index2 = series2.index
        len1 = len(index1)
        len2 = len(index2)
        min_len = min(len1,len2)
        max_len = max(len1,len2)

        # Start merging
        merged = False
        while not merged:
            bool_arr_min = np.zeros((min_len))
            bool_arr_max = np.zeros((max_len))

            for i in range(min_len):
                for j in range(i, max_len):
                    if len1 < len2:
                        if abs(index1[i] - index2[j]) < timedelta:
                            bool_arr_min[i] = True
                            bool_arr_max[j] = True
                    else:
                        if abs(index1[j] - index2[i]) < timedelta:
                            bool_arr_min[i] = True
                            bool_arr_max[j] = True

            # Condition for succesful merge
            if len(bool_arr_min[bool_arr_min == True]) == len(bool_arr_max[bool_arr_max == True]):
                merged = True
            # Checks if merge failed, will return zero then
            elif timedelta < pd.Timedelta(milliseconds = 1):
                return None
            # Make time restriction harder if merge not succesful
            else:
                 timedelta = timedelta - pd.Timedelta(seconds = 1)

        if len1 < len2:
            series1 = pd.Series(series1[bool_arr_min == True], index = index1[bool_arr_min == True])
            series2 = pd.Series(series2[bool_arr_max == True], index = index2[bool_arr_max == True])
        else:
            series1 = pd.Series(series1[bool_arr_max == True], index = index1[bool_arr_max == True])
            series2 = pd.Series(series2[bool_arr_min == True], index = index2[bool_arr_min == True])
        if return_left and return_right:
            return series1, series2
        elif return_left:
            return series1
        elif return_right:
            return series2
        else:
            return None

    def createTimeStamp(date, time_stamp):
        '''
        Creates a timestamp
        '''
        time_stamp = list(map(int, time_stamp.strip().split(':')))
        date = list(map(int, date))
        time = pd.Timestamp(year = date[0], month = 1, day = 1, hour = time_stamp[0], minute = time_stamp[1], second = time_stamp[2])
        time = time + pd.Timedelta(days = date[1])
        return time

    ############ OLD METHODS THAT HAS BEEN REPLACED  #################
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
                    Time.append(LogInfo.createTimeStamp(date,time_stamp))
                    Temp.append(data[0])
                    AtmPres.append(data[1])
                    RelHum.append(data[2]/100)


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
                    Time.append(LogInfo.createTimeStamp(date, time_stamp))

                    data = data.split('/')[-1]
                    CableCal.append(float(data))

            time_index = pd.DatetimeIndex(Time)
            CableCal = pd.Series(CableCal, index = time_index, name = 'CableCal')

            CableCal = CableCal/240000
            CableCal = CableCal - CableCal.mean()
            return {'CableCal': CableCal, 'Time': time_index}
