# Main method
import sys
from PySide2.QtWidgets import QApplication
from vgosDBpy.view.app import App
from vgosDBpy.read_log.parser import readMetData, readCableCal, printFile, mergeSeries
from vgosDBpy.read_log.plotter import plotSeries
from vgosDBpy.data.readNetCDF import print_name_dtype_dim_length

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
            print(data['CableCal'])
            print(metData['Temp'])
            data = mergeSeries(data['CableCal'], metData['Temp'], return_right = False)
            plotSeries(data)

        elif sys.argv[1] == 'Hanna':

            path = "./../../Files/10JAN04XU/ObsEdit/NumGroupAmbig_iGSFC_bX.nc"
            #path = "./../../Files/10JAN04XU/Head.nc"
            print_name_dtype_dim_length(path)
    else:
        pass
