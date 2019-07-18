
# Wrapper related
from PySide2.QtWidgets import QApplication
from vgosDBpy.view.app import App
from vgosDBpy.wrapper.parser import Parser

# Log related
from vgosDBpy.read_log.parser import readMetData, readCableCal, printFile, mergeSeries
from vgosDBpy.read_log.plotter import plotSeries


import argparse
import sys

class CommandLineInterface(argparse.ArgumentParser):
    dumpable_variables = ['Temp', 'AtmPres', 'RelHum','CableCal']
    def __init__(self):

        super(CommandLineInterface,self).__init__(prog = 'vgosDBpy')

        # Adding arguments
        self.add_argument('file', help = 'Read a file (*.wrp) or (*.log)')
        self.add_argument('--var', metavar = 'VARIABLE',
         help = 'Name of the variables that can be displayed: ' + ', '.join(CommandLineInterface.dumpable_variables))
        self.add_argument('-g','--graphic', help = 'Activate graphical user interface when reading wrapper',
                        action="store_true")


        # Retrieve arguments
        self.args = self.parse_args()

        # Decisions based on input ###################

        # Wrapper file input
        if self.args.file != None:
            # Checking if file looks correctly
            if self.args.file.endswith('.wrp'):

                # GUI
                if self.args.graphic == True:
                    # Create the Qt Application
                    app = QApplication(sys.argv)

                    # Create and show
                    window = App(self.args.file)

                    window.show()
                    # Run the main Qt loop
                    sys.exit(app.exec_())

                # Non-GUI
                else:
                    parser = Parser(self.args.file)
                    wrapper = parser.parseWrapper(self.args.file)
                    print(wrapper)

            elif self.args.file.endswith('.log'):
                print(self.args.log)

            else:
                raise ValueError('Wrong file given, does not end with .wrp or .log', self.args.file)

        else:
            pass


    def loop():
        pass
