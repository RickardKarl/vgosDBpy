##  combineYMDMS.py
This file contains functions that finds time paths to the TimeUTC.nc file stored in the same directory as a given netCDF file if there is any. It also contains function to connect the YMDHM-data with the seconds.

## getName.py
This file contains function so retrieve the full name of variables in netCDF files and their Units.

## PathParser.py

###### PathParser
This class contains methods to parse a path and retrieve information from the path as well as storing the information

## plotFuncion.py
This class retrieves, sorts and keep track of what to plot and how to plot it.

###### Axisitem
This class holds the information that will be added to the axis in the plot. It can also return the information.
Its purpose is to work as a help class to Plotfunction_class by storing and returning data.

###### Plotfunction_class
This class handles the plotting of data without visulasation which is done in the view. It retrieves data_arrays from netCDF files and connects that data and suitable labels to axis items which are connected to a plot Figure.

## plotTable.py
This file have the purpose of structuring the data from NetCDF files which should we shown in a table in a nice way so it can be used by the rest of the program.

###### tableFunction  
retrieves and stores data that should be shown in a table.It creates and returns a directory that holds the columns-names as keys and the columns-data as values.

## readNetCDF.py
This file holds all the function that collects data from netCDF files, both variables, variables' dtype, dimension, length and data. All interaction with netCDF files is done here.


## tableToASCII.py
Contains methods that export a Qt-table to ASCII format and write it to a .txt file.
