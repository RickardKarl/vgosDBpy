import sys
from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout
from PySide2.QtWidgets import QTreeView
from PySide2.QtCore import QAbstractItemModel

class Directory(QTreeView):
    def __init__(self, parent=None):
        super(Directory, self).__init__(parent)
        self.setWindowTitle("Wrapper content")
        model = TreeModel(parent)


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("My Form")

        # Create widgets
        self.edit = QLineEdit("Write my name here..")
        self.button = QPushButton("Show Greetings")
        self.button_Rickard = QPushButton('Rickards knapp')

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        layout.addWidget(self.button_Rickard)


        # Set dialog layout
        self.setLayout(layout)

        # Set button event
        self.button.clicked.connect(self.greetings)

    # Greets the user
    def greetings(self):
        print ("Hello {}".format(self.edit.text()))

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    a = Form()

    # Create and show the form
    a.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
