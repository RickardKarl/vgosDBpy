from PySide2.QtGui import QStandardItemModel
from PySide2 import QtCore
from vgosDBpy.model.standardtree import Variable
from vgosDBpy.data.readNetCDF import read_netCDF_vars, read_netCDF_dimension_for_var

class TableModel(QStandardItemModel):

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
        self.clear
        self.setHorizontalHeaderLabels(self.header)

    def updateVariables(self, item):
        self.reset()
        var_list = read_netCDF_vars(item.getPath())
        i = 0
        for vars in var_list:
            self.setItem(i,0, Variable(vars,item))
            self.setItem(i,1,Variable(read_netCDF_dimension_for_var(vars, item.getPath()),item))
            #self.item(i,1).setSelectable(False) Doesnt make any difference currently
            #self.item(i,1).setCheckable(False)
            i += 1
