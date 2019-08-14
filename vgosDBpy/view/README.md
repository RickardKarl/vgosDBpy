# view (Qt-dependent)
The widgets used by Qt GUI.

## vgosDBpyGUI.py
Main window of the GUI, will call all the other widgets.

Controls layout and several buttons.
Includes methods connected to each button.

## AxesToolBox.py

###### AxesToolBox

Widget that contains buttons (including connected methods) that control the appearance of the
plot.

Controls the data flow between the plot widgets and data table widgets,
for plot/table-mirroring.

Utilises *DataAxis* class to keep track of each displayed variable.

There is an instance variable *current_axis* that keeps track of a main DataAxis that is displayed.
This is not really necessary, the plan was to implement a feature to switch between different main
DataAxis so that you could select data from them separately in the plot. However, a lot of code exist
to implement that feature but there was not enough time to make it happen.

## plot_widgets.py

###### PlotFigure

A Qt-widget that integrates matplotlib.

Contains a figure that keep track of *DataAxis* and displays them.


###### PlotWidget

A parent QWidget that contains *PlotFigure* and a navigation toolbar that is integrated with matplotlib.

Makes sure that they are connected and sit together in the interface.

## plotlines.py

Methods that return *matplotlib.Line2D* to plot on *matplotlib.Axis*, given some data.

Current options are: ordinary line, smoothened line or marked data given a data set.


## widgets.py

###### QWrapper (Inherits from QTreeView)

Visual representation of the wrapper as a directory structure
Reads in *TreeModel*.


###### VariableTable (Inherits from QTableView)

Table widget that display the variable content from a netCDF file in a table.


###### DataTable

Table widget that display the data content from a netCDF variable in a table.
