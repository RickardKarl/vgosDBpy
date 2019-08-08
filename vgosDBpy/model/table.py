from PySide2.QtGui import QStandardItemModel
from PySide2 import QtCore
import pandas as pd

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

    Constructor needs:
    header [list of strings] is the header on the top of the table
    parent [QWidget]
    '''


    # Constructor
    def __init__(self, header, parent=None):
        super(TableModel,self).__init__(parent)
        self._header = header
        self.setHorizontalHeaderLabels(self._header)
        self.nbrItems = 0

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
        '''
        self.clear()
        self.nbrItems = 0
        if reset_header:
            self._header = []
        self.setHorizontalHeaderLabels(self._header)


    ########### Header methods
    def getHeader(self):
        return self._header

    def update_header(self,names):
        self._header = names
        self.setHorizontalHeaderLabels(self._header)

    def append_header(self,names):
        for name in names:
            self._header.append(name)
        self.setHorizontalHeaderLabels(self._header)

class VariableModel(TableModel):

    def __init__(self, header, parent=None):
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

    # Decides which one is the standard time-column when displaying data from plot
    time_col = 0

    dataChanged_customSignal = QtCore.Signal(int)

    def __init__(self, header, parent=None):
            super(DataModel,self).__init__(header, parent)

            # Hanna
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
        super(DataModel,self).resetModel(reset_header = reset_header)
        self.data_axis = []
        self.tabfunc.data_reset()
        self.tabfunc.header_reset()

    def getAllDataAxis(self):
        return self.data_axis

    def getExistingItems(self):
        items  = []
        for ax in self.data_axis:
            items.append(ax.getItem())
        return items

    def getDataAxis(self, column):
        return self.column_to_dataaxis_map.get(column)

    def getColumn(self, data_axis):
        return self.dataaxis_to_column_map.get(data_axis)

    def getData(self, column_index, data_axis = None, get_time = False):

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

    ########### Update methods ############

    def updateData(self, items):
        '''
        Resets content and then replaces it with data

        data [dict] which contains data to fill the table with. E.g. {'time': time, "var_data": var_data}
        item [QStandardItems] contains the item which contains the variable with the data
        data_axis [DataAxis] contains a list of DataAxis that corresponds to the data being plotted
        '''
        self.resetModel()

        # Retrieve data from items
        if len(items) > 0:
            path = []
            var = []
            for itm in items:
                path.append(itm.getPath())
                var.append(itm.labels)
            data = self.tabfunc.tableFunctionGeneral(path, var) # returns a map

        ## Update data_axis
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


    def appendData(self, items):
        '''

        Resets content and then replaces it with data

        data [dict] which contains data to fill the table with. E.g. {'time': time, "var_data": var_data}
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
        '''

        if len(data_axis) > 0:
            items = []
            for ax in data_axis:
                items.append(ax.getItem())

            ###### Updates header
            path = []
            var = []
            for itm in items:  #tm in items:
                path.append(itm.getPath())
                var.append(itm.labels)

            header_labels = []
            for v in var:
                header_labels.append(get_name_to_print(path, v))

            header_labels.insert(DataModel.time_col, self.tabfunc.time_label)
            self.update_header(header_labels)

            ###### Update data in table

            # Get a time index of the series,
            # all axes should have same time indices
            if get_edited_data:
                time_index = data_axis[0].getEditedData().index
            else:
                time_index = data_axis[0].getData().index

            if len(data_axis) != len(items):
                raise ValueError('data_axis and items do no have the same length')

            for i in range(len(time_index)):
                self.setItem(i, DataModel.time_col, DataValue(time_index[i], node = None, signal = self.dataChanged_customSignal))

            col_index = 0
            for j in range(len(data_axis)):
                # Checks so it does not write in same col as time
                if col_index == DataModel.time_col:
                    col_index += 1

                # Retrieve pd.Series stored in DataAxis
                if get_edited_data:
                    data = data_axis[j].getEditedData()
                else:
                    data = data_axis[j].getData()

                # Check that the time indices are the same
                if not data.index.equals(time_index):
                    raise ValueError('DataAxis', data_axis[j], 'do not have the same time indices as', data_axis[0])

                for i in range(len(data)):
                    self.setItem(i, col_index, DataValue(str(data[i]), items[j], signal = self.dataChanged_customSignal))

                self.dataaxis_to_column_map[data_axis[j]] = col_index
                self.column_to_dataaxis_map[col_index] = data_axis[j]

                col_index += 1

        self.data_axis = data_axis

    def getDataFromSelected(self, selected_items, current_axis):

        '''
        selected_items [list of QModelIndex]
        current_axis [DataAxis]
        '''
        time_index = []
        value = []
        current_col = self.dataaxis_to_column_map.get(current_axis)

        for index in selected_items:

            # Get indices in table
            item_col = index.column()
            item_row = index.row()

            item = self.itemFromIndex(index)

            if item_col != DataModel.time_col and item_col == current_col:

                # Get timestamp
                timestamp = self.item(item_row, DataModel.time_col).value
                time_index.append(timestamp)

                # Get value
                value.append(item.value)

        return pd.Series(value, index = time_index)


    def updateDataAxisfromTable(self):

        for column_index in range(self.columnCount()):

            if column_index == DataModel.time_col:
                continue

            else:
                current_data_axis = self.column_to_dataaxis_map.get(column_index)

                if current_data_axis == None:
                    continue

                time_index = []
                data = []

                for row_index in range(self.rowCount()):

                    value = self.item(row_index, column_index).value
                    data.append(float(value))

                    time_index.append(self.item(row_index, DataModel.time_col).value)

                edited_series = pd.Series(data, index = time_index)
                current_data_axis.setEditedData(edited_series)
