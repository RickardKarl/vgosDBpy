import pandas as pd
import numpy as np

class DataAxis:

    def __init__(self, axis, data, node = None):

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
        return self._axis.add_line(line)

    def updateMarkedData(self, data, remove_existing = False):
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
        self.resetEditedData()
        self.removeMarkedData()
        return self._edited_data
