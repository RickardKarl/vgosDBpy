
import sys
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog)

class Form(QDialog):
    queue=[]
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        #self.edit = QLineEdit("Write my name here")
        array = ["b1", "b2","b3", "b4"]
        """
        self.b1=QPushButton(array[0])
        self.b2=QPushButton(array[1])
        # Create layout and add widgets
        layout = QVBoxLayout()
        #layout.addWidget(self.edit)
        layout.addWidget(self.b1)
        layout.addWidget(self.b2)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.b1.clicked.connect(lambda:self.whichbtn(self.b1))
        self.b2.clicked.connect(lambda:self.whichbtn(self.b2))
        """
        self.btn =[]
        #for str in array:
        #    myButtons.append(str)
        i=0
        layout = QVBoxLayout()
        for str in array:
            # add button
            self.btn.append(QPushButton(str))
            #add characteristics of the button
            self.btn[-1].clicked.connect(lambda:self.btnPressed(self.btn[-1]))
            self.btn[-1].toggle()
            #self.btn[-1].clicked.connect(lambda:self.btnstate(self.btn[-1]))
            layout.addWidget(self.btn[-1])
            # Set dialog layout
            # Add button signal to greetings slot

        self.enter = QPushButton("Done -> plot")
        self.enter.clicked.connect(self.enterPressed)
        layout.addWidget(self.enter)
        self.setLayout(layout)


    def btnPressed(self,b):
        #if queue.index(b) == -1.: # menaing in unpressed
        add_to_plot(b)

        #else:
        #    remove_from_plot(b)

    def remove_from_plot(btn):
        queue.remove(btn)

    def add_to_plot(btn):
        if len(queue)<=3:
            queue.append(btn)

    def enterPressed():
        print(queue)

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())


"""
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
"""
