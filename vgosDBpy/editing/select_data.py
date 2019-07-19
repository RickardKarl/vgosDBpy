import pandas as pd
from math import ceil, floor
from datetime import datetime, timedelta

def getData(x1, x2, y1, y2, series, time_index = 1):
    '''
    Retrieves all data in series such that you return all values between y1 and y2, AND
    with indices between x1 and x2

    x1, x2, y1, y2 [floats], such that x1 < x2 and y1 < y2
    series [pandas.Series]

    out [pd.Series] is the output that follows our requirements

    Something is weird with the date extraction from the selector in plot_widget
    Currently a little hard-coded
    '''

    # First we need to convert indices to the correct time format to compare with indices of the series
    if time_index == 1:
        # x1, x2 are days since 01-01-0001 corresponding to the proleptic Gregorian ordinal
        date_x1 = datetime.fromordinal(int(floor(x1))) + timedelta(days= x1-floor(x1))
        date_x2 = datetime.fromordinal(int(floor(x2))) + timedelta(days= x2-floor(x2))

        x1 = pd.Timestamp(date_x1)
        x2 = pd.Timestamp(date_x2)
    else:
        x1 = ceil(x1)
        x2 = floor(x2)
    # Retrieve the correct data
    if y1 > y2:
        temp = y1
        y1 = y2
        y2 = temp
    out = series[x1:x2]
    out = out[y1 < out]
    out = out[out < y2]

    return out
