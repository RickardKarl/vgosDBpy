
from PySide2.QtWidgets import QTreeView, QTableView, QAbstractItemView, QTextEdit, QPushButton, QDialog, QVBoxLayout
from vgosDBpy.model.standardtree import TreeModel
from vgosDBpy.model.table import TableModel
from vgosDBpy.data.plotFunction import plotVariable, plotVariable2yAxis
from vgosDBpy.editing.select_data import getData

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector

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



class PlotFigure(FigureCanvas):

    def __init__(self, figure = Figure(tight_layout = True), parent = None):
        self.figure = figure

        super(PlotFigure, self).__init__(self.figure)


        #self.figure.canvas.mpl_connect('pick_event', self.selector)
        # To be initiated
        self.ax = None
        self.selector = None
        self.data = None

        self.figure.canvas.mpl_connect('button_release_event', self.selection_event)

        self.draw()

    def selection_event(self, event):
        print(self.selector, 'printed by selection_event')

    def selector_callback(self, eclick, erelease):
        #'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

        getData(x1, x2, y1, y2, self.data)




    def updatePlot(self):
        # Set picker tolerance
        if type(self.ax) == 'tuple':
            for a in self.ax:
                a.set_picker(5)
        else:
            self.ax.set_picker(5)

        # Set selector
        self.selector = RectangleSelector(self.ax, self.selector_callback, drawtype='box')

    def updateFigure(self, items):
        # Discards the old graph
        self.figure.clear()

        # Add new axis
        if len(items) == 1:
            self.ax, self.data = plotVariable(items[0].getPath(), items[0].labels, self.figure)

        elif len(items) == 2:
            self.ax = plotVariable2yAxis(items[0].getPath(), items[0].labels, items[1].getPath(), items[1].labels, self.figure)

        else:
            raise ValueError('Argument items contains wrong number of items, should be one or two.')

        # refresh canvas
        self.updatePlot()
        self.draw()
