from PySide2.QtGui import QStandardItemModel
from PySide2 import QtCore
from vgosDBpy.model.standardtree import Variable
from vgosDBpy.data.readNetCDF import read_netCDF_variables, read_netCDF_dimension_for_var

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
        self.clear
        self.setHorizontalHeaderLabels(self.header)

    def updateVariables(self, item_list):
        '''
        Resets content and then replaces it with items in the given list

        item_list [list of QStandardItems] contains the item which replaces previous content
        '''
        self.reset()
        var_list = read_netCDF_variables(item.getPath())
        i = 0

        # Puts variable in first column and associated dimension in another
        for vars in var_list:
            self.setItem(i,0, Variable(vars,item))
            self.setItem(i,1,Variable(read_netCDF_dimension_for_var(vars, item.getPath()),item))
            i += 1
