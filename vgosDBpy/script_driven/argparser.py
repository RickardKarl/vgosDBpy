
# Wrapper related
from PySide2.QtWidgets import QApplication
from vgosDBpy.view.app import App
from vgosDBpy.wrapper.parser import Parser

# Log related
from vgosDBpy.read_log.parser import LogInfo
from vgosDBpy.read_log.plotter import plotSeries

# Script-driven
from vgosDBpy.script_driven.script_main import script_class

from vgosDBpy.data.getName import create_wrp_path
import argparse
import sys

class CommandLineInterface(argparse.ArgumentParser):

    '''
    A command-line interface that is implemented with argparse.ArgumentParser

    Is called by __main__.py
    '''

    dumpable_variables = []
    for var in LogInfo.available_variables:
        dumpable_variables.append(var.capitalize())


    def __init__(self):
        super(CommandLineInterface,self).__init__(prog = 'vgosDBpy')

        # Adding arguments
        self.add_argument('file', help = 'Read a file (*.wrp or *.txt)')
        self.add_argument('-g','--graphic', help = 'Activate graphical user interface when reading wrapper',
                        action="store_true")

        #self.add_argument('--var', metavar = 'VARIABLE',
        # help = 'Name of the variables that can be displayed: ' + ', '.join(CommandLineInterface.dumpable_variables))

        # Retrieve arguments
        self.args = self.parse_args()
        self.script = script_class()

        # Decisions based on input ###################

        # Wrapper file input

        # Checking if file looks correctly
        if self.args.file.endswith('.wrp'):
            wrp_path = create_wrp_path(self.args.file)

            # GUI
            if self.args.graphic == True:
                # Create the Qt Application
                app = QApplication(sys.argv)

                # Create and show
                #wrp_path = create_wrp_path(self.args.file)
                window = App(wrp_path)

                window.show()
                # Run the main Qt loop
                sys.exit(app.exec_())

            else:
                parser = Parser(wrp_path)
                wrapper = parser.parseWrapper()
                print(wrapper)

        elif self.args.file.endswith('.txt'):
            self.script.script(self.args.file)

        '''
        elif self.args.file.endswith('.log'):
            if self.args.var != None:
                variable_exists = self.args.var.lower() in LogInfo.available_variables
                assert variable_exists, 'Given variable ' + self.args.var + ' is not recognized'

                read_log = LogInfo(self.args.file)
                read_log.plotVar(self.args.var)
        '''



        #else:
        #    raise ValueError('Wrong file given, does not end with .wrp or .log', self.args.file)


    def loop():
        pass
