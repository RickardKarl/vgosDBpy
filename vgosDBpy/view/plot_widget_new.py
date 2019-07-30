from PySide2.QtWidgets import QTabWidget, QWidget, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure

from vgosDBpy.data.plotFunction import plot_generall, is_multdim_var
from vgosDBpy.model.data_axis import DataAxis
from vgosDBpy.view.plotlines import createLine2D, createSmoothCurve
from vgosDBpy.data.readNetCDF import not_S1
from vgosDBpy.view.AxesToolBox import AxesToolBox

class PlotFigure(FigureCanvas):
    '''
    View of matplotlib plots
    Can display several axes
    '''
    def __init__(self, figure = Figure(tight_layout = True), parent = None):

        '''
        Constructor:
        figure [matplotlib.Figure]
        parent [QWidget]
        '''

        # Save figure and create Qt instance that displays plots from matplotlib
        self.figure = figure
        super(PlotFigure, self).__init__(self.figure)

        self.timeInt = 1
        # To be initiated
        self._ax = []
        self.draw()

        self.paths = []
        self.vars = []
        self.items = []

        self.Mult_item_added = False

    def updatePlot(self):
        self.draw()

    def addAxis(self, data_axis):
        '''
        Adds axis to the figure

        data_axis [DataAxis]
        '''
        axis = self.figure.add_axes(data_axis.getAxis())
        self._ax.append(data_axis)

    def removeAxis(self, data_axis):
        '''
        Removes axis from the figure

        data_axis [DataAxis]
        '''
        axis = data_axis.getAxis()
        self._ax.remove(data_axis)
        self._ax.clear()

    def getDataAxis(self):
        '''
        Returns list of axes that belongs to the figure [list of DataAxis]
        '''
        return self._ax

    def getItems(self):
        '''
        Returns list of items that belongs to the figure [list of QNodeItems]
        '''
        return self.items

    def getFigure(self):
        '''
        Returns figure [matplotlib.Figure]
        '''
        return self.figure

    def updateFigure(self, items, timeUpdated = False):

        '''
        Updates figure with the given items

        items [list of QStandardItem]
        '''

        # Discards the old graph
        self.resetFigure()

        if timeUpdated is False:
            self.paths = []
            self.vars = []
            self.items = []

            for itm in items:
                self.paths.append(itm.getPath())
                self.vars.append(itm.labels)
                self.items.append(itm)

        #for i in range(0,len(self.paths)):
            #print('paths: ' +  self.paths[i])
            #print('vars:' + self.vars[i] )

        if not_S1(self.paths, self.vars):
            axis, data = plot_generall(self.paths, self.vars, self.figure, self.timeInt)
            is_mult = is_multdim_var(self.paths, self.vars)

            if is_mult!= -1 and timeUpdated == False:
                items.append(items[is_mult])

            for i in range(len(axis)):
                self.addAxis(DataAxis(axis[i], data[i], items[i]))

            # Refresh canvas
            self.updatePlot()
        else:
            print('Trying to plot a string')

    def resetFigure(self):
        self.figure.clear()
        for ax in self._ax:
            self.removeAxis(ax)
        self._ax = []

    def updateTime(self):
        self.updateFigure(self.items, timeUpdated = True)
        self.parentWidget().getPlotToolBar().updateDataAxis(self._ax)

    def append_plot(self, item):
        #add new item
        self.paths.append(item.getPath())
        self.vars.append(item.labels)
        self.items.append(item)
        self.resetFigure()
        if not_S1(self.paths,self.vars):
            axis, data = plot_generall(self.paths, self.vars, self.figure, self.timeInt)
            for i in range(len(axis)):
                self.addAxis(DataAxis(axis[i], data[i], self.items[i]))

            # Refresh canvas
            self.updatePlot()
        else:
            print('Trying to plot a string')

    def clearFigure(self):
        self.paths = []
        self.vars = []
        self.items = []
        self.Mult_item_added = False

        self.resetFigure()
        self.updatePlot()

    def saveCanvas(self, file_name):
        '''
        Saves current figure as a pdf

        file_name [str]
        '''
        with PdfPages(file_name) as pdf:
            pdf.savefig(self.figure)


class PlotWidget(QWidget):
    '''
    Widget that brings the PlotFigure together with a navigation toolbar that allows different
    matplotlib features such as zoom and move in plot.
    '''
    def __init__(self, parent = None):
        super(PlotWidget, self).__init__(parent)

        self.plot_canvas = PlotFigure(parent = self)
        self.nav_toolbar = NavigationToolbar(self.plot_canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.nav_toolbar)
        layout.addWidget(self.plot_canvas)
        self.setLayout(layout)

    def getPlotToolBar(self):
        return self.parentWidget().parentWidget().parentWidget().plot_toolbox

    def getDataAxis(self):
        return self.plot_canvas.getDataAxis()

    def getItems(self):
        return self.plot_canvas.getItems()
