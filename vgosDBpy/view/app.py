from PySide2.QtWidgets import QApplication, QTreeView, QAbstractItemView, QWidget, QTextEdit, QPushButton, QVBoxLayout, QGridLayout
from PySide2 import QtCore

from pandas.plotting import register_matplotlib_converters

from vgosDBpy.view.widgets import QWrapper, VariableTable, DataTable
from vgosDBpy.data.readNetCDF import read_netCDF_vars_info #, read_netCDF_dimension_for_var, read_netCDF_variables,
from vgosDBpy.view.plot_widget_new import AxesToolBox, PlotWidget

from vgosDBpy.editing.track_edits import EditTracking

class App(QWidget):
    '''
    Application that is the entire interface for the utilities
    '''

    def __init__(self, wrapper_path, parent = None):
        '''
        Constructor

        wrapper_path [string] is the path to the wrapper file which is to be displayed
        parent [QWidget]
        '''
        super(App,self).__init__(parent)

        ######### Keep track of changes
        self.track_edits = EditTracking(wrapper_path)

        ######### Matplotlib time format converter registers
        register_matplotlib_converters()

        ######### Save wrapper path

        ########### Creating widgets

        # Wrapperview
        self.treeview = QWrapper(wrapper_path, self)

        # Tableview
        self.table = VariableTable(self)
        self.data_table = DataTable(self)

        # Text
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)

        # Buttons
        # Plot and display table
        self.button_plot_table = QPushButton('& Plot + Table ')
        self.button_plot = QPushButton('& Plot',self)
        self.button_table = QPushButton('& Table',self)
        self.button_append_table = QPushButton('& Add to table' )

        # Button event
        self.button_plot_table.clicked.connect(self._plot_table_button)
        self.button_plot.clicked.connect(self._plotbutton)
        self.button_table.clicked.connect(self._tablebutton)
        self.button_append_table.clicked.connect(self._addbutton)

        # Matplotlib widget and toolbox
        self.plot_widget = PlotWidget(self)
        self.plot_toolbox = AxesToolBox(self, self.plot_widget.plot_canvas)


        # Layout
        layout = QGridLayout()
        layout.addWidget(self.treeview, 0, 0)
        layout.addWidget(self.plot_widget, 0, 1)
        layout.addWidget(self.data_table, 0, 2)

        layout.addWidget(self.table, 1, 0)
        layout.addWidget(self.plot_toolbox, 1, 1)
        layout.addWidget(self.text, 1, 2)

        layout.addWidget(self.button_plot_table,3,0)
        layout.addWidget(self.button_plot, 4, 0)
        layout.addWidget(self.button_table, 5, 0)
        layout.addWidget(self.button_append_table, 5,1)

        self.setLayout(layout)

        # Listeners
        self.treeview.selectionModel().selectionChanged.connect(self._showItemInfo)

    ### Getters ###
    def getWrapperModel():
        return self.treeview.getModel()

    def _getSelected(self, widget):
        '''
        Returns selected indices from a view widget (e.g. table or tree view)

        widget [QWidget] that has a selection model, it requires that the widget
        has a instance variable named selection which points to the selection model
        '''
        return widget.selection.selectedIndexes()

    ### Methods connected the interface ###

    def _showItemInfo(self):
        '''
        Updates information in the app, selected items are read from the wrapper directory
        '''
        index = self._getSelected(self.treeview)
        if not index == []:
            item = self.treeview.getModel().itemFromIndex(index[0])
            if item.isNetCDF():
                text = read_netCDF_vars_info(item.getPath())
                self.text.setPlainText(str(text))
                self.table.updateVariables(item)
                #self.data_table.updateData(item)

    def _plot_table_button(self):
        self._plotbutton()
        self._tablebutton()

    def _plotbutton(self):
        '''
        Method for plotting data from variables
        '''
        index = self._getSelected(self.table)
        if not index == []:
            items = []
            for i in range(len(index)):
                items.append(self.table.model.itemFromIndex(index[i]))
            self.plot_widget.plot_canvas.updateFigure(items)

        for data_axis in self.plot_widget.plot_canvas.getAxis():
            self.plot_toolbox.updateAxis(data_axis)

    def _tablebutton(self):
        '''
        Method for displaying variables in table
        '''
        index = self._getSelected(self.table)
        if not index == [] :
            items = []
            for i in range (len(index)):
                items.append(self.table.model.itemFromIndex(index[i]))
            self.data_table.updateData(items)


    def _addbutton(self):
        index= self._getSelected(self.table)
        if not index  == [] :
            items = []
            for i in range (len(index)):
                items.append(self.table.model.itemFromIndex(index[i]))
        self.data_table.appendData(items)
