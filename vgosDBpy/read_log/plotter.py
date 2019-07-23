import matplotlib.pyplot as plt
import pandas as pd


def plotSeries(series):
    '''
    Plot series [pd.Series]
    '''
    series.plot()
    goodTicks(series, pd.Timedelta(minutes = 6))
    plt.show()


def goodTicks(series, time_delta):
    '''
    series [pd.Series]
    time_delta [pd.Timedelta]

    Return tick labels that have a spacing given by a pandas Timedelta
    '''
    time = series.index
    i = 0
    ticks = []
    ticks_label = []
    prev_stamp = time[0]
    ticks.append(prev_stamp)
    ticks_label.append(createLabel(prev_stamp))

    for stamp in time:
        if stamp - prev_stamp > time_delta:
            ticks.append(stamp)
            ticks_label.append(createLabel(stamp))
            prev_stamp = stamp
        i += 1

    plt.xticks(ticks, ticks_label)

def createLabel(time_stamp):
    '''
    time_stamp [pd.Timestamp]

    Returns string label from a pandas Timestamp
    '''
    label = list(map(str,[time_stamp.hour, time_stamp.minute, time_stamp.second]))
    return ':'.join(label)
