import importlib.util
import os

def import_func(file, path):
    spec = importlib.util.spec_from_file_location(file, path)
    pack = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pack)
    return pack

Parser = import_func('parser', '/Users/rickardkarlsson/Documents/NVI/vgosDBpy-git/vgosDBpy/wrapper/parser.py').Parser
tree = import_func('tree', '/Users/rickardkarlsson/Documents/NVI/vgosDBpy-git/vgosDBpy/wrapper/tree.py')
Node = tree.Node
NetCDF_File = tree.NetCDF_File

from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2 import QtCore

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

    def __init__(self, header, root_path, wrapper_name, parent=None):
        super(TreeModel,self).__init__(parent)
        self.setupModel(root_path,wrapper_name)


    def flags(self, index):
        '''
        Let's us choose if the selected items should be enabled, editable, etc

        index [QModelIndex]
        '''

        if not index.isValid():
            return 0

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable #| QtCore.Qt.ItemIsEditable # Uncomment if you want to be able to edit it

    # Model setup
    def setupModel(self, root_path, wrapper_name):
        '''
        Parsing the wrapper
        (Imports Parser class)

        root_path [string]
        wrapper_name [string]
        '''
        parser = Parser()
        parser.parseWrapper(root_path + '/' + wrapper_name)
        root_parent = parser.getWrapperRoot()
        self.recursive(root_parent, self.invisibleRootItem())

    def recursive(self, node, parent):
        if node.isNetCDF():
            item = NetCDFItem(node)
        else:
            item = QNodeItem(node)
        print(type(item))
        item = QNodeItem(node)
        parent.appendRow(item)
        if node.hasChildren():
            children = node.getChildren()
            for row in range(node.getChildCount()):
                c = children[row]
                self.recursive(c, item)



class QNodeItem(QStandardItem):
    '''
    Custom data item for the QStandardItemModel

    Not yet fully understood how it works

    Constructor
    node [Node]
    '''
    _type = 1110

    def __init__(self, node):
        super(QNodeItem, self).__init__()
        self.name = str(node)
        self.node = node
        self.path = node.getPath()

        # Attributes
        

    def type(self):
        return QNodeItem._type

    def data(self, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return self.name

        elif role == QtCore.Qt.EditRole:
            return self.node

        else:
            return None

    def setData(self, data, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            self.name = data

        elif role == QtCore.Qt.DisplayRole: # Do not really do anything?
            self.name = data

        else:
            return False

        self.emitDataChanged()
        return True


    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name



class NetCDFItem(QNodeItem):
    _type = 1111

    def __init__(self, node):
        super(NetCDFItem, self).__init__(node)

    def type(self):
        NetCDFItem._type



'''
class NetCDFVariable:
'''
