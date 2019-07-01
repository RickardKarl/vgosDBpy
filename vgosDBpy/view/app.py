import sys
import os
from PySide2.QtWidgets import QApplication, QTreeView, QAbstractItemView, QWidget, QTextEdit, QPushButton, QVBoxLayout, QGridLayout
from PySide2 import QtCore
from vgosDBpy.model.standardtree import TreeModel
from vgosDBpy.model.toolbox import Tools
from vgosDBpy.view.widgets import QWrapper, VariableTable
from vgosDBpy.data.readNetCDF import read_netCDF_vars, read_netCDF_vars_info, read_netCDF_dimension_for_var
from vgosDBpy.data.plot import plot_2

class App(QWidget):
    '''
    Frame for testing stuff
    '''

    def __init__(self, wrapper_path, parent = None):
        super(App,self).__init__(parent)


        # Creating widgets
        # Wrapper view
        self.treeview = QWrapper(wrapper_path, self)

        # Text
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)

        # Button
        self.button = QPushButton('& Plot',self)
        # Button event
        self.button.clicked.connect(self._plotbutton)

        # Tools
        #self.toolbox = Tools(self)

        # Table
        self.table = VariableTable(self)

        # Layout
        layout = QGridLayout()
        layout.addWidget(self.treeview,0,0)
        layout.addWidget(self.text,0,1)
        layout.addWidget(self.button,3,0)
        layout.addWidget(self.table, 2,0)
        self.setLayout(layout)

        # Listeners
        self.treeview.selectionModel().selectionChanged.connect(self._showItemInfo)

    def _getSelected(self, widget):
        return widget.getSelected()

    def _showItemInfo(self):
        index = self._getSelected(self.treeview)
        if not index == []:
            item = self.treeview.model.itemFromIndex(index[0])
            if item.isNetCDF():
                text = read_netCDF_vars_info(item.getPath())
                self.text.setPlainText(str(text))
                self.table.updateVariables(item)

    def _plotbutton(self):
        index = self._getSelected(self.table)
        if not index == []:
            items = []
            for i in range(2):
                items.append(self.table.model.itemFromIndex(index[i]))
        plot_2(items[0].getPath(), items[0].labels, items[1].getPath(), items[1].labels)
