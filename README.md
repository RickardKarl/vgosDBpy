# vgosDBpy

**Authors: Hanna Ek & Rickard Karlsson**

This project was developed during a summer internship at NVI Inc. @ NASA GSFC

## How to install vgosDBpy
Read the installation manual in /Manuals/.

###### Get the files to your computer

Either download the zip-file from the github repository or enter 'git clone https://github.com/RickardKarl/vgosDBpy.git' in the terminal


## How to use vgosDBpy
Read user manual in /Manuals/.


# Overview of code
Inside each folder is a README.md file that gives a brief explanation of each file.

###### __main__.py
Code block that is running when executing vgosDBpy.

###### argparser.py
This argument parser is the code which creates the command-line user interface. Called by __main__.py

###### wrapper
Parses a wrapper and keep track of it's content with a tree structure, this structure is then readable by code in the /model/ folder.

###### model
Mostly Qt-based models that consists of different data structures which among other things contains variable data and wrapper directory tree. Another model is the *DataAxis*, it keeps track of the data displayed in both plots and tables. This is required to connect what's displayed at the same time in a table and a plot. It is also used to track changes in the data. 

###### view
Contains all Qt-widgets, which is the main window, plot/table widgets, button and etc. Also has *AxesControlBox* which has a lot of control features between model and view.

###### editing
Makes it possible to edit/save data in the netCDF files. Also contains the methods that generate not only the new netCDF files but new filenames, wrappers and history files. 

###### read_log
A working, but unpolished, set of code that can parse a log file and plot weather data as well as cable calibration data.

###### data
Reads netCDF files, and also code that retrieves information for the plots and tables

###### script_driven
Code that controls the script driven features of vgosDBpy

