from PySide2.QtGui import QStandardItemModel
from PySide2 import QtCore
import pandas as pd
import numpy as np

from vgosDBpy.model.qtree import Variable, DataValue
from vgosDBpy.data.readNetCDF import get_netCDF_variables, get_dtype_var_str, get_dimension_var, show_in_table
from vgosDBpy.data.combineYMDHMS import combineYMDHMwithSec,findCorrespondingTime
from vgosDBpy.data.getName import get_unit_to_print
from vgosDBpy.data.plotTable import Tablefunction as TF
from vgosDBpy.data.getName import get_name_to_print
from vgosDBpy.model.data_axis import DataAxis

class TableModel(QStandardItemModel):
    '''
    Internal representation of items in a table

    Imports QStandardItemModel
    '''


    # Constructor
    def __init__(self, header, parent=None):
        '''
        header [list of strings] is the header on the top of the table
        parent [QWidget]
        '''
        super(TableModel,self).__init__(parent)
        self._header = header
        self.setHorizontalHeaderLabels(self._header)

    # Set flags
    def flags(self, index):
        '''
        Let us choose if the selected items should be enabled, editable, etc

        index [QModelIndex]
        '''

        if not index.isValid():
            return 0

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable #| QtCore.Qt.ItemIsEditable # Uncomment if you want to be able to edit it

    # Reset method
    def resetModel(self, reset_header = False):
        '''
        Resets content of the table without removing the header
        (Has to be done since clear otherwise would remove the header)

        reset_header [boolean]
        '''
        self.clear()
        if reset_header:
            self._header = []
        self.setHorizontalHeaderLabels(self._header)


    ########### Header methods
    def getHeader(self):
        '''
        Returns list of strings
        '''
        return self._header

    def update_header(self,names):
        '''
        Clears old header and updates it

        names [list of string]
        '''
        self._header = names
        self.setHorizontalHeaderLabels(self._header)

    def append_header(self,names):
        '''
        Append new labels to the header

        names [list of string]
        '''
        for name in names:
            self._header.append(name)
        self.setHorizontalHeaderLabels(self._header)

class VariableModel(TableModel):

    '''
    Internal representation of netCDF variables in a table

    Inherits from TableModel
    '''


    def __init__(self, header, parent=None):
        '''
        header [list of strings] is the header on the top of the table
        parent [QWidget]
        '''
        super(VariableModel,self).__init__(header, parent)

    ########### Update methods ############

    def updateVariables(self, item):
        '''
        USED BY VariableTable

        Resets content and then replaces it with items in the given list

        item [QStandardItems] contains the item which replaces previous content
        '''
        self.resetModel()
        var_list = get_netCDF_variables(item.getPath())
        i = 0
        # Puts variable in first column and associated dimension in another
        for var in var_list:
            if show_in_table(item.getPath(),var):
                self.setItem(i,0,Variable(var,item))
                self.setItem(i,1,Variable(get_unit_to_print(item.getPath(), var),item))
                self.setItem(i,2,Variable(get_dimension_var(item.getPath(), var),item))
                self.setItem(i,3,Variable(get_dtype_var_str(item.getPath(), var),item))
                i += 1


