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

def createSmoothCurve(series, window_size = 31, pol_order = 4, return_data = False):
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
    if return_data:
        return pd.Series(data, index = series.index)
    else:
        return createLine2D(pd.Series(data, index = series.index))


def createMarkedCurve(series, marked_data, return_data = False):
    '''
    Return Line2D with marked data

    '''
    index_list = []
    for index in marked_data:
        index_list.append(index)
    marked_series = series.take(index_list)

    line = createLine2D(pd.Series(marked_series))
    line.set_marker('s')
    line.set_linestyle('None')

    if return_data:
        return marked_series
    else:
        return line
