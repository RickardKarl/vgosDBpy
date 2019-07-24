
from PySide2.QtWidgets import QTreeView, QTableView, QAbstractItemView

from vgosDBpy.model.standardtree import TreeModel
from vgosDBpy.model.table import TableModel
from vgosDBpy.data.plotTable import Tablefunction as TF

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
        self.model = TableModel(['Name', 'Unit'], parent)
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

class ConstantTable(QTableView):
    def __init__(self, parent=None):
        super(DataTable,self).__init__(parent)
        self.model = TableModel(' ', parent)
        self.setModel(self.model)

class DataTable(QTableView):
    '''
    Displays data from TableModel which has values from a variable together with timestamp

    parent [QWidget] is the parent widget
    '''

    def __init__(self, parent = None):
        super(DataTable, self).__init__(parent)
        #self.table = Table()
        # Setup model
        self.model = TableModel('', parent) # just use the two functions get_name_to_print and get_unit_to_print istead of 'Value'
        self.setModel(self.model)
        self.tabfunc = TF()
        # Selection of items
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.selection = self.selectionModel()


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
            self.model.update_header(self.tabfunc.return_header_names(path,var))
        else:
            raise ValueError('Argument items contains wrong number of items, should be one or two.')

        # Updates model
        self.model.updateData(data,items)

        # Updates size of column when content is changed
        for i in range(self.model.columnCount()):
            self.resizeColumnToContents(i)


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
            data = self.tabfunc.append_table(path, var)
            self.model.update_header(self.tabfunc.append_header(path,var))
        else:
            raise ValueError('Argument items contains wrong number of items, should be one or two.')

        # Updates model
        self.model.appendData(data,items)

        # Updates size of column when content is changed
        for i in range(self.model.columnCount()):
            self.resizeColumnToContents(i)

    def clearTable(self):
        self.model.clearTable()
