import importlib.util
import os
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2 import QtCore

from vgosDBpy.wrapper.parser import Parser
from vgosDBpy.wrapper.tree import Node
#from vgosDBpy.data.readNetCDF import read_netCDF_variables

class TreeModel(QStandardItemModel):
    '''
    Model that represents the wrapper
    It is inherited from QStandardModel which can be used to implement a tree structure
    Is used together with QTreeView to generate a visual representation

    Constructor
    root_path [string]
    wrapper_name [string]
    parent [QWidget]
    '''

    def __init__(self, header, root_path, parent=None):
        super(TreeModel,self).__init__(parent)
        self.setupModel(root_path)
        self.setHorizontalHeaderLabels(header)


    def flags(self, index):
        '''
        Let us choose if the selected items should be enabled, editable, etc

        index [QModelIndex]
        '''

        if not index.isValid():
            return 0

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable #| QtCore.Qt.ItemIsEditable # Uncomment if you want to be able to edit it

    # Model setup
    def setupModel(self, root_path):
        '''
        Parsing the wrapper
        (Imports Parser class)

        root_path [string]
        wrapper_name [string]
        '''
        parser = Parser(root_path)
        parser.parseWrapper(root_path)
        root_parent = parser.getWrapperRoot()
        self.recursive(root_parent, self.invisibleRootItem())

    def recursive(self, node, parent):
        if node.isNetCDF():
            item = NetCDFItem(node)
        else:
            item = QNodeItem(node)
        parent.appendRow(item)
        if node.hasChildren():
            children = node.getChildren()
            for row in range(node.getChildCount()):
                c = children[row]
                self.recursive(c, item)
        else:
            if node.isNetCDF() is False and not node.isHistFile():
                item.appendRow(QStandardItem('Empty'))


class QNodeItem(QStandardItem):
    '''
    Custom data item for the QStandardItemModel

    Constructor
    node [Node]
    '''
    _type = 1110


    def __init__(self, node):
        super(QNodeItem, self).__init__(0,2)
        self.labels = str(node)
        self.node = node

    def getPath(self):
        '''
        Returns path of node
        '''
        return self.node.getPath()

    def getNode(self):
        return self.node

    def isNetCDF(self):
        '''
        Checks if the node points to a netCDF
        '''
        return self.node.isNetCDF()

    def isHistFile(self):
        '''
        Checks if the node points to a .hist file
        '''
        return self.node.isHistFile()

    def type(self):
        return QNodeItem._type

    def data(self, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return self.labels

        elif role == QtCore.Qt.EditRole:
            return self.node

        else:
            return None

    def setData(self, data, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            self.labels = data

        elif role == QtCore.Qt.DisplayRole: # Do not really do anything?
            self.labels = data

        else:
            return False

        self.emitDataChanged()
        return True

    def __str__(self):
        return self.labels

    def __repr__(self):
        return self.labels

    def __hash__(self):
        return hash(self.labels)*33 + hash(self.labels)*22 + hash(str(self.node.parent))*11



class NetCDFItem(QNodeItem):

    '''
    Inherited from QNodeItem

    This should be used to differ QNodeItem which points to netCDF files
    '''

    _type = 1111

    def __init__(self, node):
        super(NetCDFItem, self).__init__(node)

    def type(self):
        NetCDFItem._type



class Variable(QNodeItem):

    '''
    Inherited from QNodeItem

    self.node becomes the NetCDFItem that the variable belongs to
    This should be used to differ variables that are stored in this format which points to netCDF files
    '''

    _type = 1112

    def __init__(self, variable_name, node):
        super(Variable, self).__init__(node)
        self.labels = variable_name

    def type(self):
        NetCDFItem._type


class DataValue(QNodeItem):

    '''
    Inherited from QNodeItem

    This should be used to store single data values from the node
    '''

    _type = 1113

    def __init__(self, value, node):
        super(DataValue, self).__init__(node)
        self.value = value

    def type(self):
        NetCDFItem._type

    def data(self, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return self.value

        elif role == QtCore.Qt.EditRole:
            return self.value

        else:
            return None

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
