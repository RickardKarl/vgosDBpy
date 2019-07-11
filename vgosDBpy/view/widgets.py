
from PySide2.QtWidgets import QTreeView, QTableView, QAbstractItemView

from vgosDBpy.model.standardtree import TreeModel
from vgosDBpy.model.table import TableModel
from vgosDBpy.data.plotTable import tableFunction, tableFunction2data, tableFunctionGeneral, return_header_names



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


class DataTable(QTableView):
    '''
    Displays data from TableModel which has values from a variable together with timestamp

    parent [QWidget] is the parent widget
    '''

    def __init__(self, parent = None):
        super(DataTable, self).__init__(parent)

        # Setup model
        self.model = TableModel(['Index', 'Value'], parent) # just use the two functions get_name_to_print and get_unit_to_print istead of 'Value'
        self.setModel(self.model)

    def updateData(self, items):
        '''
        Updates the data in the table

        items [list of QNodeItems] contains the nodes which points to the netCDF variables
        that should be displayed
        '''
        if len(items) > 0 :
            path = []
            var = []
            for itm in items:
                path.append(itm.getPath())
                var.append(itm.labels)
            data= tableFunctionGeneral(path, var)
            self.model.update_header(return_header_names(var))
            """
            # Retrieve values for variables
            if len(items) == 1:
                path = []
                var = []
                path.append( items[0].getPath() )
                var.append( items[0].labels )
                #data = tableFunction(path, var)
                data = tableFunctionGeneral(path,var)


            elif len(items) == 2:
                #path = []
                #var= []
                #for itm in items:
                #    path.append(itm.getPath())
                #    var.append(itm.labels)
                path1 = items[0].getPath()
                path2 = items[1].getPath()
                var1 = items[0].labels
                var2 = items[1].labels
                data = tableFunction2data(path1, var1, path2, var2)
                #data =  tableFunctionGeneral(path,var)
            """
        else:
            raise ValueError('Argument items contains wrong number of items, should be one or two.')

        # Updates model
        self.model.updateData(data, items)

        # Updates size of column when content is changed
        for i in range(self.model.columnCount()):
            self.resizeColumnToContents(i)
