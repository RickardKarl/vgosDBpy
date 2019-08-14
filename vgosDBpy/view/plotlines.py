from matplotlib.lines import Line2D
from scipy.signal import savgol_filter
import pandas as pd

def createLine2D(series, marker = None):
    '''
    Returns an artist object [Line2D] which represents the series,
    used for adding new line to an existing axis in matplotlib

    series [pd.Dataframe] is a time series
    marker [string] decides if a marker should be shown for the line
    '''
    return Line2D(series.index, series[:], marker = marker)

def createSmoothCurve(series, window_size = 31, pol_order = 4, return_data = False):
    '''
    Return a dataset [pd.Series or Line2D] that is a smoothened curve of the input data

    series [pd.Dataframe] is a time series
    window_size [int] is the window size of the applied filter, has to be an non-even integer
    pol_order [int] is the highest order of the polynome fitted to the data,
    has to be lower than the window size
    return_data [boolean] decides whether pandas.Series or Line2D should be returned
    '''
    if window_size%2 == 0:
        window_size += 1

    while pol_order > window_size:
        pol_order -= 1
        if pol_order == 1:
            raise ValueError('Polynome order is too small, adjust window size')

    error = True
    while error:

        try:
            data = savgol_filter(series, window_size, pol_order)

        except:
            window_size -= 1

            # Lowest possible window_size. Breaks loop and returns None if true
            if window_size <= pol_order:
                return None
        else:
            error = False


    if return_data:
        return pd.Series(data, index = series.index)
    else:
        return createLine2D(pd.Series(data, index = series.index))


def createMarkedCurve(series, marked_data, return_data = False):
    '''
    Returns curve with the marked data points

    series [pandas.Series] contains the whole dataset
    marked_data [list of int] contains the corresponding integer index in series to each of
    the marked data points
    return_data [boolean] decides whether pandas.Series or Line2D should be returned

    Return Line2D or pandas.Series with marked data
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
