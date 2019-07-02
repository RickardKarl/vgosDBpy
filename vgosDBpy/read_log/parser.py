import matplotlib.pyplot as plt
import pandas as pd


def printFile(file_path, number_of_lines):
    with open(file_path,'r') as src:
        i = 0
        for line in src:
            if i < number_of_lines:
                print(line)
            else:
                break


def readMetData(file_path):
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
    Temp = pd.Series(Temp, index = time_index)
    AtmPres = pd.Series(AtmPres, index = time_index)
    RelHum = pd.Series(RelHum, index = time_index)

    return {'Temp':Temp, 'AtmPres': AtmPres, 'RelHum': RelHum,
    'Time': time_index}

def readCableCal(file_path):
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
        CableCal = pd.Series(CableCal, index = time_index)

        return {'CableCal': CableCal, 'Time': time_index}

def createTimeStamp(date, time_stamp):

    time_stamp = list(map(int, time_stamp.strip().split(':')))
    date = list(map(int, date))
    time = pd.Timestamp(year = date[0], month = 1, day = 1, hour = time_stamp[0], minute = time_stamp[1], second = time_stamp[2])
    time = time + pd.Timedelta(days = date[1])
    return time
