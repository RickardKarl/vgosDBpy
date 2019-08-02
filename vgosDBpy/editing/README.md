# editing
Contains classes and methods that keep track of changes in the data as well as methods that can
create new netCDF-files, wrapper-files and history-files with the saved changes.  

## createWrapper.py

Contains methods that create a new wrapper. It will write a new wrapper with a certain amount
of given information, see file.


## createNetCDF.py

Contains methods that create a new netCDF-file. See file for more information.


## newFileNames.py

Contains methods that generate new file names for wrapper- and netCDF-files


## select_data.py

Contains a method that given an interval and a pandas.Series will return the data within the
interval. Is used by the selector when marking data.


## track_edits.py

###### EditTracking

A class that is used to keep track of changes to variables within netCDF files that a wrapper
points to. Also has a method for creating a new history file (.hist) and a method that saves
all made changes which calls for methods that create new wrapper- and netCDF-files
