import pandas as pd

def getData(x1, x2, y1, y2, series):
    x1 = pd.Timestamp(x1, unit = 's').time()
    x2 = pd.Timestamp(x2, unit = 's').time()
    x = series[x1:x2]
    #print([y1 < x])
    print(x)
