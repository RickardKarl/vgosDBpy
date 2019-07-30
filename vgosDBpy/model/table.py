from PySide2.QtGui import QStandardItemModel
from PySide2 import QtCore
import pandas as pd

from vgosDBpy.model.standardtree import Variable, DataValue
from vgosDBpy.data.readNetCDF import read_netCDF_variables, is_possible_to_plot, is_var_constant, is_numScan_or_NumObs, get_dtype_var, read_netCDF_dimension_for_var, get_dataBaseline , show_in_table#read_netCDF_dimension_for_var,
from vgosDBpy.data.PathParser import findCorrespondingTime
from vgosDBpy.data.combineYMDHMS import combineYMDHMwithSec
from vgosDBpy.data.getRealName import get_unit_to_print

class TableModel(QStandardItemModel):
    '''
    Internal representation of items in a table

    Imports QStandardItemModel

    Constructor needs:
    header [list of strings] is the header on the top of the table
    parent [QWidget]
    '''

    time_col = 0

    def __init__(self, header, parent=None):
        super(TableModel,self).__init__(parent)
        self._header = header
        self.setHorizontalHeaderLabels(self._header)
        self.nbrItems = 0

        # Map to keep track of which column that belongs to each DataAxis
        self.data_axis = None # Keep track of the DataAxis that it shows from the plot
        self.dataaxis_to_column_map = {} # DataAxis : Column index
        self.column_to_dataaxis_map = {}

    def getHeader(self):
        return self._header

    def update_header(self,names):
        self._header = names
        self.setHorizontalHeaderLabels(self._header)

    def flags(self, index):
        '''
        Let us choose if the selected items should be enabled, editable, etc

        index [QModelIndex]
        '''

        if not index.isValid():
            return 0

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable #| QtCore.Qt.ItemIsEditable # Uncomment if you want to be able to edit it


    def reset(self):
        '''
        Resets content of the table without removing the header
        (Has to be done since clear otherwise would remove the header)
        '''
        self.clear()
        self.setHorizontalHeaderLabels(self._header)


    def updateVariables(self, item):
        '''
        USED BY VariableTable

        Resets content and then replaces it with items in the given list

        item [QStandardItems] contains the item which replaces previous content
        '''
        self.reset()
        var_list = read_netCDF_variables(item.getPath())
        i = 0
        # Puts variable in first column and associated dimension in another
        for var in var_list:
            if show_in_table(item.getPath(),var):
                self.setItem(i,0,Variable(var,item))
            #if is_possible_to_plot(item.getPath(), vars):
            #    self.setItem(i,0, Variable(vars,item))

            #elif is_var_constant(item.getPath(), vars):
            #    self.setItem(i,1,Variable(vars,item))
            #    i += 1
                self.setItem(i,1,Variable(get_unit_to_print(item.getPath(), var),item))
                self.setItem(i,2,Variable(read_netCDF_dimension_for_var(item.getPath(), var),item))
                self.setItem(i,3,Variable(get_dtype_var(item.getPath(), var),item))
            #    j=2
                i += 1

    def updateData(self, data, items):
        '''
        USED BY DataTable

        Resets content and then replaces it with data

        data [dict] which contains data to fill the table with. E.g. {'time': time, "var_data": var_data}
        item [QStandardItems] contains the item which contains the variable with the data
        data_axis [DataAxis] contains a list of DataAxis that corresponds to the data being plotted
        '''
        names = list(data)
        self.reset()
        #self.clearTable()
        for i in range(0,len(data[names[0]])):
            for j in range (0,len(names)):
                if len(names) > 1:
                    self.setItem(i, j, DataValue(str(data[names[j]][i]), items[j%(len(names)-1)]))
                else:
                    self.setItem(i, j, DataValue(str(data[names[j]][i]), items[0]))

        self.nbrItems = len(names)

    def appendData(self, data_new, item):
        '''
        USED BY DataTable

        Resets content and then replaces it with data

        data [dict] which contains data to fill the table with. E.g. {'time': time, "var_data": var_data}
        item [QStandardItems] contains the item which contains the variable with the data
        '''
        names = list(data_new)
        start = self.nbrItems
        #print('Start:'+str(start))
        #self.reset()
        for i in range(0,len(data_new[names[0]])):
            for j in range (0,len(names)):
                if len(names) > 1:
                    self.setItem(i, start+j, DataValue(str(data_new[names[j]][i]), item[j%(len(names)-1)]))
                else:
                    self.setItem(i, start+j, DataValue(str(data_new[names[j]][i]), item[0]))
        self.nbrItems += len(names)

        #names = list(data)
        #name = names[-1]
        #d = data[name]
        #self.reset()
        #j= len(names)-1
        #print(item)
        #print(data[name][1])
        #for i in range(0,len(data[name])):
        #    self.setItem(i,j,DataValue(str(data[names][i]), item))

    def clearTable(self):
        self._header = []
        self.reset()
        self.nbrItems = 0
        #self._header = []
        self.setHorizontalHeaderLabels(self._header)
        #self.data_axis = None # Keep track of the DataAxis that it shows from the plot
        #self.dataaxis_to_column_map = {} # DataAxis : Column index


    def updateFromDataAxis(self, data_axis):
        '''
        Update table model from one/several DataAxis

        data_axis [list of DataAxis] is what should be displayed in the table
        '''

        if len(data_axis) > 0:
            items = []
            for ax in data_axis:
                items.append(ax.getItem())

            time_index = data_axis[0].getData().index # Get a time index of the series,
                                                      # all axes should have same time indices

            if len(data_axis) != len(items):
                raise ValueError('data_axis and items do no have the same length')
            for i in range(len(time_index)):
                self.setItem(i, TableModel.time_col, DataValue(time_index[i], node = None))

            col_index = 0
            for j in range(len(data_axis)):

                # Checks so it does not write in same col as time
                if col_index == TableModel.time_col:
                    col_index += 1

                data = data_axis[j].getData() # Retrieve pd.Series stored in DataAxis

                # Check that the time indices are the same
                # np.array_equal(a1, a2)
                if not data_axis[j].getData().index.equals(time_index):
                    raise ValueError('DataAxis', data_axis[j], 'do not have the same time indices as', data_axis[0])

                for i in range(len(data)):
                    self.setItem(i, col_index, DataValue(str(data[i]), items[j]))

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

            if item_col != TableModel.time_col and item_col == current_col:

                # Get timestamp
                timestamp = self.item(item_row, TableModel.time_col).value
                time_index.append(timestamp)

                # Get value
                value.append(item.value)

        return pd.Series(value, index = time_index)


