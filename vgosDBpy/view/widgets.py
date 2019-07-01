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

        # Expand first column
        self.expandToDepth(0)

        # Quality of life features for the QTreeView
        self.setExpandsOnDoubleClick(True)

        #self.setEditTriggers(QAbstractItemView.NoEditTriggers) # Sets through the view so that editing is not possible

        # Size-related
        self.resizeColumnToContents(0)

    def currentSelectionModel(self):
        return self.selectionModel()

    def changeSelection(self):
        pass

    def getSelected(self):
        return self.selection.selectedIndexes()

class VariableTable(QTableView):
        def __init__(self, parent=None):
            super(VariableTable, self).__init__(parent)

            # Setup model
            self.model = TableModel(['Variables'], parent)
            self.setModel(self.model)

        def updateVariables(self, var_list):
            self.model.updateVariables(var_list)
