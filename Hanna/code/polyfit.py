## Using minsta kvadratmetoden to check if data ok####

import numpy as np

def polyfit(xdata, ydata, degree):

    yhat = avitzky_golay(ydata, 51, 3)
