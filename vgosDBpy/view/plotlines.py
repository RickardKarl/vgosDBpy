from matplotlib.lines import Line2D
from scipy.signal import savgol_filter
import pandas as pd

def createLine2D(series, marker = None):
    '''
    Returns an artist object [Line2D] which represents the series,
    used for adding new line to an existing axis in matplotlib

    series [pd.Dataframe] is a time series
    '''
    return Line2D(series.index, series[:], marker = marker)

def createSmoothCurve(series, window_size = 19, pol_order = 4):
    '''
    Return a time series [pd.Datafram] that is more smooth

    series [pd.Dataframe] is a time series
    window_size [int] is the window size of the applied filter
    pol_order [int] is the highest order of the polynome fitted to the data,
    has to be lower than the window size and uneven
    '''
    if window_size%2 == 0:
        window_size += 1

    while pol_order > window_size:
        pol_order -= 1
        if pol_order == 1:
            raise ValueError('Polynome order is too small, adjust window size')

    data = savgol_filter(series, window_size, pol_order)
    return createLine2D(pd.Series(data, index = series.index))
