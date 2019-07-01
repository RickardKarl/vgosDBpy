import matplotlib.pyplot as plt
import pandas as pd

def readMetData(file_path):
    Time = []
    Temp = []
    AtmPres = []
    RelHum = []

    with open(file_path,'r') as src:
        i = 0
        for line in src:
            # Split string
            line = line.split('.')
            date = line[0:1]
            time_stamp = line[2]
            data = '.'.join(line[3:])

            # Check if correct string (weather data contains /wx/ in line)
            if '/wx/' in data:
                data = data.split('/')[-1].strip().split(',')

                createTimeStamp(date,time_stamp)
                Time = time_stamp
                Temp.append(data[0])
                AtmPres.append(data[1])
                RelHum.append(data[2])

    plt.plot(Temp)
    plt.plot(AtmPres)
    plt.show()



def createTimeStamp(date, time_stamp):

    time_stamp = int(time_stamp.strip().split(':'))
    time = pd.Timestamp(year = date[0], month = 0, day = 0, hour = time_stamp[0], minute = time_stamp[1], second = time_stamp[2])
    time = time + pd.Timedelta(days = time_stamp[1])
    print(time)
