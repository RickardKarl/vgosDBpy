from PySide2.QtGui import QStandardItemModel
from PySide2 import QtCore
from vgosDBpy.model.standardtree import Variable, DataValue
from vgosDBpy.data.readNetCDF import read_netCDF_variables, is_possible_to_plot, is_var_constant,read_unit_for_var, is_numScan_or_NumObs, get_dtype_var, read_netCDF_dimension_for_var, get_dataBaseline #read_netCDF_dimension_for_var,
from vgosDBpy.data.PathParser import findCorrespondingTime
from vgosDBpy.data.combineYMDHMS import combineYMDHMwithSec

class TableModel(QStandardItemModel):
    '''
    Internal representation of items in a table

    Imports QStandardItemModel

    Constructor needs:
    header [list of strings] is the header on the top of the table
    parent [QWidget]
    '''

    def __init__(self, header, parent=None):
        super(TableModel,self).__init__(parent)
        self.header = header
        self.setHorizontalHeaderLabels(self.header)

    def update_header(self,names):
        self.header = names
        self.setHorizontalHeaderLabels(self.header)

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
        self.setHorizontalHeaderLabels(self.header)

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
            if is_numScan_or_NumObs(item.getPath(), var) :
                self.setItem(i,0,Variable(var,item))
            #if is_possible_to_plot(item.getPath(), vars):
            #    self.setItem(i,0, Variable(vars,item))

            #elif is_var_constant(item.getPath(), vars):
            #    self.setItem(i,1,Variable(vars,item))
            #    i += 1
                self.setItem(i,1,Variable(read_unit_for_var(item.getPath(), var),item))
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
        '''
        names = list(data)
        self.reset()
        for i in range(0,len(data[names[0]])):
            for j in range (0,len(names)):
                if len(names) > 1:
                    self.setItem(i, j, DataValue(str(data[names[j]][i]), items[j%(len(names)-1)]))
                self.setItem(i, j, DataValue(str(data[names[j]][i]), items[0]))

    def appendData(self, data, item):
        '''
        USED BY DataTable

        Resets content and then replaces it with data

        data [dict] which contains data to fill the table with. E.g. {'time': time, "var_data": var_data}
        item [QStandardItems] contains the item which contains the variable with the data
        '''
        names = list(data)
        name = names[-1]
        d = data[name]
        #self.reset()
        j= len(names)-1
        print(item)
        print(data[name][1])
        for i in range(0,len(data[name])):
            self.setItem(i,j,DataValue(str(data[name][i]), item))

    def clearTable(self):
        self.data = {}
        self.header = []
        self.reset()

        #for i in range(0,len(data[names[0]])):
        #    for j in range (0,len(names)):
        #        self.setItem(i, j, DataValue(str(data[names[j]][i]), items[j%(len(names)-1)]))
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
        self.header = header
        self.setHorizontalHeaderLabels(self.header)

    def update_header(self,names):
        self.header = names
        self.setHorizontalHeaderLabels(self.header)

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
        self.setHorizontalHeaderLabels(self.header)

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
