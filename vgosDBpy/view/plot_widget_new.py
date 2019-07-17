from PySide2.QtWidgets import QTabWidget, QGridLayout, QWidget, QCheckBox, QButtonGroup, QRadioButton, QVBoxLayout
from PySide2 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector
from matplotlib.lines import Line2D

from vgosDBpy.data.plotFunction import plot_generall #plotVariable, plotVariable2yAxis
from vgosDBpy.editing.select_data import getData
from vgosDBpy.model.data_axis import DataAxis

import pandas as pd
from scipy.signal import savgol_filter




class PlotFigure(FigureCanvas):
    '''
    View of matplotlib plots
    Can display several axes
    '''
    def __init__(self, figure = Figure(tight_layout = True), parent = None):
        '''
        Constructor

        figure [matplotlib.Figure]
        parent [QWidget]
        '''

        # Save figure and create Qt instance that displays plots from matplotlib
        self.figure = figure
        super(PlotFigure, self).__init__(self.figure)

        self.timeInt = 0
        # To be initiated
        self.ax = []
        self.draw()

        self.paths = []
        self.vars = []

    def updatePlot(self):
        self.draw()

    def addAxis(self, data_axis):
        '''
        Adds axis to the figure

        data_axis [DataAxis]
        '''
        axis = self.figure.add_axes(data_axis.getAxis())
        self.ax.append(data_axis)

    def removeAxis(self, data_axis):
        '''
        Removes axis from the figure

        data_axis [DataAxis]
        '''
        axis = data_axis.getAxis()
        self.ax.remove(axis)
        self.figure.delaxes(axis)

    def getAxis(self):
        '''
        Returns list of axes that belongs to the figure [list of matplotlib.Axis]
        '''
        return self.ax

    def getFigure(self):
        '''
        Returns figure [matplotlib.Figure]
        '''
        return self.figure

    def updateFigure(self, items):
        '''
        Updates figure with the given items

        items [list of QStandardItem]
        '''
        # Discards the old graph
        self.figure.clear()
        self.paths = []
        self.vars = []
        for itm in items:
            self.paths.append(itm.getPath())
            self.vars.append(itm.labels)
        axis, data = plot_generall(self.paths,self.vars, self.figure, self.timeInt)

        """
        if len(items) == 1:
            #axis, data = plotVariable(items[0].getPath(), items[0].labels, self.figure)
            axis, data = plot_generall(paths, vars, self.figure, 1)
        elif len(items) == 2:
            axis = plotVariable2yAxis(items[0].getPath(), items[0].labels, items[1].getPath(), items[1].labels, self.figure)
            ax1, ax2, d1, d2 = plot_generall(paths, vars, self.figure, 1)
        else:
            raise ValueError('Argument items contains wrong number of items, should be one or two.')
        """
        for i in range(0,len(axis) ) :
            self.ax.append( DataAxis( axis[i], data[i] ) )
        # Refresh canvas
        self.updatePlot()

    def updateTime(self):
        self.figure.clear()
        axis, data = plot_generall(self.paths, self.vars, self.figure, self.timeInt)
        # Add new axis
        for i in range(0,len(axis) ) :
            self.ax.append( DataAxis( axis[i], data[i] ) )
        # Refresh canvas
        self.updatePlot()


    def saveCanvas(self, file_name):
        '''
        Saves current figure as a pdf

        file_name [str]
        '''
        with PdfPages(file_name) as pdf:
            pdf.savefig(self.figure)


