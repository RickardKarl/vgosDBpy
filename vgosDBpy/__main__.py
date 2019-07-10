# Main method
import sys
from PySide2.QtWidgets import QApplication
from vgosDBpy.view.app import App
from vgosDBpy.read_log.parser import readMetData, readCableCal, printFile, mergeSeries
from vgosDBpy.read_log.plotter import plotSeries

#Hanna
from vgosDBpy.data.readNetCDF import print_name_dtype_dim_length
#from vgosDBpy.data.createNewWrp import create_new_wrapper

if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1].endswith('.wrp'):
            # Create the Qt Application
            app = QApplication(sys.argv)

            # Create and show

            window = App(sys.argv[1])

            window.show()
            # Run the main Qt loop
            sys.exit(app.exec_())

        elif sys.argv[1].endswith('.log'):

            data = readCableCal(sys.argv[1])
            metData = readMetData(sys.argv[1])
            data = mergeSeries(data['CableCal'], metData['Temp'], return_right = False)
            if len(sys.argv) > 2:
                plotSeries(metData[sys.argv[2]])

        elif sys.argv[1] == 'Hanna':

            path = "./../../Files/10JAN04XK/Apriori/num"
            #path = "./../../Files/10JAN04XU/Session/GroupBLWeights.nc"
            #path = "../../Files/10JAN04XK/10JAN04XK_V005_iGSFC_kall.wrp"
            #path = "./../../Files/10JAN04XU/Head.nc"
            print_name_dtype_dim_length(path)
            #create_new_wrapper(path)
    else:
        pass
