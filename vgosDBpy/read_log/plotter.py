import matplotlib.pyplot as plt
import pandas as pd
from vgosDBpy.read_log.parser import readData


def plotSeries(series):
    series.plot()
    goodTicks(series, pd.Timedelta(minutes = 6))
    plt.show()


def goodTicks(series, time_delta):
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
    label = list(map(str,[time_stamp.hour, time_stamp.minute, time_stamp.second]))
    return ':'.join(label)
