import sys
import os
from PySide2.QtWidgets import QApplication, QTreeView, QAbstractItemView, QWidget, QTextEdit, QPushButton, QVBoxLayout
from standardtree import TreeModel


'''
Will soon enough be moved to view folder

'''

class QWrapper(QTreeView):
    '''
    Widget that inherits from QTreeView
    Visual representation of the wrapper as a folder structure

    Imports TreeModel which is the model representation of the wrapper

    Constructor needs:
    root_path [string]
    wrapper_file [string]
    parent [QWidget]


    '''
    def __init__(self, root_path, wrapper_file, parent=None):
        super(QWrapper, self).__init__(parent)

        # Setup model
        self.model = TreeModel(['Name', 'Type'], root_path, wrapper_file)
        self.setModel(self.model)

        # Selection of items
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.selection = self.selectionModel()
        # Expand first column
        self.expandToDepth(0)

        # Quality of life features for the QTreeView
        self.setExpandsOnDoubleClick(True)
        #self.setEditTriggers(QAbstractItemView.NoEditTriggers) # Sets through the view so that editing is not possible


    def currentSelectionModel(self):
        return self.selectionModel()

    def changeSelection(self):
        pass

class App(QWidget):
    '''
    Frame for testing stuff
    '''

    def __init__(self, parent = None):
        super(App,self).__init__(parent)

        # Creating widgets

        # Wrapper view
        self.treeview = QWrapper(os.getcwd(), sys.argv[1], self)

        # Text
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)

        # Button
        self.button = QPushButton('& Details',self)
        # Button event
        self.button.clicked.connect(self.showItemInfo)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.treeview)
        layout.addWidget(self.text)
        layout.addWidget(self.button)
        self.setLayout(layout)


    def getSelected(self):
        return self.treeview.selection.selectedIndexes()

    def showItemInfo(self):
        index = self.getSelected()
        for i in index:
            print(i)
            item = self.treeview.model.itemFromIndex(i)
            self.text.setPlainText(str(item))
        print(self.treeview.currentSelectionModel())


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show
    window = App()

    window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
