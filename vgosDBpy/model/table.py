from PySide2.QtGui import QStandardItemModel
from PySide2 import QtCore
from vgosDBpy.model.standardtree import Variable
from vgosDBpy.data.readNetCDF import read_netCDF_vars

class TableModel(QStandardItemModel):

    def __init__(self, header, parent=None):
        super(TableModel,self).__init__(parent)
        self.setHorizontalHeaderLabels(header)


    def flags(self, index):
        '''
        Let us choose if the selected items should be enabled, editable, etc

        index [QModelIndex]
        '''

        if not index.isValid():
            return 0

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable #| QtCore.Qt.ItemIsEditable # Uncomment if you want to be able to edit it


    def updateVariables(self, item):
        var_list = read_netCDF_vars(item.getPath())
        item_list = []
        i = 0
        for vars in var_list:
            self.setItem(i,0, Variable(vars,item))
            i += 1
        #self.appendColumn(var_list)
