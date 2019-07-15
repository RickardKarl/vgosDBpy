import pandas as pd

class DataAxis:

    def __init__(self, axis, data):

        self._axis = axis
        self._data = data
        self._edited_data = data.copy(deep = True)
        self._marked_data  = []

    def getAxis(self):
        return self._axis

    def getData(self):
        return self._data

    def getEditedData(self):
        return self._edited_data

    def getMarkedData(self):
        return self._marked_data

    def resetEditedData(self):
        self._edited_data = self._data.copy(deep = True)

    def addLine(self, line):
        return self._axis.add_line(line)


    def updateMarkedData(self, data):
        for point in data.iteritems():
            if point in self._marked_data:
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
        Delete all marked data from current data
        '''
        time_stamp = []
        for data in self._marked_data:
            time_stamp.append(data[0])

        self._edited_data.drop(labels = time_stamp, inplace = True, errors = 'ignore')
