from PySide2.QtGui import QStandardItemModel
from PySide2 import QtCore
from vgosDBpy.model.standardtree import Variable, DataValue
from vgosDBpy.data.readNetCDF import read_netCDF_variables, read_netCDF_dimension_for_var, is_possible_to_plot

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
        self.setHorizontalHeaderLabels(header)


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
        Resets content and then replaces it with items in the given list

        item [QStandardItems] contains the item which replaces previous content
        '''
        self.reset()
        var_list = read_netCDF_variables(item.getPath())
        i = 0
        # Puts variable in first column and associated dimension in another
        for vars in var_list:
            if is_possible_to_plot(item.getPath(), vars):
                self.setItem(i,0, Variable(vars,item))
                #self.setItem(i,1,Variable(read_netCDF_dimension_for_var(vars, item.getPath()),item))
                i += 1


    def updateData(self, data, items):
        names = list(data)

        '''
        self.setRowCount(len(data['Time']))
        self.setColumnCount(len(names))
        self.setColumnWidth(0, 180) # extra long to fit timeStamp

        for i in range(1,len(names)):
            self.setColumnWidth(i, 80)
        '''
        self.reset()

        for i in range(0,len(data[names[0]])):
            for j in range (0,len(names)):
                self.setItem(i, j, DataValue(str(data[names[j]][i]), items[j%(len(names)-1)]))
