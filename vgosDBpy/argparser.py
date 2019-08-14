import argparse
import sys

# Wrapper related
from PySide2.QtWidgets import QApplication
from vgosDBpy.view.app import vgosDBpyGUI
from vgosDBpy.wrapper.parser import Parser

# Script-driven
from vgosDBpy.script_driven.script_main import script_class
from vgosDBpy.data.getName import create_wrp_path


class CommandLineInterface(argparse.ArgumentParser):

    '''
    A command-line interface that is implemented with argparse.ArgumentParser

    Is called by __main__.py
    '''

    def __init__(self):
        super(CommandLineInterface,self).__init__(prog = 'vgosDBpy')

        # Adding arguments
        self.add_argument('file', help = 'Read a file (*.wrp or *.txt)')
        self.add_argument('-g','--graphic', help = 'Activate graphical user interface when reading wrapper',
                        action="store_true")

        # Retrieve arguments
        self.args = self.parse_args()
        self.script = script_class()

        ####### Control flow based on input ###################

        # Wrapper file input

        # Checking if file looks correctly
        if self.args.file.endswith('.wrp'):
            wrp_path = create_wrp_path(self.args.file)

            # GUI if -g flag is given
            if self.args.graphic == True:
                # Create the Qt Application
                app = QApplication(sys.argv)


                window = vgosDBpyGUI(wrp_path)
                window.show()

                # Run the main Qt loop
                sys.exit(app.exec_())

            # Non-GUI
            else:
                parser = Parser(wrp_path)
                wrapper = parser.parseWrapper()
                print(wrapper)

        # Parse a .txt file for the script driven feature
        elif self.args.file.endswith('.txt'):
            self.script.script(self.args.file)
