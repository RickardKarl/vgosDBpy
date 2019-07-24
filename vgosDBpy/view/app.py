from PySide2.QtWidgets import QApplication, QTreeView, QAbstractItemView, QWidget, QTextEdit, QPushButton, QVBoxLayout, QGridLayout, QTabWidget
from PySide2 import QtCore

from pandas.plotting import register_matplotlib_converters

from vgosDBpy.view.widgets import QWrapper, VariableTable, DataTable
from vgosDBpy.data.readNetCDF import read_netCDF_vars_info,read_netCDF_data_info #, read_netCDF_dimension_for_var, read_netCDF_variables,
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

        # Text
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)

        # Buttons
        # Plot and display table
        self.button_plot_table = QPushButton('& Plot + Table ')
        self.button_plot = QPushButton('& Plot',self)
        self.button_table = QPushButton('& Table',self)
        self.button_append_table = QPushButton('& Add to table' )
        self.button_append_plot = QPushButton( '& Add to plot')
        self.button_clear_plot = QPushButton('& Clear plot')
        self.button_clear_table = QPushButton('& Clear table')

        # Button event
        self.button_plot_table.clicked.connect(self._plot_table_button)
        self.button_plot.clicked.connect(self._plotbutton)
        self.button_table.clicked.connect(self._tablebutton)
        self.button_append_table.clicked.connect(self._addbutton)
        self.button_append_plot.clicked.connect(self._append_plotbutton)
        self.button_clear_plot.clicked.connect(self._clear_plot)
        self.button_clear_table.clicked.connect(self._clear_table)

        # Button layout
        self.button_widget = QWidget(self)
        button_layout = QGridLayout()
        button_layout.addWidget(self.button_plot, 0, 0)
        button_layout.addWidget(self.button_table, 0, 1)
        button_layout.addWidget(self.button_append_plot, 1, 0)
        button_layout.addWidget(self.button_append_table, 1, 1)
        button_layout.addWidget(self.button_clear_plot, 2, 0)
        button_layout.addWidget(self.button_clear_table, 2, 1)
        self.button_widget.setLayout(button_layout)

        # Tableview
        self.data_table = DataTable(self)
        self.table = VariableTable(self)


        # Matplotlib widget and toolbox
        self.plot_widget = PlotWidget(self, self.data_table)
        self.plot_toolbox = AxesToolBox(self, self.plot_widget.plot_canvas)


        # Tab-widget for plot and data table
        self.tab_widget_plt = QTabWidget(self)
        self.tab_widget_plt.addTab(self.plot_widget,'& Plot')
        self.tab_widget_plt.addTab(self.data_table, '& Table')

        self.tab_widget_varinfo = QTabWidget(self)
        self.tab_widget_varinfo.addTab(self.table, '& Variable')
        self.tab_widget_varinfo.addTab(self.text, '& Info')

        # App layout
        layout = QGridLayout()
        layout.setColumnStretch(0,1)
        layout.setColumnStretch(1,1)
        layout.setColumnStretch(2,3)

        layout.addWidget(self.treeview, 0, 0)
        layout.addWidget(self.tab_widget_plt, 0, 1, 1, 2)

        layout.addWidget(self.tab_widget_varinfo, 1, 0)
        layout.addWidget(self.button_widget, 1, 1)
        layout.addWidget(self.plot_toolbox, 1, 2)

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

    ### Methods connected to buttons ###

    def _showItemInfo(self):
        '''
        Updates information in the app, selected items are read from the wrapper directory
        '''
        index = self._getSelected(self.treeview)
        if not index == []:
            item = self.treeview.getModel().itemFromIndex(index[0])
            if item.isNetCDF():
                text_info = read_netCDF_vars_info(item.getPath())
                text_data =read_netCDF_data_info(item.getPath())
                text_total = text_info + text_data
                self.text.setPlainText(str(text_total))
                self.table.updateVariables(item)

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

            data_axis = self.plot_widget.getDataAxis()
            for single_axis in data_axis:
                self.plot_toolbox.updateAxis(single_axis)
            self.data_table.updateFromDataAxis(data_axis, items)

    def _append_plotbutton(self):
        index = self._getSelected(self.table)
        if not index == []:
            item = self.table.model.itemFromIndex(index[-1])
            self.plot_widget.plot_canvas.append_plot(item)

        for data_axis in self.plot_widget.getDataAxis():
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

    def _clear_plot(self):
        self.plot_widget.plot_canvas.clearFigure()

    def _clear_table(self):
        self.data_table.clearTable()
