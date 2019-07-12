from PySide2.QtWidgets import QTabWidget, QGridLayout, QWidget, QCheckBox, QButtonGroup, QRadioButton
from PySide2 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector
from matplotlib.lines import Line2D

from vgosDBpy.data.plotFunction import plotVariable, plotVariable2yAxis, plot_generall
from vgosDBpy.editing.select_data import getData

import pandas as pd
from scipy.signal import savgol_filter

class PlotFigure(FigureCanvas):
    '''
    CAN NOT HANDLE SEVERAL AXES AT THE SAME TIME CURRENTLY
    '''
    def __init__(self, figure = Figure(tight_layout = True), parent = None):

        # Save figure and create Qt instance that displays plots from matplotlib
        self.figure = figure
        super(PlotFigure, self).__init__(self.figure)

        # To be initiated
        self.ax = None
        self.data = None
        self.draw()

    def updatePlot(self):
        # Set selector
        self.draw()

    def getAxis(self):
        return self.ax

    def getArtist(self):
        return self.ax.get_lines()

    def redrawData(self):
        self.ax.cla()
        self.ax.plot(self.data)

    def updateFigure(self, items):
        # Discards the old graph
        self.figure.clear()

        paths = []
        vars = []
        state = get_time_default()
        for itm in items:
            paths.append(itm.getPath())
            vars.append(itm.labels)
        self.ax, self.data = plot_generall(paths, vars,self.figure , 0)
        """
        # Add new axis
        if len(items) == 1:
            self.ax, self.data = plotVariable(items[0].getPath(), items[0].labels, self.figure)

        elif len(items) == 2:
            self.ax = plotVariable2yAxis(items[0].getPath(), items[0].labels, items[1].getPath(), items[1].labels, self.figure)

        else:
            raise ValueError('Argument items contains wrong number of items, should be one or two.')
        """
        # Refresh canvas
        self.updatePlot()


class AxesToolBox(QWidget):
    def __init__(self, parent, canvas):
        super(AxesToolBox, self).__init__(parent)
        # Instance variables
        self.canvas = canvas
        self.ax = None
        self.lines = None

        self.smooth_curve = None # Saves the smooth curve

        self.marked_data = [] # Used to save the marked data
        self.marked_data_curve = None

        appearance_widget = QWidget(self)
        self.check_line = QCheckBox('Show line')
        self.check_marker = QCheckBox('Show markers')
        self.check_smooth_curve = QCheckBox('Show smooth curve')

        #self.marked_data_buttons = QButtonGroup(self)
        self.highlight_marked = QRadioButton("Highlight marked data", self)
        self.hide_marked = QRadioButton("Hide marked data", self)

        appearance_layout = QGridLayout()
        appearance_layout.addWidget(self.check_line, 0, 0)
        appearance_layout.addWidget(self.check_marker, 1, 0)
        appearance_layout.addWidget(self.check_smooth_curve, 2, 0)

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

        self.highlight_marked.setChecked(True)
        self.highlight_marked.toggled.connect(self.highlightMarkedData)
        self.hide_marked.toggled.connect(self.highlightMarkedData)


    def updateToolBox(self, ax):
        self.selector = RectangleSelector(ax, self.selector_callback, drawtype='box')
        self.ax = ax
        self.lines = ax.get_lines()

    def selector_callback(self, eclick, erelease):
        #'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

        self.updateMarkedData(getData(x1, x2, y1, y2, self.canvas.data))

    def updateMarkedData(self, data):
        for point in data.iteritems():
            if point in self.marked_data:
                self.marked_data.remove(point)
            else:
                self.marked_data.append(point)

        self.highlightMarkedData()

    def _showLine(self):
        for plot in self.lines:
            if self.check_line.isChecked():
                plot.set_linestyle('-')
            else:
                plot.set_linestyle('None')
        self.canvas.updatePlot()

    def _showMarkers(self):
        for plot in self.lines:
            if self.check_marker.isChecked():
                plot.set_marker('o')
            else:
                plot.set_marker('None')

        self.canvas.updatePlot()

    def _showSmoothCurve(self):

        if self.check_smooth_curve.isChecked():

            line = createLine2D(createSmoothCurve(self.canvas.data, window_size = int(len(self.canvas.data)/4)))
            self.smooth_curve = self.ax.add_line(line)

        else:
            self.smooth_curve.remove()


        self.canvas.updatePlot()

    def highlightMarkedData(self):

        index = []
        value = []
        for data in self.marked_data:
            index.append(data[0])
            value.append(data[1])

        if self.marked_data_curve != None:
            self.marked_data_curve.remove()
        line = createLine2D(pd.Series(value, index = index))
        line.set_marker('s')
        line.set_linestyle('None')
        self.marked_data_curve = self.ax.add_line(line)
        line.set_visible(self.highlight_marked.isChecked())

        self.canvas.updatePlot()





class PlotToolBox(QTabWidget):

    def __init__(self, parent, canvas):
        super(PlotToolBox, self).__init__(parent)

        ## Appearance widget
        appearance_widget = AxesToolBox(self, canvas)
        self.addTab(appearance_widget, 'Appearance')


        ## Editing widget
        button2 = QPushButton('Test')
        self.addTab(button2, 'Editing')

        self.show()


def createLine2D(series, marker = None):
    '''
    Returns an artist object [Line2D] which represents the series,
    used for adding new line to an existing axis in matplotlib

    series [pd.Dataframe] is a time series
    '''
    return Line2D(series.index, series[:], marker = marker)

def createSmoothCurve(series, window_size = 10, pol_order = 3):
    '''
    Return a time series [pd.Datafram] that is more smooth

    series [pd.Dataframe] is a time series
    window_size [int] is the window size of the applied filter
    pol_order [int] is the highest order of the polynome fitted to the data,
    has to be lower than the window size and uneven
    '''
    if window_size%2 == 0:
        window_size += 1
    data = savgol_filter(series, window_size, pol_order)
    return pd.Series(data, index = series.index)
