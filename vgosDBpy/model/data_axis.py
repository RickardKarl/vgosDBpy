import pandas as pd
import numpy as np

from vgosDBpy.view.plotlines import createLine2D, createSmoothCurve, createMarkedCurve


class DataAxis:
    '''
    Data structure to keep track of an Axes and the data that it is plotting
    This is used to mark data and enables editing of the data
    '''

    def __init__(self, axes, data, item):
        '''
        Axes [matplotlib.Axes]
        data [pd.Series]
        item [model.standardtree.Variable]
        '''
        self._axes = axes
        self._data = data
        self._edited_data = data.copy(deep = True)
        self._marked_data  = [] # Indices of data points in self._data that has been marked

        self._item = item

        if self.axisExists():
            ### Lines that belongs to the axes
            if len(axes.get_lines()) > 1:
                raise ValueError('Too many lines in Axes, need to fix.', axes.get_lines())

            self.main_curve = axes.get_lines()[0] # Saves the curve for edited data (where marked data is hidden)

            self.smooth_curve = self._axes.add_line(createSmoothCurve(self._data)) # Saves the smooth curve
            self.smooth_curve.update_from(self.main_curve)

            self.marked_data_curve = self._axes.add_line(createMarkedCurve(self._data, self._marked_data)) # Saves marked data points to plot

            self.smooth_curve.set_visible(False)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._item == other.getItem() and self._data.equals(other.getData())
        else:
            return False

    def __hash__(self):
        series_data = self._edited_data.values # Gives a numpy array
        return hash(self._item)*22 + hash(series_data.tostring())*11 # Combines has of the node and the numpy array

    def axisExists(self):
        return self._axes != None

    ########## Getters and setters

    def getAxis(self):
        return self._axes

    def getData(self):
        return self._data

    def getItem(self):
        return self._item

    def getEditedData(self):
        return self._edited_data

    def setEditedData(self, edited_data):
        self._edited_data = edited_data

    def getMarkedData(self):
        return self._marked_data

    def resetEditedData(self):
        self._edited_data = self._data.copy(deep = True)

    def clearMarkedData(self):
        '''
        Unselect all marked data points
        '''
        self._marked_data = []

    ######### Appearance methods

    def setMarkerSize(self, marker_size):
        if self.axisExists():
            self.main_curve.set_markersize(marker_size)
            self.smooth_curve.set_markersize(marker_size)
            self.marked_data_curve.set_markersize(marker_size*1.2)

    def displayMainCurve(self, bool):
        if self.axisExists():
            if bool == True:
                self.main_curve.set_linestyle('-')
            else:
                self.main_curve.set_linestyle('None')

    def displayMarkers(self, bool):
        if self.axisExists():
            if bool == True:
                self.main_curve.set_marker('o')
            else:
                self.main_curve.set_marker('None')

    def displayMarkedDataCurve(self, bool):
        if self.axisExists():
            self.marked_data_curve.set_visible(bool)

    def displaySmoothCurve(self, bool):
        if self.axisExists():
            self.smooth_curve.set_visible(bool)



    ######### Update methods

    def addLine(self, line):
        '''
        line [matplotlib.Line2D]
        '''
        if self.axisExists():
            return self._axes.add_line(line)

    def updateLines(self):
        if self.axisExists():
            self.main_curve.set_ydata(self._edited_data)

            smooth_data = createSmoothCurve(self._edited_data, return_data = True)
            self.smooth_curve.set_ydata(smooth_data.array)

            marked_data = createMarkedCurve(self._edited_data, self._marked_data, return_data = True)
            self.marked_data_curve.set_ydata(marked_data.array)
            self.marked_data_curve.set_xdata(marked_data.index)

    def getNewEdit(self):
        '''
        Returns an edited pd.Series without the current marked data
        '''
        self.removeMarkedData()
        return self._edited_data

    ######### Marked data methods

    def updateMarkedData(self, data, remove_existing = False):
        '''
        data [pd.Series] is the selected data to be added to the marked data list
        remove_existing [bool]

        Updates the marked_data with the indices of the currently selected data points
        if remove_existing is True:
            Selected data will be removed if already added to the marked data list
        else:
            Data from the list will not be removed
        '''
        time_index = self._data.index
        for point in data.iteritems():
            integer_index = time_index.get_loc(point[0])
            if integer_index in self._marked_data and remove_existing:
                self._marked_data.remove(integer_index)
            else:
                self._marked_data.append(integer_index)

    def removeMarkedData(self):
        '''
        Replaces all marked data from current data with a NaN
        '''
        for index in self._marked_data:
            self._edited_data[index] = np.nan


    #### Class methods

    def lineExists(line):
        if line != None:
            if line.axes != None:
                return True
            else:
                return False
        else:
            return False
