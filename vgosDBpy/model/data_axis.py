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

            smooth_curve = createSmoothCurve(self._data)
            if type(smooth_curve) == None:
                self.smooth_curve = None
            else:
                self.smooth_curve = self._axes.add_line(smooth_curve) # Saves the smooth curve
                self.smooth_curve.update_from(self.main_curve)
                self.smooth_curve.set_visible(False)


            self.marked_data_curve = self._axes.add_line(createMarkedCurve(self._data, self._marked_data)) # Saves marked data points to plot



    def __eq__(self, other):
        '''
        Makes it possible to use the equal operator with this Class
        other [Object]
        '''
        if isinstance(other, self.__class__):
            return self._item == other.getItem() and self._data.equals(other.getData())
        else:
            return False

    def __hash__(self):
        '''
        Hash-function
        '''
        series_data = self._edited_data.values # Gives a numpy array
        return hash(self._item)*22 + hash(series_data.tostring())*11 # Combines has of the node and the numpy array

    def axisExists(self):
        '''
        Check if this DataAxis has a plot axis
        '''
        return self._axes != None

    ########## Getters and setters

    def getAxis(self):
        '''
        Return matplotlib.Axes
        '''
        return self._axes

    def getData(self):
        '''
        Return data belonging to this DataAxis [pandas.Series]
        '''
        return self._data

    def getItem(self):
        '''
        Returns model.standardtree.Variable
        '''
        return self._item

    def getEditedData(self):
        '''
        Returns edited data [pandas.Series]
        '''
        return self._edited_data

    def getMarkedData(self):
        '''
        Return list of int
        '''
        return self._marked_data

    def setEditedData(self, edited_data):
        '''
        edited_data [pandas.Series]
        '''

        self._edited_data = edited_data

    def resetEditedData(self):
        '''
        Reset edited_data to original data
        '''
        self._edited_data = self._data.copy(deep = True)

    def clearMarkedData(self):
        '''
        Unselect all marked data points
        '''
        self._marked_data = []

    ######### Appearance methods

    def setMarkerSize(self, marker_size):
        '''
        Set marker size for all lines in the DataAxis

        marker_size [float]
        '''
        if self.axisExists():
            if DataAxis.lineExists(self.main_curve):
                self.main_curve.set_markersize(marker_size)
            if DataAxis.lineExists(self.smooth_curve):
                self.smooth_curve.set_markersize(marker_size)
            if DataAxis.lineExists(self.marked_data_curve):
                self.marked_data_curve.set_markersize(marker_size*1.2)

    def displayMainCurve(self, bool):
        '''
        Decides whether to display main line with the data

        bool [boolean]
        '''
        if self.axisExists():
            if bool == True:
                self.main_curve.set_linestyle('-')
            else:
                self.main_curve.set_linestyle('None')

    def displayMarkers(self, bool):
        '''
        Decides whether to display markers on the main line

        bool [boolean]
        '''
        if self.axisExists():
            if bool == True:
                self.main_curve.set_marker('o')
            else:
                self.main_curve.set_marker('None')

    def displayMarkedDataCurve(self, bool):
        '''
        Decides whether to display the markers with marked data

        bool [boolean]
        '''
        if self.axisExists():
            self.marked_data_curve.set_visible(bool)

    def displaySmoothCurve(self, bool):
        '''
        Decides whether to display a smoothened fit of the main line

        bool [boolean]
        '''
        if self.axisExists():
            if DataAxis.lineExists(self.smooth_curve):
                self.smooth_curve.set_visible(bool)



    ######### Update methods

    def addLine(self, line):
        '''
        Add line to this DataAxis instance

        line [matplotlib.Line2D]
        '''
        if self.axisExists():
            return self._axes.add_line(line)

    def updateLines(self):
        '''
        Updates the data to all of the lines in this DataAxis
        '''
        if self.axisExists():
            self.main_curve.set_ydata(self._edited_data)

            smooth_data = createSmoothCurve(self._edited_data, return_data = True)
            if type(smooth_data) != None:
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
        Updates the marked_data with the indices of the currently selected data points


        data [pd.Series] is the selected data to be added to the marked data list
        remove_existing [bool]

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
        '''
        Check if the line exists be seeing if it belongs to any matplotlib.Axes
        
        line [matplotlib.lines.line2D]
        '''
        if line != None:
            if line.axes != None:
                return True
            else:
                return False
        else:
            return False
