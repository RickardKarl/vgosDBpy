import sys
import os
from PySide2.QtWidgets import QTreeView, QTableView, QAbstractItemView, QTextEdit, QPushButton
from vgosDBpy.model.standardtree import TreeModel
from vgosDBpy.model.table import TableModel

'''
Will soon enough be moved to view folder

'''

class QWrapper(QTreeView):
    '''
    Widget that inherits from QTreeView
    Visual representation of the wrapper as a folder structure

    Imports TreeModel which is the model representation of the wrapper

    Constructor needs:
    root_path [string]
    wrapper_file [string]
    parent [QWidget]

    '''

    def __init__(self, root_path, parent=None):
        super(QWrapper, self).__init__(parent)

        # Setup model
        self.model = TreeModel(['Name'], root_path)
        self.setModel(self.model)

        # Selection of items
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.selection = self.selectionModel()

        # Expansion options
        self.expandToDepth(0)
        self.setExpandsOnDoubleClick(True)

        # Size-related
        self.resizeColumnToContents(0)

class VariableTable(QTableView):
    '''
    Widget that inherits from QTableView
    Visual representation of the items in a table

    Imports TableModel

    Constructor needs:
    parent [QWidget]

    '''
    def __init__(self, parent=None):
        super(VariableTable, self).__init__(parent)

        # Setup model
        self.model = TableModel(['Variables', 'Dimensions'], parent)
        self.setModel(self.model)

        # Selection of items
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.selection = self.selectionModel()

        # Size
        '''
        max_width = self.frameSize().width()
        self.setMaximumWidth(max_width)
        self.setColumnWidth(0, 6/10*max_width)
        self.setColumnWidth(1, 4/10*max_width)
        '''
    def updateVariables(self, var_list):
        '''
        Updates content of table model

        var_list [list of QStandardItems]
        '''
        self.model.updateVariables(var_list)

        # Updates size of column when content is changed
        for i in range(self.model.columnCount()):
            self.resizeColumnToContents(i)
