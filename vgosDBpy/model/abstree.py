from PySide2.QtCore import QAbstractItemModel
from vgosDBpy.wrapper.representation import Node

class TreeModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super(TreeModel, self).__init__(parent)


    def index(row, column, QIndex):
        pass
        # Call createIndex()
        # Return QModelIndex

    def parent(QChild):
        pass
        # Return QModelIndex

    def rowCount(QIndex):
        pass
        # Return int which is the number of rows under the given parent
        # = Number of children under parent

    def columnCount(QIndex):
        pass
        # Return int which is the number of columns for
        # the children of the given parent


    def data(QIndex, role):
        pass
        # role is int
        # Returns data stored at the index
