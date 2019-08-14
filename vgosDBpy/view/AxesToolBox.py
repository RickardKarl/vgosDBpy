from PySide2.QtWidgets import QGridLayout, QWidget, QCheckBox, QRadioButton, QPushButton, QMessageBox
from PySide2 import QtCore
from PySide2.QtGui import QMouseEvent
from matplotlib.widgets import RectangleSelector
import pandas as pd

from vgosDBpy.editing.select_data import getData
from vgosDBpy.view.plotlines import createLine2D, createSmoothCurve
from vgosDBpy.data.tableToASCII import convertToAscii, write_ascii_file
from vgosDBpy.model.data_axis import DataAxis
from vgosDBpy.view.popUpWindows import popUpBoxTable, popUpBoxEdit, popUpChooseCurrentAxis, history_information
from vgosDBpy.view.widgets import VariableTable

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
        table_widget [DataTable]
        start_axis [DataAxis] is the axis which should be the current axis from start
        '''

        super(AxesToolBox, self).__init__(parent)

        ##### Instance variables

        # Widgets
        self.canvas = canvas
        self.table_widget = table_widget

        # Track edits
        self.track_edits = self.parentWidget().track_edits

        # Control, appearance and data variables
        self.selector = None
        self.data_axis = canvas.getDataAxis()
        self.current_axis = start_axis

        # Buttons and their respective functions ##################################################
        appearance_widget = QWidget(self)

        self.check_line = QCheckBox('Show line')
        self.check_marker = QCheckBox('Show markers')
        self.check_smooth_curve = QCheckBox('Show smooth curve')
        self.timeDefault = QCheckBox('Display time on X-axis')

        self.clear_marked = QPushButton('Clear all marked data', self)
        self.remove_marked = QPushButton('Remove marked data', self)
        self.restore_marked = QPushButton('Restore original data', self)


        self.saveEdit = QPushButton('Save changes', self)
        self.printTable = QPushButton('Print table', self)

        # Layout ##################################################
        appearance_layout = QGridLayout()

        appearance_layout.addWidget(self.check_line, 0, 0)
        appearance_layout.addWidget(self.check_marker, 1, 0)
        appearance_layout.addWidget(self.check_smooth_curve, 2, 0)
        appearance_layout.addWidget(self.timeDefault, 3, 0)

        appearance_layout.addWidget(self.clear_marked, 0, 1)
        appearance_layout.addWidget(self.remove_marked, 1, 1)
        appearance_layout.addWidget(self.restore_marked, 2, 1)

        appearance_layout.addWidget(self.saveEdit, 0, 2)
        appearance_layout.addWidget(self.printTable, 1, 2)

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

        self.clear_marked.clicked.connect(self._clearMarkedData)
        self.remove_marked.clicked.connect(self._trackEdit)
        self.restore_marked.clicked.connect(self._restoreChanges)

        self.saveEdit.clicked.connect(self._saveEdit)
        self.printTable.clicked.connect(self._printTable)

        ######### Listen to changes of selection in table_widget

        self.table_widget.custom_mouse_release.connect(self._selection_changed_callback_table)
        self.table_widget.getModel().dataChanged_customSignal.connect(self._tableDataChanged)

    ######## Methods for updating the DataAxis of the tool box

    def updateDataAxis(self, data_axis):
        '''
        Updates the tool box with a list of DataAxis

        data_axis [list of DataAxis]
        '''

        if len(data_axis) > 0:
            self.resetToolBox()

            bool = True
            for ax in data_axis:
                if ax not in self.data_axis:
                    self.addSingleDataAxis(ax, make_current_axis = bool)
                    bool = False


    def addSingleDataAxis(self, data_axis, make_current_axis = False):
        '''
        Updates the instance with a new axis

        data_axis [DataAxis]
        make_current_axis [boolean] decides if the new data_axis should become the current axis
        '''
        self.data_axis.append(data_axis)
        if make_current_axis:
            self.setCurrentAxis(data_axis)
        self._updateDisplayedData(update_plot_only = True)
        data_axis.setMarkerSize(AxesToolBox.marker_size)

    def resetToolBox(self):
        '''
        Reset the selector and list of DataAxis belonging to the figure
        '''
        self.selector = None
        self.data_axis = []
        self.canvas.updatePlot()

    def setCurrentAxis(self, data_axis):
        '''
        Sets the given DataAxis as the current axis of the tool box

        data_axis [DataAxis]
        '''
        if data_axis in self.data_axis:
            self.current_axis = data_axis
            self.updateSelector(data_axis)
            self._updateDisplayedData()

        else:
            raise ValueError('Invalid choice of DataAxis, does not exist in figure.', data_axis)


    ############## Selector methods #########

    ###### Used by plot canvas

    def updateSelector(self, data_axis):
        '''
        Updates the selector of the axes with a new selector

        data_axis [DataAxis]
        '''
        if data_axis.axisExists():
            self.selector = RectangleSelector(data_axis.getAxis(), self._selector_callback_plot, drawtype='box')

    def _selector_callback_plot(self, eclick, erelease):
        '''
        Called by RectangleSelector
        '''
        #eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

        marked_data = getData(x1, x2, y1, y2, self.current_axis.getData(), self.canvas.timeInt)

        # Update marked data
        self.current_axis.updateMarkedData(marked_data)

        # Update appearance of plot and table
        self._updateSelectionWidgets()

    ####### Used by data table

    def _selection_changed_callback_table(self):
        '''

        Called when selecting items in DataTable

        '''
        # Get marked data
        for ax in self.data_axis:
            marked_data = self.table_widget.getModel().getDataFromSelected(self.table_widget.selection.selectedIndexes(), ax)
            # Update current axis with the marked data
            if self.canvas.isPlotting():
                ax.updateMarkedData(marked_data)

        # Update appearance of plot and table
        self._updateSelectionWidgets()

    @QtCore.Slot(int)
    def _tableDataChanged(self, int):
        '''
        Called when the data is edited in DataTable

        int is the column index of the edited cell in the table
        '''

        # Check that the column does not contain time
        if not self.table_widget.getModel().isTimeColumn(int):

            # Update table
            self.table_widget.getModel().updateDataAxisfromTable()

            # Track changes
            edited_data_axis = self.table_widget.getModel().getDataAxis(int)
            edited_data = edited_data_axis.getEditedData()
            self.track_edits.addEdit(edited_data_axis.getItem(), edited_data.values)

            # Update plot
            if self.canvas.isPlotting():
                self._updateDisplayedData(update_plot_only = True)


        else:
            # Update table
            self.table_widget.updateFromDataAxis(self.data_axis)


    ############# Used by both plot canvas and data table

    def _updateSelectionWidgets(self):
        '''
        Update the appearance of the widgets with respect of the marked/edited data
        '''

        # Update plot figure with marked data
        for ax in self.data_axis:
            ax.updateLines()
        self.canvas.updatePlot()

        # Update table with marked data
        #self.table_widget.getSignal().disconnect(self._selection_changed_callback_table)
        self.table_widget.updateMarkedRows(self.data_axis)

    def _updateDisplayedData(self, update_plot_only = False):
        '''
        Updates the displayed data

        update_plot_only [boolean] decides whether both plot and table should be updated or only plot
        '''

        if update_plot_only is True:
            self.table_widget.updateFromDataAxis(self.data_axis)

        for ax in self.data_axis:
            ax.updateLines()
        self.canvas.updatePlot()
        self._showLine()
        self._showMarkers()
        self._showSmoothCurve()

        # Update table
        self.table_widget.updateFromDataAxis(self.data_axis)


    ######## Button methods that control appearance

    def _showLine(self):
        '''
        Method that displays/hide the line in the plot
        '''
        self.current_axis.displayMainCurve(self.check_line.isChecked())
        self.canvas.updatePlot()

    def _showMarkers(self):
        '''
        Method that displays/hide the markers in the data
        '''
        self.current_axis.displayMarkers(self.check_marker.isChecked())
        self.canvas.updatePlot()


    def _showSmoothCurve(self):
        '''
        Method that displays/hide a smooth curve fit in the data
        '''
        self.current_axis.displaySmoothCurve(self.check_smooth_curve.isChecked())
        self.canvas.updatePlot()


    def _timeDefault(self):
        '''
        Checks if time should be displayed on the X-axis or not

        Sets an instance variable in the PlotFigure instance
        '''
        if self.timeDefault.isChecked():
            self.canvas.timeInt = 1
        else:
            self.canvas.timeInt = 0


        self.table_widget.resetModel()
        self.canvas.timeChanged()

    #### Methods for editing and saving data

    def _clearMarkedData(self):
        '''
        Clears the marked data
        '''
        if self.current_axis == None:
            pass
        else:
            self.current_axis.clearMarkedData()
            self._updateSelectionWidgets()

    def _trackEdit(self):
        '''
        Remove the marked data and track it as a change
        '''
        edited_data = self.current_axis.getNewEdit()
        self.track_edits.addEdit(self.current_axis.getItem(), edited_data.values)
        self._clearMarkedData()
        self._updateDisplayedData()

    def _restoreChanges(self):
        '''
        Restore changes in the currently displayed data
        '''
        self.current_axis.resetEditedData()
        self.track_edits.removeEdit(self.current_axis.getItem())
        self._clearMarkedData()
        self._updateDisplayedData()


    def _saveEdit(self):
        '''
        Save all of the tracked edits that have been made to data in netCDF
        '''
        # Ask for confirmation by user
        msg = self.track_edits.getTextInfo()
        button_pressed = popUpBoxEdit(msg)

        # If confirmed, generate information in text format and save changes
        if button_pressed == QMessageBox.AcceptRole:
            information = history_information()
            self.track_edits.saveEdit(information)

        # If user wants to reset
        elif button_pressed == QMessageBox.ResetRole:
            self.track_edits.reset()
            for ax in self.data_axis:
                ax.resetEditedData()
            self._updateDisplayedData()


    def _printTable(self):
        '''
        Writes a text file in ASCII format of the currently displayed table
        '''
        # Convert table to a PrettyTable instance
        ptable = convertToAscii(self.table_widget)

        # Generate text in header of the text file
        session_name = self.parentWidget().treeview.getWrapper().session_name
        info = 'Session: ' + session_name

        # Generate file name
        file_name = ''
        for head in ptable.field_names:
            if len(head) > 3:
                head = head[0:3]
            file_name = file_name + '_' + head

        # Generate path
        path = session_name + file_name + '.txt'

        # Confirm save by used
        button_pressed = popUpBoxTable(path)

        # Save file to ASCII if confirmed
        if button_pressed == QMessageBox.AcceptRole:
            write_ascii_file(ptable, info, path)
