import pandas as pd

def getData(x1, x2, y1, y2, series):
    '''
    Something is weird with the date extraction from the selector in plot_widget
    Currently a little hard-coded

    '''
    time = []
    startTime = series.index[0]
    for stamp in series.index:
        time.append(stamp)

    correction = startTime.year*365 + 123
    x1 = x1 - correction
    x2 = x2 - correction
    startYear = startTime.year
    x1 = pd.Timedelta(x1, unit = 'D') + pd.Timestamp(year = startYear, month = 1, day = 1, hour = 0)
    x2 = pd.Timedelta(x2, unit = 'D') + pd.Timestamp(year = startYear, month = 1, day = 1, hour = 0)

    out = series[x1:x2]
    out = out[y1 < out]
    out = out[out < y2]

    return out
