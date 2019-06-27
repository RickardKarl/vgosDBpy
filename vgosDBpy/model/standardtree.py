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

    def __init__(self, header, root_path, wrapper_name, parent=None):
        super(TreeModel,self).__init__(parent)
        self.setupModel(root_path,wrapper_name)

        # Set header
        self.setHorizontalHeaderLabels(header)

    def itemFromIndex(self, index):
        return 1

    # Model setup
    def setupModel(self, root_path, wrapper_name):
        parser = Parser()
        parser.parseWrapper(root_path + '/' + wrapper_name)
        root_parent = parser.getWrapperRoot()
        self.recursive(root_parent, self.invisibleRootItem())

    def recursive(self, node, parent):
        #if not isinstance(node, list):
        #    data = [node]
        if type(node) == tree.NetCDF_File:
            item = NetCDFItem(node)
        else:
            item = QNodeItem(node)
        parent.appendRow(item)
        if node.hasChildren():
            #item.insertChildren(item.childCount(), node.getChildCount(), column)
            children = node.getChildren()
            for row in range(node.getChildCount()):
                c = children[row]
                #item.getChild(row).setData(0,str(c))
                self.recursive(c, item)



class QNodeItem(QStandardItem):
    _type = 1110

    def __init__(self, node):
        super(QNodeItem, self).__init__()
        self.name = str(node)
        self.node = node
        self.path = node.getPath()


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
        super(NetCDFItem, self).__init__()

    def type(self):
        NetCDFItem._type

    def ifChecked(self):
        print(self.name)

'''
class NetCDFVariable:
'''
