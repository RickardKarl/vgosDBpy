# Test code sheet to learn python and do tests

"""
# Monday 17/6 -2019
print("Hello NVI")

# syntax for-loop
for i in range(10,20):
  print("Now I am number ", i)
  j=3

# syntax if-loop
j = 2
if j==2:
  print ("j is 2")

else:
  print("j is not 2")

b=5
while b>3:
  print ("b is larger than 3")
  b -= 1
"""

# Monday 24/6 - 2019
# Structure for what to print, when moving along tree structure.
"""
if elem is folder:
    for child in elem:
        print child
        add listner to child
        child is child.getType
elif elem is file:
    for var in elem.variables():
        print var.name()
        add listner to var
        var is var.getType
elif elem is array:
    for line in elem:
        print (line)
"""

import sys
from PySide2.QtWidgets import QApplication, QPushButton
from PySide2.QtCore import Slot

@Slot()
def say_hello():
 print("Button clicked, Hello!")

# Create the Qt Application
app = QApplication(sys.argv)
# Create a button, connect it and show it
button = QPushButton("Click me")
button.clicked.connect(say_hello)
button.show()
# Run the main Qt loop
app.exec_()
