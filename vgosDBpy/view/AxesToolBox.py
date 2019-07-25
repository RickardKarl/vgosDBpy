from PySide2.QtWidgets import QGridLayout, QWidget, QCheckBox, QRadioButton, QPushButton
from PySide2 import QtCore
from matplotlib.widgets import RectangleSelector
import pandas as pd

from vgosDBpy.editing.select_data import getData
from vgosDBpy.view.plotlines import createLine2D, createSmoothCurve

class AxesToolBox(QWidget):
    '''
    A class that controls the PlotFigure and DataTable
    Also includes the interface which controls it
    (view/control)

    Contains DataAxis which represents the data set that is plotted/shown in table
    '''
    # Class variables
    marker_size = 2.3 # Controls size of markers in plots


    def __init__(self, parent, canvas, table_widget, start_axis = None):

        '''
        Constructor

        parent [QWidget]
        canvas [PlotFigure]
        data_axis [DataAxis]
        '''

        super(AxesToolBox, self).__init__(parent)

        ##### Instance variables

        # Widgets
        self.canvas = canvas
        self.table_widget = table_widget

        # Control, appearance and data variables
        self.selector = None
        self.data_axis = canvas.getDataAxis()
        self.current_axis = start_axis

        # If current_axis is given
        if self.current_axis == None and not len(self.data_axis) > 0:
            self.original_lines = None
        else:
            self.original_lines = self.current_axis.getAxis().get_lines()


        self.edited_curve = None # Saves the curve for edited data (where marked data is hidden)
        self.smooth_curve = None # Saves the smooth curve
        self.marked_data_curve = None # Saves marked data points in pot

        # Buttons and their respective functions ##################################################
        appearance_widget = QWidget(self)
        self.check_line = QCheckBox('Show line')
        self.check_marker = QCheckBox('Show markers')
        self.check_smooth_curve = QCheckBox('Show smooth curve')
        self.timeDefault = QCheckBox('Plot against time')

        self.highlight_marked = QRadioButton('Highlight marked data', self)
        self.hide_marked = QRadioButton('Hide marked data', self)
        self.clear_marked = QPushButton('Clear marked data', self)

        self.trackEdit = QPushButton('Track edit', self)
        self.saveEdit = QPushButton('Save all changes', self)

        # Layout ##################################################
        appearance_layout = QGridLayout()
        appearance_layout.addWidget(self.check_line, 0, 0)
        appearance_layout.addWidget(self.check_marker, 1, 0)
        appearance_layout.addWidget(self.check_smooth_curve, 2, 0)
        appearance_layout.addWidget(self.timeDefault, 3, 0)

        appearance_layout.addWidget(self.highlight_marked, 0, 1)
        appearance_layout.addWidget(self.hide_marked, 1, 1)
        appearance_layout.addWidget(self.clear_marked, 2, 1)

        appearance_layout.addWidget(self.trackEdit, 0, 3)
        appearance_layout.addWidget(self.saveEdit, 1, 3)
        appearance_widget.setLayout(appearance_layout)

        # Listeners ##################################################
        self.check_line.setCheckState(QtCore.Qt.Checked)
        self.check_line.stateChanged.connect(self._showLine)

        self.check_marker.setCheckState(QtCore.Qt.Unchecked)
        self.check_marker.stateChanged.connect(self._showMarkers)

        self.check_smooth_curve.setCheckState(QtCore.Qt.Unchecked)
        self.check_smooth_curve.stateChanged.connect(self._showSmoothCurve)

        self.timeDefault.setCheckState(QtCore.Qt.Checked)
        self.timeDefault.stateChanged.connect(self._timeDefault)

        self.highlight_marked.setChecked(True)
        self.highlight_marked.toggled.connect(self.highlightMarkedData)
        self.hide_marked.toggled.connect(self.highlightMarkedData)

        self.clear_marked.clicked.connect(self._clearMarkedData)

        self.trackEdit.clicked.connect(self._trackEdit)
        self.saveEdit.clicked.connect(self._saveEdit)


    ######## Methods for updating the DataAxis of the tool box
    def updateDataAxis(self, data_axis):
        '''
        Updates the tool box with a list of DataAxis

        data_axis [list of DataAxis]
        '''
        if len(data_axis) > 0:
            self.current_axis = data_axis[0]

            for ax in data_axis:
                self.addSingleDataAxis(ax)

    def addSingleDataAxis(self, data_axis):
        '''
        Updates the instance with a new axis

        data_axis [list of DataAxis]
        '''
        self.data_axis.append(data_axis)
        if data_axis == self.current_axis:
            self.original_lines = data_axis.getAxis().get_lines()
            self.updateSelector(data_axis)

        self._showLine()
        self._showMarkers()
        for line in data_axis.getAxis().get_lines():
            line.set_markersize(AxesToolBox.marker_size)

    ######## Selector methods

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

        # Update plot with marked data and eventually highlight them

        self.current_axis.updateMarkedData(getData(x1, x2, y1, y2, self.current_axis.getData(), self.canvas.timeInt))
        self.highlightMarkedData()


        table_widget = self.parentWidget().data_table
        table_widget.updateMarkedRows(self.data_axis)

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
        Method that displays/hide a smooth curve fit in the data
        '''

        if self.check_smooth_curve.isChecked():
            data = self.current_axis.getData()
            line = createLine2D(createSmoothCurve(data, window_size = int(len(data)/10)))
            self.smooth_curve = self.current_axis.addLine(line)
        else:
            self.smooth_curve.remove()

        self.canvas.updatePlot()

    def _clearMarkedData(self):
        if self.current_axis == None:
            pass
        else:
            self.current_axis.clearMarkedData()
            self.highlightMarkedData()

    def _trackEdit(self):
        edited_data = self.current_axis.getNewEdit()
        self.parentWidget().track_edits.addEdit(self.current_axis.getItem(), edited_data.values)

    def _saveEdit(self):
        self.parentWidget().track_edits.saveEdit()

    def _timeDefault(self):
        if self.timeDefault.isChecked():
            self.canvas.timeInt = 1
        else:
            self.canvas.timeInt = 0
        # if there exist a plot update it
        #if len(self.canvas.paths) > 0:

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
                self.current_axis.addLine(line)

        # Button press
        if self.highlight_marked.isChecked():

            # Retrieve marked data
            self._showLine()
            index_list = []
            for index in self.current_axis.getMarkedData():
                index_list.append(index)

            marked_series = self.current_axis.getData().take(index_list)
            print(marked_series)
            line = createLine2D(pd.Series(marked_series))
            line.set_marker('s')
            line.set_linestyle('None')
            self.marked_data_curve = self.current_axis.addLine(line)

        else:
            self.plotEditedData()

        #self.table_widget.updateMarkedRows(self.data_axis)
        self.canvas.updatePlot()

    def plotEditedData(self):
        '''
        Temporarily removes marked data and plots only the non-selected data
        '''
        self._showLine(show_line = False)
        line = createLine2D(self.current_axis.getNewEdit())
        line.set_color('r')
        self.edited_curve = self.current_axis.addLine(line)
