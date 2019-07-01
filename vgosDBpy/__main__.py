# Main method
import sys
from PySide2.QtWidgets import QApplication
from vgosDBpy.view.app import App
from vgosDBpy.read_log.parser import readMetData

if __name__ == '__main__':

    if sys.argv[1].endswith('.wrp'):
        # Create the Qt Application
        app = QApplication(sys.argv)

        # Create and show

        window = App(sys.argv[1])

        window.show()
        # Run the main Qt loop
        sys.exit(app.exec_())

    elif sys.argv[1].endswith('.log'):
        readMetData(sys.argv[1])
