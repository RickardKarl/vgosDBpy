from PySide2.QtWidgets import QTabWidget, QGridLayout, QWidget, QCheckBox, QButtonGroup, QRadioButton
from PySide2 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
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

        # Save figure and create Qt instance that displays plots from matplotlib
        self.figure = figure
        super(PlotFigure, self).__init__(self.figure)

        # To be initiated
        self.ax = []
        self.draw()

    def updatePlot(self):
        self.draw()

    def addAxis(self, data_axis):
        axis = self.figure.add_axes(data_axis.getAxis())
        self.ax.append(data_axis)

    def removeAxis(self, data_axis):
        axis = data_axis.getAxis()
        self.ax.remove(axis)
        self.figure.delaxes(axis)

    def getAxis(self):
        return self.ax

    def getFigure(self):
        return self.figure

    def updateFigure(self, items):
        # Discards the old graph
        self.figure.clear()

        # Retrieves new graph from items
        paths =[]
        vars = []
        for itm in items:
            paths.append(itm.getPath())
            vars.append(itm.labels)
        axis, data = plot_generall(paths, vars, self.figure, 1)
        for i in range(len(axis)):
            self.addAxis(DataAxis(axis[i], data[i]))
        # Refresh canvas
        self.updatePlot()


    def saveCanvas(self, file_name):
        with PdfPages(file_name) as pdf:
            pdf.savefig(self.figure)


class AxesToolBox(QWidget):
    def __init__(self, parent, canvas, data_axis = None):

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

        appearance_widget = QWidget(self)
        self.check_line = QCheckBox('Show line')
        self.check_marker = QCheckBox('Show markers')
        self.check_smooth_curve = QCheckBox('Show smooth curve')

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

    def updateAxis(self, data_axis):
        self.data_axis = data_axis
        self.original_lines = data_axis.getAxis().get_lines()
        self.updateSelector(self.data_axis)
        self._showLine()
        self._showMarkers()

    def updateSelector(self, data_axis):
        self.selector = RectangleSelector(data_axis.getAxis(), self.selector_callback, drawtype='box')

    def selector_callback(self, eclick, erelease):
        #'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        print(getData(x1, x2, y1, y2, self.data_axis.getData()))
        self.data_axis.updateMarkedData(getData(x1, x2, y1, y2, self.data_axis.getData()))

        self.highlightMarkedData()

    def _showLine(self, show_line = True):
        for plot in self.original_lines:
            if self.check_line.isChecked() and show_line:
                plot.set_linestyle('-')
            else:
                plot.set_linestyle('None')

        self.canvas.updatePlot()

    def _showMarkers(self):
        for plot in self.original_lines:
            if self.check_marker.isChecked():
                plot.set_marker('o')
            else:
                plot.set_marker('None')

        self.canvas.updatePlot()


    def _showSmoothCurve(self):

        if self.check_smooth_curve.isChecked():
            data = self.data_axis.getData()
            line = createLine2D(createSmoothCurve(data, window_size = int(len(data)/4)))
            self.smooth_curve = self.data_axis.addLine(line)

        else:
            self.smooth_curve.remove()


        self.canvas.updatePlot()
    '''
    def highlightMarkedData_old(self):

        index = []
        value = []
        for data in self.data_axis.getMarkedData():
            index.append(data[0])
            value.append(data[1])

        if self.marked_data_curve != None:
            self.marked_data_curve.remove()

        line = createLine2D(pd.Series(value, index = index))
        line.set_marker('s')
        line.set_linestyle('None')
        self.marked_data_curve = self.data_axis.addLine(line)
        line.set_visible(self.highlight_marked.isChecked())

        self.canvas.updatePlot()
    '''
    def highlightMarkedData(self):
        if self.marked_data_curve != None:
            if self.marked_data_curve.axes != None:
                self.marked_data_curve.remove()
        if self.edited_curve != None:
            if self.edited_curve.axes != None:
                self.edited_curve.remove()
        for line in self.original_lines:
            if line.axes == None:
                print(1)
                self.data_axis.addLine(line)

        index = []
        value = []
        if self.highlight_marked.isChecked():
            self._showLine()
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
        self._showLine(show_line = False)
        self.data_axis.resetEditedData()
        self.data_axis.removeMarkedData()
        line = createLine2D(self.data_axis.getEditedData())
        line.set_color('r')
        self.edited_curve = self.data_axis.addLine(line)




class PlotToolBox(QTabWidget):
    pass
'''
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
