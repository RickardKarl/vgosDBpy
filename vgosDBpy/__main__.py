# Main method
import sys
from PySide2.QtWidgets import QApplication
from vgosDBpy.view.app import App
#from vgosDBpy.read_log.parser import readMetData, readCableCal, printFile, mergeSeries
from vgosDBpy.read_log.plotter import plotSeries
from vgosDBpy.script_driven.argparser import CommandLineInterface

#Hanna
from vgosDBpy.data.netCDFdebug import print_name_dtype_dim_length
from vgosDBpy.editing.createNewWrp import test


if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'Hanna':

            #path = "./../../Files/10JAN04XK/Apriori/Antenna.nc"
            #path = "./../../Files/10JAN04XU/Session/GroupBLWeights.nc"
            #path = "../../Files/10JAN04XK/10JAN04XK_V005_iGSFC_kall.wrp"
            #path = "./../../Files/10JAN04XU/Head.nc"
            #path = "./../../Files/10JAN04XK/WETTZELL/Met.nc"
            #print_name_dtype_dim_length(path)
            #print(get_constants(path))
            #create_new_wrapper(path)
            path = '../../Files/10JAN04XK/10JAN04XK_V005_iGSFC_kall.wrp'
            print_wrapper_file(path)
            test()
        else:
            interface = CommandLineInterface()

    else:
        interface = CommandLineInterface()