"""
class DataTableModel(QStandardItemModel):

    '''
    Internal representation of items in a table

    Imports QStandardItemModel

    Constructor needs:
    header [list of strings] is the header on the top of the table
    parent [QWidget]
    '''

    def __init__(self, header, parent=None):
        super(DataTableModel,self).__init__(parent)
        self._header = header
        self.setHorizontalHeaderLabels(self._header)

    def update_header(self,names):
        self._header = names
        self.setHorizontalHeaderLabels(self._header)

    def flags(self, index):
        '''
        Let us choose if the selected items should be enabled, editable, etc

        index [QModelIndex]
        '''

        if not index.isValid():
            return 0

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable #| QtCore.Qt.ItemIsEditable # Uncomment if you want to be able to edit it


    def reset(self):
        '''
        Resets content of the table without removing the header
        (Has to be done since clear otherwise would remove the header)
        '''
        self.clear()
        self.setHorizontalHeaderLabels(self._header)

    def updateData(self, data, items):
        '''
        USED BY DataTable

        Resets content and then replaces it with data

        data [dict] which contains data to fill the table with. E.g. {'time': time, "var_data": var_data}
        item [QStandardItems] contains the item which contains the variable with the data
        '''
        names = list(data)
        self.reset()

        for i in range(0,len(data[names[0]])):
            for j in range (0,len(names)):
                self.setItem(i, j, DataValue(str(data[names[j]][i]), items[j%(len(names)-1)]))


    def append_data(self, data, items):
        names = list(data)

        for i in range(0,len(data[names[0]])):
            for j in range (0,len(names)):
                self.setItem(i, j, DataValue(str(data[names[j]][i]), items[j%(len(names)-1)]))
"""