class DataModel(TableModel):

    '''
    Internal representation of data points from netCDF variables in a table

    Inherits from TableModel
    '''

    # Decides which one is the standard time-column when displaying data from plot
    time_col = 0

    # Custom signal to detect when data is changed, used to avoid bugs
    dataChanged_customSignal = QtCore.Signal(int)

    def __init__(self, header, parent=None):
        '''
        header [list of strings] is the header on the top of the table
        parent [QWidget]
        '''
        super(DataModel,self).__init__(header, parent)

        # Class that retrieves data for table
        self.tabfunc = TF()

        # Map to keep track of which column that belongs to each DataAxis (USED BY DataTable)
        self.data_axis = [] # Keep track of the DataAxis that it shows from the plot
        self.time_index = None
        self.dataaxis_to_column_map = {} # DataAxis : Column index
        self.column_to_dataaxis_map = {}



    # Set flags
    def flags(self, index):
        '''
        Let us choose if the selected items should be enabled, editable, etc

        index [QModelIndex]
        '''

        if not index.isValid():
            return 0

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable


    ############# Getter method & setters

    def resetModel(self, reset_header = True):
        '''
        Reset model

        reset_header [boolean]
        '''
        super(DataModel,self).resetModel(reset_header = reset_header)
        self.data_axis = []
        self.time_index = None
        self.tabfunc.data_reset()
        self.tabfunc.header_reset()

    def getAllDataAxis(self):
        '''
        Return list of DataAxis
        '''
        return self.data_axis

    def getExistingItems(self):
        '''
        Return list of QStandardItems
        '''
        items  = []
        for ax in self.data_axis:
            items.append(ax.getItem())
        return items

    def getDataAxis(self, column):
        '''
        Given a table column index, return the corresponding DataAxis

        column [int]
        '''
        return self.column_to_dataaxis_map.get(column)

    def getColumn(self, data_axis):
        '''
        Given a DataAxis, return the corresponding table column index

        data_axis [DataAxis]
        '''
        return self.dataaxis_to_column_map.get(data_axis)

    def getData(self, column_index, data_axis = None, get_time = False):
        '''
        Get data that belongs to a certain table column (or DataAxis)

        column_index [int]
        data_axis [DataAxis]
        get_time [boolean] return the Series with time indices added

        returns a pandas.Series with the column data
        '''

        # List to append data to
        data = []
        if get_time == True:
            time_index = []

        # Get column if a DataAxis is given
        if data_axis != None:
            column_index = self.column_to_dataaxis_map.get(data_axis)

        # Loop through rows of the data table
        for row_index in range(self.rowCount()):

            data.append(self.item(row_index, column_index).value)

            if get_time == True:
                time_index.append(self.item(row_index, DataModel.time_col).value)

        if get_time == True:
            return pd.Series(data, index = time_index)
        else:
            return pd.Series(data)


    def isTimeColumn(self, column_index):
        '''
        Checks if the column is displaying time

        col_index [int]
        '''
        header_label = self._header[column_index]

        return header_label == TF.time_label


    ###########  methods ############
    """
    Updates the data for the table, this is done by using the functions in "plotTable.py"
    input: items[QStandardItems]
    """
    def updateData(self, items):
        '''
        Resets content and then replaces it with data

        item [QStandardItems] contains the item which contains the variable with the data
        '''
        self.resetModel()

        # Retrieve data from items
        if len(items) > 0:
            path = []
            var = []
            for itm in items:
                path.append(itm.getPath())
                var.append(itm.labels)
            data = self.tabfunc.tableFunctionGeneral(path, var) # returns a dictionary
            items = DataModel.updateItems(data, items)


            ### Update data_axis

            # Get time indices if they exists
            for key, var in data.items():
                if key == TF.time_key:
                    self.time_index = var

            # Turn data into DataAxis
            index = 0
            for key, var in data.items():
                if key != TF.time_key:
                    if self.time_index != None:
                        data_series = pd.Series(var, index = self.time_index)
                    else:
                        data_series = pd.Series(var)

                    data_axis = DataAxis(None, data_series, items[index])
                    self.data_axis.append(data_axis)
                    index += 1

            # Update model

            self.updateFromDataAxis(self.data_axis)

        else:
            raise ValueError('Argument items can not be empty.')



    """
    Makes sure that the list of items in syncronized in element and index with the list of data for the table
    input: data: [array[data_arrays[variable_dtype]]], items: [array[Items]]
    output: items [array[items]] - fixed
    """
    def updateItems(data,items):
        names = list(data)
        prev = names[0]
        i = 1
        for j in range(0,len(names)-1):
            prev = prev.split('#')[0]
            name = names[i].split('#')[0]
            if prev == name:
                items.insert(j, items[j-1] )
            prev = names[i]
            i +=  1
        return items

    def appendData(self, items):
        '''

        Resets content and then replaces it with data
        item [QStandardItems] contains the item which contains the variable with the data
        '''
        # Retrieve data from items
        path = []
        var = []
        if len(items) > 0:
            for itm in items:
                path.append(itm.getPath())
                var.append(itm.labels)
            data_new = self.tabfunc.append_table(path, var)
            items = DataModel.updateItems(data_new, items)
            ## Update data_axis
            # Get time indices if they exists
            for key, var in data_new.items():
                if key == TF.time_key:
                    self.time_index = var

            # Turn data into DataAxis
            index = 0
            for key, var in data_new.items():
                if key != TF.time_key:
                    if self.time_index != None:
                        data_series = pd.Series(var, index = self.time_index)
                    else:
                        data_series = pd.Series(var)

                    data_axis = DataAxis(None, data_series, items[index])
                    self.data_axis.append(data_axis)

                    index += 1

            # Updates model
            self.updateFromDataAxis(self.data_axis)

        else:
            raise ValueError('Argument items contains wrong number of items, should be one or two.')

    ######## DataAxis related methods

    def updateFromDataAxis(self, data_axis, get_edited_data = True):
        '''

        Update table model from one/several DataAxis

        data_axis [list of DataAxis] is what should be displayed in the table
        get_edited_data [boolean] decides if edited data or original should be given in the table
        '''

        if len(data_axis) > 0:
            items = []
            for ax in data_axis:
                items.append(ax.getItem())

            ###### Update data in table

            # Get a time index of the series,
            # all axes should have same time indices
            if get_edited_data:
                time_index = data_axis[0].getEditedData().index
            else:
                time_index = data_axis[0].getData().index

            if len(data_axis) != len(items):
                raise ValueError('data_axis and items do no have the same length')

            # Check if time_index is ordinary integer indices or timestamps
            if time_index.dtype == 'datetime64[ns]':
                use_timestamp = True
            else:
                use_timestamp = False

            if use_timestamp is True:
                for i in range(len(time_index)):
                    self.setItem(i, DataModel.time_col, DataValue(time_index[i], node = None, signal = self.dataChanged_customSignal))

            col_index = 0
            for j in range(len(data_axis)):
                # Checks so it does not write in same col as time
                if col_index == DataModel.time_col and use_timestamp:
                    col_index += 1

                # Retrieve pd.Series stored in DataAxis
                if get_edited_data:
                    data = data_axis[j].getEditedData()
                else:
                    data = data_axis[j].getData()

                for i in range(len(data)):

                    data_value = str(data.iloc[i])
                    self.setItem(i, col_index, DataValue(data_value, items[j], signal = self.dataChanged_customSignal))

                self.dataaxis_to_column_map[data_axis[j]] = col_index
                self.column_to_dataaxis_map[col_index] = data_axis[j]

                col_index += 1


            ###### Updates header
            path = []
            var = []
            for itm in items:  #tm in items:
                path.append(itm.getPath())
                var.append(itm.labels)

            header_labels = []
            for v in var:
                header_labels.append(get_name_to_print(v))
                ##################HERE#######################

            if use_timestamp is True:
                header_labels.insert(DataModel.time_col, self.tabfunc.time_label)

            self.update_header(header_labels)

        self.data_axis = data_axis

    def getDataFromSelected(self, selected_items, current_axis):

        '''
        selected_items [list of QModelIndex]
        current_axis [DataAxis]

        return pandas.Series with selected data
        '''
        # Get column from selected data_axis
        current_col = self.dataaxis_to_column_map.get(current_axis)

        time_index = []
        value = []

        # Loop through indices
        for index in selected_items:

            # Get indices in table
            item_col = index.column()
            item_row = index.row()

            # Get item
            item = self.itemFromIndex(index)

            # Checks that it is the correct column
            if item_col != DataModel.time_col and item_col == current_col:

                # Get timestamp
                timestamp = self.item(item_row, DataModel.time_col).value
                time_index.append(timestamp)

                # Get value
                value.append(item.value)

        return pd.Series(value, index = time_index)


    def updateDataAxisfromTable(self):
        '''
        Updates an DataAxis given the data in the table
        '''

        # Loop through all columns
        for column_index in range(self.columnCount()):

            # Checks if time is displayed in that column
            if self.isTimeColumn(column_index):
                continue

            # If not, then we are good
            else:

                # Get DataAxis
                current_data_axis = self.column_to_dataaxis_map.get(column_index)

                if current_data_axis == None:
                    continue

                # Retrieve data
                time_index = []
                data = []

                for row_index in range(self.rowCount()):

                    value = self.item(row_index, column_index).value
                    data.append(value)

                    time_index.append(self.item(row_index, DataModel.time_col).value)

                # Create a pandas.Series and set the edited data for each DataAxis to that
                edited_series = pd.Series(data, index = time_index)
                current_data_axis.setEditedData(edited_series)
