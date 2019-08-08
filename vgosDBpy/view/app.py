from PySide2.QtWidgets import QApplication, QTreeView, QAbstractItemView, QWidget, QTextEdit, QPushButton, QVBoxLayout, QGridLayout, QTabWidget
from PySide2 import QtCore

from pandas.plotting import register_matplotlib_converters

from vgosDBpy.view.widgets import QWrapper, VariableTable, DataTable
from vgosDBpy.data.readNetCDF import get_netCDF_vars_info
from vgosDBpy.view.plot_widget_new import AxesToolBox, PlotWidget
from vgosDBpy.editing.track_edits import EditTracking
from vgosDBpy.wrapper.tree import Wrapper


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

        ######### Matplotlib time format converter registers
        register_matplotlib_converters()

        ########### Creating widgets
        # Wrapperview
        self.treeview = QWrapper(wrapper_path, self)

        ######### Keep track of changes
        self.track_edits = EditTracking(self.treeview.getWrapper())

        # Text
        self.info_text = QTextEdit(self)
        self.info_text.setReadOnly(True)

        # Tableview
        self.data_table = DataTable(self)
        self.var_table = VariableTable(self)

        # Matplotlib widget and toolbox
        self.plot_widget = PlotWidget(self)
        self.plot_toolbox = AxesToolBox(self, self.plot_widget.plot_canvas, self.data_table)

        # Tab-widget for plot and datatable
        self.tab_widget_plt = QTabWidget(self)
        self.tab_widget_plt.addTab(self.plot_widget,'& Plot')
        self.tab_widget_plt.addTab(self.data_table, '& Table')

        self.tab_widget_varinfo = QTabWidget(self)
        self.tab_widget_varinfo.addTab(self.var_table, '& Variable')
        self.tab_widget_varinfo.addTab(self.info_text, '& Info')

        ################## Buttons ########################
        # Plot and display table
        self.button_plot = QPushButton('& Plot',self)
        self.button_table = QPushButton('& Table',self)
        self.button_append_table = QPushButton('& Add to table' )
        self.button_append_plot = QPushButton( '& Add to plot')
        self.button_clear = QPushButton('& Clear')

        # Button event
        self.button_plot.clicked.connect(self._plotbutton)
        self.button_table.clicked.connect(self._tablebutton)
        self.button_append_table.clicked.connect(self._append_tablebutton)
        self.button_append_plot.clicked.connect(self._append_plotbutton)
        self.button_clear.clicked.connect(self._clear)

        # Button layout
        self.button_widget = QWidget(self)
        button_layout = QGridLayout()
        button_layout.addWidget(self.button_plot, 0, 0)
        button_layout.addWidget(self.button_table, 0, 1)
        button_layout.addWidget(self.button_append_plot, 1, 0)
        button_layout.addWidget(self.button_append_table, 1, 1)
        button_layout.addWidget(self.button_clear, 2, 0)
        self.button_widget.setLayout(button_layout)

        # Listeners
        self.treeview.selection.selectionChanged.connect(self._showItemInfo)

        ################## App layout ##################
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
        #return widget.selectedIndexes()

    ### Methods connected to buttons ###

    def _showItemInfo(self):
        '''
        Updates information in the app, selected items are read from the wrapper directory
        '''
        index = self._getSelected(self.treeview)
        if not index == []:
            item = self.treeview.getModel().itemFromIndex(index[0])
            if item.isNetCDF():
                text = get_netCDF_vars_info(item.getPath())
                self.info_text.setPlainText(str(text))
                self.var_table.updateVariables(item)

            elif item.isHistFile():
                text = Wrapper.getHistory(item.getPath())
                self.info_text.setPlainText(text)

    def _plotbutton(self):
        '''
        Method for plotting data from variables
        '''
        self._clear()
        index = self._getSelected(self.var_table)
        if not index == []:
            items = []
            for i in range(len(index)):
                items.append(self.var_table.getModel().itemFromIndex(index[i]))

            self.plot_widget.plot_canvas.updateFigure(items)

            data_axis = self.plot_widget.getDataAxis()
            self.plot_toolbox.updateDataAxis(data_axis)
            self.data_table.updateFromDataAxis(data_axis)

    def _append_plotbutton(self):
        index = self._getSelected(self.var_table)
        if not index == []:
            item = self.var_table.getModel().itemFromIndex(index[-1])
            self.plot_widget.plot_canvas.append_plot(item)

        data_axis = self.plot_widget.getDataAxis()
        self.plot_toolbox.updateDataAxis(data_axis)
        self.data_table.updateFromDataAxis(data_axis)

    def _tablebutton(self):
        '''
        Method for displaying variables in table
        '''
        self._clear()
        index = self._getSelected(self.var_table)
        if not index == []:
            items = []
            for i in range (len(index)):
                items.append(self.var_table.getModel().itemFromIndex(index[i]))
            if not items == [] :
                self.data_table.updateData(items)
                self.plot_toolbox.updateDataAxis(self.data_table.getModel().getAllDataAxis())

    def _append_tablebutton(self):
        index= self._getSelected(self.var_table)
        if not index  == [] :
            items = []
            for i in range (len(index)):
                items.append(self.var_table.getModel().itemFromIndex(index[i]))
        self.data_table.appendData(items)
        self.plot_toolbox.updateDataAxis(self.data_table.getModel().getAllDataAxis())

    def _clear(self):
        self.plot_widget.plot_canvas.clearFigure()
        self.data_table.resetModel()
