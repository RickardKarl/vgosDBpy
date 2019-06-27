import importlib.util
import os

def import_func(file, path):
    spec = importlib.util.spec_from_file_location(file, path)
    pack = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pack)
    return pack

Parser = import_func('parser', '/Users/rickardkarlsson/Documents/NVI/vgosDBpy-git/vgosDBpy/wrapper/parser.py').Parser

from PySide2 import QtCore
from PySide2.QtCore import QAbstractItemModel, QModelIndex


class TreeItem():
    def __init__(self, data, parent = None):
        self.data = data
        assert isinstance(self.data, list), 'Argument of wrong type!'
        self.children = []
        self.parent = parent

    def getChild(self, row):
        return self.children[row]

    def childCount(self):
        return len(self.children)

    def childNumber(self):
        if self.parent != None:
            return self.parent.children.index(self)
        return 0

    def columnCount(self):
        return len(self.data)

    def getParent(self):
        return self.parent

    def getData(self, column):
        return self.data[column]

    def insertChildren(self, position, count, columns):
        if position < 0 or position > len(self.children):
            return False

        for row in range(count):
            data = [None for v in range(columns)]
            item = TreeItem(data, self)
            self.children.insert(position, item)

        return True

    def insertColumns(self, position, columns):
        if position < 0 or position > len(self.data):
            return False

        for column in range(columns):
            self.data.insert(position, None)

        for child in self.children:
            child.insertColumns(position, columns)

        return True

    def removeChildren(self, position, count):
        if position < 0 or position + count > len(self.children):
            return False

        for row in range(count):
            self.children.pop(position)

        return True

    def removeColumns(self, position, columns):
        if position < 0 or position + columns > len(self.data):
            return False

        for column in range(columns):
            self.data.pop(position)

        for child in self.children:
            child.removeColumns(position, columns)

        return True

    def setData(self, column, value):
        if column >= len(self.data) or column < 0:
            return False
        self.data[column] = value
        return True

    def __str__(self):
        return str(self.children)

    def __repr__(self):
        return str(self.children)

class NetCDFItem(TreeItem):
    pass

class TreeModel(QAbstractItemModel):

    # Pre-defined scopes will have the folder made automatically
    scopes = ['session','scan', 'observation', 'station']

    def __init__(self, header, root_path, wrapper_name, parent=None):
        super(TreeModel, self).__init__(parent)
        self.root = TreeItem(header)
        self.setupModel(root_path, wrapper_name)

    #def createIndex(self, row, column):


    ###########################
    # Read data

    def columnCount(self, parent=QModelIndex()):
        return self.root.columnCount()

    def rowCount(self, parent=QModelIndex()):
        parentItem = self.getItem(parent)
        return parentItem.childCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole:
            return None

        item = self.getItem(index)
        return item.getData(index.column())


    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()

        parentItem = self.getItem(parent)
        childItem = parentItem.getChild(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.getParent()

        if parentItem == self.root:
            return QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.root

    ###########################
    # Edit data

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole:
            return False

        item = self.getItem(index)
        accepted = item.setData(index.column(), value)

        if accepted:
            self.dataChanged.emit(index, index)

        return accepted

    def flags(self, index):
        if not index.isValid():
            return 0

        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.root.getData(section)

        return None

    def setHeaderData(self, section, orientation, value, role=QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole or orientation != QtCore.Qt.Horizontal:
            return False

        accepted = self.root.setData(section, value)
        if accepted:
            self.headerDataChanged.emit(orientation, section, section)

        return accepted



    # Inserting and removing
    def insertColumns(self, position, columns, parent=QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)
        success = self.root.insertColumns(position, columns)
        self.endInsertColumns()

        return success

    def insertRows(self, position, rows, parent=QModelIndex()):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows,
                self.root.columnCount())
        self.endInsertRows()

        return success

    def removeColumns(self, position, columns, parent=QModelIndex()):
        self.beginRemoveColumns(parent, position, position + columns - 1)
        success = self.root.removeColumns(position, columns)
        self.endRemoveColumns()

        if self.root.columnCount() == 0:
            self.removeRows(0, rowCount())

        return success

    def removeRows(self, position, rows, parent=QModelIndex()):
        parentItem = self.getItem(parent)

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()

        return success


    # Model setup
    def setupModel(self, root_path, wrapper_name):
        parser = Parser()
        parser.parseWrapper(root_path + '/' + wrapper_name)
        root_parent = parser.getWrapperRoot()
        TreeModel.recursive(root_parent, 0)

    def recursive(node, column):
        parent = node.getParent()
        if node.getParent() == None:
            parent = QModelIndex()

        if type(node) is not list:
            data = [node]
        item = TreeItem(data,parent)
        if node.hasChildren():
            item.insertChildren(item.childCount(), node.getChildCount(), column)
            children = node.getChildren()
            for row in range(node.getChildCount()):
                c = children[row]
                item.getChild(row).setData(0,str(c))
                TreeModel.recursive(c, column + 1)
        

if __name__ == "__main__":
    p = Parser()
    w = p.parseWrapper(wrapper_path)
