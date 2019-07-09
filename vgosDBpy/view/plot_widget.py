from PySide2.QtWidgets import QTabWidget, QGridLayout, QWidget, QPushButton, QCheckBox

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector

from vgosDBpy.data.plotFunction import plotVariable, plotVariable2yAxis
from vgosDBpy.editing.select_data import getData

class PlotFigure(FigureCanvas):
    '''
    CAN NOT HANDLE SEVERAL AXES AT THE SAME TIME CURRENTLY
    '''
    def __init__(self, figure = Figure(tight_layout = True), parent = None):
        self.figure = figure

        super(PlotFigure, self).__init__(self.figure)

        # To be initiated
        self.ax = None
        self.selector = None
        self.data = None
        self.marked_data = None

        self.figure.canvas.mpl_connect('button_release_event', self.selection_event)
        self.draw()

    def selection_event(self, event):
        pass

    def selector_callback(self, eclick, erelease):
        #'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

        print(getData(x1, x2, y1, y2, self.data))


    def getAxis(self):
        return self.ax

    def getArtist(self):
        return self.ax.get_children()

    def updatePlot(self):
        # Set selector
        self.selector = RectangleSelector(self.ax, self.selector_callback, drawtype='box')

        self.draw()

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

        # Refresh canvas
        self.updatePlot()


class AxesToolBox(QWidget):
    def __init__(self, parent, canvas):
        super(AxesToolBox, self).__init__(parent)
        self.canvas = canvas

        appearance_widget = QWidget(self)
        self.check_line = QCheckBox('Show line')
        b2 = QPushButton('2')
        b3 = QPushButton('3')
        b4 = QPushButton('4')

        appearance_layout = QGridLayout()
        appearance_layout.addWidget(self.check_line, 0, 0)
        appearance_layout.addWidget(b2, 0, 1)
        appearance_layout.addWidget(b3, 1, 0)
        appearance_layout.addWidget(b4, 1, 1)
        appearance_widget.setLayout(appearance_layout)

    def showLine(self):
        ax = self.canvas.getArtist()[0]
        if self.check_line.isChecked():
            ax.set_linestyle('-')
        else:
            ax.set_linestyle('None')

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
