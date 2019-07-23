import pandas as pd
import numpy as np

class DataAxis:
    '''
    Data structure to keep track of an axis and the data that it is plotting
    This is used to mark data and enables editing of the data
    '''

    def __init__(self, axis, data, node):
        '''
        axis [matplotlib.Axes]
        data [pd.Series]
        node [model.standardtree.Variable]
        '''
        self._axis = axis
        self._data = data
        self._node = node
        self._edited_data = data.copy(deep = True)
        self._marked_data  = []

    def getAxis(self):
        return self._axis

    def getData(self):
        return self._data

    def getNode(self):
        return self._node

    def getEditedData(self):
        return self._edited_data

    def getMarkedData(self):
        return self._marked_data

    def resetEditedData(self):
        self._edited_data = self._data.copy(deep = True)

    def addLine(self, line):
        '''
        line [matplotlib.Line2D]
        '''
        return self._axis.add_line(line)

    def updateMarkedData(self, data, remove_existing = False):
        '''
        data [pd.Series] is the selected data to be added to the marked data list
        remove_existing [bool]

        Updates the marked_data with the currently selected data points
        If remove_existing is True:
            Selected data will be removed if already added to the marked data list
        Else:
            Data from the list will not be removed
        '''
        for point in data.iteritems():
            if point in self._marked_data and remove_existing:
                self._marked_data.remove(point)
            else:
                self._marked_data.append(point)

    def clearMarkedData(self):
        '''
        Unselect all marked data points
        '''
        self._marked_data = []
        self._edited_data = self._data


    def removeMarkedData(self):
        '''
        Replaces all marked data from current data with a NaN
        '''
        for data in self._marked_data:
            self._edited_data[data[0]] = np.nan


    def getNewEdit(self):
        '''
        Returns an edited pd.Series without the current marked data
        '''
        self.resetEditedData()
        self.removeMarkedData()
        return self._edited_data
