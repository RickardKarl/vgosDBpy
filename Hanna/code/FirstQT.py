"""
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.openFileNameDialog()
        self.openFileNamesDialog()
        self.saveFileDialog()

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

"""

import sys
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog)
from plotFunction import plotFunc
from combineYMDHMS import combineYMDHMwithSec as combine
from createMap import plotMap
from readNetCDF import possible_to_plot

class Form(QDialog):
    #path = "./../../../../Files/10JAN04XU/KOKEE/Met.nc"
    #array = possible_to_plot(path)
    queue=[]
    path = "./../../../../Files/10JAN04XU/KOKEE/Met.nc"
    pathToTime = "./../../../../Files/10JAN04XU/TimeUTC.nc"
    m = plotMap()
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        #self.edit = QLineEdit("Write my name here")

        #array = ["b1", "b2","b3", "b4"]
        #path = "./../../../../Files/10JAN04XU/KOKEE/Met.nc"
        array = possible_to_plot(self.path)
        #queue=[]
        # Create layout and add widgets
        self.btn =[]
        #for str in array:
        #    myButtons.append(str)
        i=0
        layout = QVBoxLayout()
        for str in array:
            # add buttons
            self.btn.append(QPushButton(str,self))
            #add characteristics of the button
            self.btn[i].clicked.connect(self.btnClicked)
            self.btn[i].toggle()
            #self.btn[-1].clicked.connect(lambda:self.btnstate(self.btn[-1]))
            layout.addWidget(self.btn[i])
            # Set dialog layout
            # Add button signal to greetings slot
            i=i+1

        self.time = QPushButton("Time",self)
        layout.addWidget(self.time)
        self.time.clicked.connect(self.btnClicked)

        self.enter = QPushButton("Done -> plot")
        self.enter.clicked.connect(self.enterPressed)
        layout.addWidget(self.enter)
        self.setLayout(layout)


    def btnClicked(self):
        sender = self.sender()

        if self.queue.count(sender.text())==0: # menaing in unpressed
            self.add_to_plot(sender)
        else:
           self.remove_from_plot(sender)


    def remove_from_plot(self, btn):
        self.queue.remove(btn.text())
        self.m.removeFromMap(btn.text)


    def add_to_plot(self, btn):
        if len(self.queue)<=3:
            if btn.text == "Time":
                self.m.insertToMap(self.pathToTime,btn.text())
            else:
                self.m.insertToMap(self.path, btn.text())
            self.queue.append(btn.text())

    def enterPressed(self):
        #plot[]
        #for i in range(len(self.queue)):
            #plot.append[map[self.queue[i]]]
        print(self.m.getMapKeys())
        xStr= self.queue[0]
        xData = self.m.getKeyValue(xStr)
        yStr= self.queue[1]
        yData = self.m.getKeyValue(yStr)
        plotFunc(xStr, xData, yStr, yData,0)
        self.queue.clear()


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    #path = "./../../../../Files/10JAN04XU/KOKEE/Met.nc"
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())


"""
##################################################################
import sys
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from PySide2.QtWidgets import *


class Form(QDialog):
   def __init__(self, parent=None):
      super(Form, self).__init__(parent)

      layout = QVBoxLayout()
      self.b1 = QPushButton("Button1")
      self.b1.clicked.connect(lambda:self.whichbtn(self.b1))
      layout.addWidget(self.b1)

      self.b2 = QPushButton("Button2")
      #self.b2.setIcon(QIcon(QPixmap("python.gif")))
      self.b2.clicked.connect(lambda:self.whichbtn(self.b2))
      layout.addWidget(self.b2)
      self.setLayout(layout)
      self.b3 = QPushButton("Disabled")
      #self.b3.setEnabled(False)
      layout.addWidget(self.b3)

      self.b4 = QPushButton("&Default")
      self.b4.setDefault(True)
      self.b4.clicked.connect(lambda:self.whichbtn(self.b4))
      layout.addWidget(self.b4)

      self.setWindowTitle("Button demo")

  # def btnstate(self):
    #  if self.b1.isChecked():
    #     print ("button pressed")
     # else:
    #     print ("button released")

   def whichbtn(self,b):
      print("clicked button is "+b.text())

def main():
   app = QApplication(sys.argv)
   ex = Form()
   ex.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()



import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog)

app = QApplication(sys.argv)

data = ['folder1/file1', 'file2', 'file3', 'folder2/file4']

treeWidget = QTreeWidget()
treeWidget.setColumnCount(1)
treeWidget.setMinimumSize(600, 400)

items = []

for item in data:
    itemparts = item.split('/')

    entry = QTreeWidgetItem(None, [itemparts[0]])
    partentitem = entry

    if len(itemparts) > 1:
        for i in itemparts[1:]:
            childitem = QTreeWidgetItem(None, [i])
            partentitem.addChild(childitem)
            partentitem = childitem

    items.append(entry)

treeWidget.insertTopLevelItems(0, items)

treeWidget.show()
app.exec_()
"""