class AxesToolBox(QWidget):
    '''
    A class that controls the appearance of the PlotFigure
    Also includes the interface which controls it
    (view/control)

    Contains one DataAxis which represents the data set that is plotted
    '''
    # Class variables
    marker_size = 1.8 # Controls size of markers in plots


    def __init__(self, parent, canvas, data_axis = None):

        '''
        Constructor

        parent [QWidget]
        canvas [PlotFigure]
        data_axis [DataAxis]
        '''

        super(AxesToolBox, self).__init__(parent)

        # Instance variables
        self.canvas = canvas
        self.selector = None
        self.data_axis = data_axis
        if data_axis == None:
            self.original_lines = None
        else:
            self.original_lines = self.data_axis.getAxis().get_lines()


        self.edited_curve = None # Saves the curve for edited data (where marked data is hidden)
        self.smooth_curve = None # Saves the smooth curve
        self.marked_data_curve = None # Saves marked data points in pot

        # Buttons and their respective functions
        appearance_widget = QWidget(self)
        self.check_line = QCheckBox('Show line')
        self.check_marker = QCheckBox('Show markers')
        self.check_smooth_curve = QCheckBox('Show smooth curve')
        self.timeDefault = QCheckBox('Plot against time')

        self.highlight_marked = QRadioButton("Highlight marked data", self)
        self.hide_marked = QRadioButton("Hide marked data", self)

        appearance_layout = QGridLayout()
        appearance_layout.addWidget(self.check_line, 0, 0)
        appearance_layout.addWidget(self.check_marker, 1, 0)
        appearance_layout.addWidget(self.check_smooth_curve, 2, 0)
        appearance_layout.addWidget(self.timeDefault, 3, 0)

        appearance_layout.addWidget(self.highlight_marked, 0, 1)
        appearance_layout.addWidget(self.hide_marked, 1, 1)
        appearance_widget.setLayout(appearance_layout)

        # Listeners
        self.check_line.setCheckState(QtCore.Qt.Checked)
        self.check_line.stateChanged.connect(self._showLine)

        self.check_marker.setCheckState(QtCore.Qt.Unchecked)
        self.check_marker.stateChanged.connect(self._showMarkers)

        self.check_smooth_curve.setCheckState(QtCore.Qt.Unchecked)
        self.check_smooth_curve.stateChanged.connect(self._showSmoothCurve)

        self.timeDefault.setCheckState(QtCore.Qt.Checked)
        self.timeDefault.stateChanged.connect(self._Deafult_on_time)

        self.highlight_marked.setChecked(True)
        self.highlight_marked.toggled.connect(self.highlightMarkedData)
        self.hide_marked.toggled.connect(self.highlightMarkedData)

    def updateAxis(self, data_axis):
        '''
        Updates the instance with a new axis

        data_axis [DataAxis]
        '''
        self.data_axis = data_axis
        self.original_lines = data_axis.getAxis().get_lines()
        self.updateSelector(self.data_axis)
        self._showLine()
        self._showMarkers()
        for line in self.data_axis.getAxis().get_lines():
            line.set_markersize(AxesToolBox.marker_size)

    def updateSelector(self, data_axis):
        '''
        Updates the selector of the axes with a new selector

        data_axis [DataAxis]
        '''
        self.selector = RectangleSelector(data_axis.getAxis(), self._selector_callback, drawtype='box')

    def _selector_callback(self, eclick, erelease):
        '''
        Called by RectangleSelector
        '''
        #eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        print(getData(x1, x2, y1, y2, self.data_axis.getData()))
        self.data_axis.updateMarkedData(getData(x1, x2, y1, y2, self.data_axis.getData()))

        self.highlightMarkedData()

    def _showLine(self, show_line = True):
        '''
        Method that displays/hide the line in the plot
        '''
        for line in self.original_lines:
            if self.check_line.isChecked() and show_line:
                line.set_linestyle('-')
            else:
                line.set_linestyle('None')

        self.canvas.updatePlot()

    def _showMarkers(self):
        '''
        Method that displays/hide the markers in the data
        '''
        for line in self.original_lines:
            if self.check_marker.isChecked():
                line.set_marker('o')
            else:
                line.set_marker('None')

        self.canvas.updatePlot()


    def _showSmoothCurve(self):
        '''
        Method that displays/hide the a smooth curve fit in the data
        '''

        if self.check_smooth_curve.isChecked():
            data = self.data_axis.getData()
            line = createLine2D(createSmoothCurve(data, window_size = int(len(data)/4)))
            self.smooth_curve = self.data_axis.addLine(line)

        else:
            self.smooth_curve.remove()


        self.canvas.updatePlot()

    def _Deafult_on_time(self):
        if self.timeDefault.isChecked():
            self.canvas.timeInt =1
        else:
            self.canvas.timeInt = 0
        # if there exist a plot update it
        if len(self.canvas.paths) > 0 :
            self.canvas.updateTime()

    def highlightMarkedData(self):
        '''
        Method that highlight the marked data or temporarily removes it from the plot
        '''

        # Removes previous curves if needed
        if self.marked_data_curve != None:
            if self.marked_data_curve.axes != None:
                self.marked_data_curve.remove()
        if self.edited_curve != None:
            if self.edited_curve.axes != None:
                self.edited_curve.remove()

        # Adds the ordinary lines if needed
        for line in self.original_lines:
            if line.axes == None:
                self.data_axis.addLine(line)

        # Button press
        if self.highlight_marked.isChecked():

            # Retrieve marked data
            self._showLine()
            index = []
            value = []
            for data in self.data_axis.getMarkedData():
                index.append(data[0])
                value.append(data[1])

            line = createLine2D(pd.Series(value, index = index))
            line.set_marker('s')
            line.set_linestyle('None')
            self.marked_data_curve = self.data_axis.addLine(line)

        else:
            self.plotEditedData()

        self.canvas.updatePlot()

    def plotEditedData(self):
        '''
        Temporarily removes marked data and plots only the  non-selected data

        '''
        self._showLine(show_line = False)
        self.data_axis.resetEditedData()
        self.data_axis.removeMarkedData()
        line = createLine2D(self.data_axis.getEditedData())
        line.set_color('r')
        self.edited_curve = self.data_axis.addLine(line)

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

'''
class PlotToolBox(QTabWidget):

    def __init__(self, parent = None, canvas = PlotFigure()):
        super(PlotToolBox, self).__init__(parent)
        self.parent = parent
        self.canvas = canvas
        self.current_plots = []
        ## Appearance widget

    def addAxisTools(self, data_axis):
        appearance_widget = AxesToolBox(self.parent, self.canvas, data_axis)
        self.addTab(appearance_widget, 'Appearance')

        self.current_plots.append(data_axis)


        ## Editing widget
        #button2 = QPushButton('Test')
        #self.addTab(button2, 'Editing')

        #self.show()
'''

def createLine2D(series, marker = None):
    '''
    Returns an artist object [Line2D] which represents the series,
    used for adding new line to an existing axis in matplotlib

    series [pd.Dataframe] is a time series
    '''
    return Line2D(series.index, series[:], marker = marker)

def createSmoothCurve(series, window_size = 10, pol_order = 8):
    '''
    Return a time series [pd.Datafram] that is more smooth

    series [pd.Dataframe] is a time series
    window_size [int] is the window size of the applied filter
    pol_order [int] is the highest order of the polynome fitted to the data,
    has to be lower than the window size and uneven
    '''
    if window_size%2 == 0:
        window_size += 1

    while pol_order > window_size:
        pol_order -= 1
        if pol_order == 1:
            raise ValueError('Polynome order is too small, adjust window size')

    data = savgol_filter(series, window_size, pol_order)
    return pd.Series(data, index = series.index)