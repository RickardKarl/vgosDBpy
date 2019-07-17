import pandas as pd
from math import ceil, floor

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
        startTime = series.index[0]
        time = []
        for stamp in series.index:
            time.append(stamp)
        correction = startTime.year*365 + 123
        x1 = x1 - correction
        x2 = x2 - correction
        startYear = startTime.year
        x1 = pd.Timedelta(x1, unit = 'D') + pd.Timestamp(year = startYear, month = 1, day = 1, hour = 0)
        x2 = pd.Timedelta(x2, unit = 'D') + pd.Timestamp(year = startYear, month = 1, day = 1, hour = 0)
    else:
        x1 = ceil(x1)
        x2 = floor(x2)
    # Retrieve the correct data
    out = series[x1:x2]
    out = out[y1 < out]
    out = out[out < y2]

    return out
