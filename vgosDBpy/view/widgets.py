
from PySide2.QtWidgets import QTreeView, QTableView, QAbstractItemView
from PySide2.QtCore import QItemSelectionModel
from vgosDBpy.model.standardtree import TreeModel
from vgosDBpy.model.table import TableModel
from vgosDBpy.data.plotTable import Tablefunction as TF

from datetime import datetime
import time

class QWrapper(QTreeView):
    '''
    Widget that inherits from QTreeView
    Visual representation of the wrapper as a folder structure

    Imports TreeModel which is the model representation of the wrapper

    Constructor needs:
    root_path [string] is the path to the root folder of the vgosDB data base
    parent [QWidget]
    '''

    def __init__(self, root_path, parent=None):
        super(QWrapper, self).__init__(parent)

        # Setup model
        self._model = TreeModel(['Name'], root_path)
        self.setModel(self._model)

        # Selection of items
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.selection = self.selectionModel()

        # Expansion options
        self.expandToDepth(0)
        self.setExpandsOnDoubleClick(True)

        # Size-related
        self.resizeColumnToContents(0)

    def getModel(self):
        return self._model

    def getWrapper(self):
        return self._model.getWrapper()

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
        self._model = TableModel(['Name', 'Unit', 'Dimension', 'Dtype'], parent)
        self.setModel(self._model)

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

    def getModel(self):
        return self._model

    def updateVariables(self, var_list):
        '''
        Updates content of table model

        var_list [list of QStandardItems]
        '''
        self._model.updateVariables(var_list)

        # Updates size of column when content is changed
        for i in range(self._model.columnCount()):
            self.resizeColumnToContents(i)

class ConstantTable(QTableView):
    def __init__(self, parent=None):
        super(DataTable,self).__init__(parent)
        self._model = TableModel(' ', parent)
        self.setModel(self._model)

class DataTable(QTableView):
    '''
    Displays data from TableModel which has values from a variable together with timestamp

    parent [QWidget] is the parent widget
    '''

    def __init__(self, parent = None):
        super(DataTable, self).__init__(parent)

        # Setup model
        self._model = TableModel('', parent) # just use the two functions get_name_to_print and get_unit_to_print istead of 'Value'
        self.setModel(self._model)
        self.tabfunc = TF()
        # Selection of items
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.selection = self.selectionModel()

    def updateItems(self,data,items):
        names = list(data)
        prev = names[0]
        i = 1
        for j in range(0,len(names)-1):
            prev = prev.split('#')[0]
            name = names[i].split('#')[0]
            if prev == name:
                items.insert(j, items[j-1] )
            prev = names[i]
            i +=  1
        return items

    def getModel(self):
        return self._model

    def updateColumnSize(self):
        '''
        Updates size of column adjusted after the content
        '''
        for i in range(self._model.columnCount()):
            self.resizeColumnToContents(i)

    def updateData(self, items):
        '''
        Updates the data in the table

        items [list of QNodeItems] contains the nodes which points to the netCDF variables
        that should be displayed
        '''
        path = []
        var = []
        if len(items) > 0 :
            for itm in items:  #tm in items:
                path.append(itm.getPath())
                var.append(itm.labels)
            data = self.tabfunc.tableFunctionGeneral(path, var)
            self._model.update_header(self.tabfunc.return_header_names(path,var))
        else:
            raise ValueError('Argument items can not be empty.')

        # Update Items incase one path gave several data arrays
        items = self.updateItems(data,items)

        # Updates model
        self._model.updateData(data, items)

        # Updates size of column when content is changed
        self.updateColumnSize()


    def appendData(self,items):
        '''
        Updates the data in the table

        items [list of QNodeItems] contains the nodes which points to the netCDF variables
        that should be displayed
        '''
        path = []
        var = []
        if len(items) > 0:
            for itm in items:  #tm in items:
                path.append(itm.getPath())
                var.append(itm.labels)
            data_new = self.tabfunc.append_table(path, var)
            data_all = self.tabfunc.get_table()
            self._model.update_header(self.tabfunc.append_header(path,var))
        else:
            raise ValueError('Argument items contains wrong number of items, should be one or two.')

        items = self.updateItems(data_new, items)
        # Updates model
        self._model.appendData(data_new,items)

        # Updates size of column when content is changed
        self.updateColumnSize()

    def clearTable(self):
        self._model.clearTable()
        self.setModel(self._model)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.selection = self.selectionModel()
        self.tabfunc.data_reset()
        self.tabfunc.header_reset()

    def updateFromDataAxis(self, data_axis):
        '''
        Updates the table by giving it the data_axis, this gives a one to one correspondance with
        the plot
        '''
        if len(data_axis) > 0:
            items = []
            for ax in data_axis:
                items.append(ax.getItem())

            # Update values in table
            self._model.updateFromDataAxis(data_axis)

            # Updates header
            path = []
            var = []
            for itm in items:  #tm in items:
                path.append(itm.getPath())
                var.append(itm.labels)
            header_labels = self.tabfunc.return_header_names(path,var)
            #header_labels[0]=TF.time_label
            self._model.update_header(header_labels)

        # Updates size of column when content is changed
        self.updateColumnSize()

    def updateMarkedRows(self, data_axis):
        '''
        data_axis [DataAxis]

        Mark selected data from plot in the table
        '''

        self.selection.clear()


        for ax in data_axis:
            column_index = self._model.dataaxis_to_column_map[ax]
            selected_data = ax.getMarkedData()

            for row_index in selected_data:
                for col_index in range(self._model.columnCount()):
                    model_item = self._model.item(row_index, col_index)
                    item_index = self._model.indexFromItem(model_item)

                    self.selection.select(item_index, QItemSelectionModel.Select) # This line takes a lot of time to execute, needs fix
