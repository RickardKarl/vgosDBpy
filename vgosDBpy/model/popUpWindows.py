from PyQt5.QtWidgets import QMessageBox

def popUpBoxEdit(msg):
    msgBox = QMessageBox()
    msgBox.setText('The changes were saved!')
    msgBox.setInformativeText(msg)
    msgBox.exec_()

def popUpBoxTable(msg):
    msgBox = QMessageBox()
    msgBox.setText('The table were saved to an ASCII file!')
    msgBox.setInformativeText(msg)
    msgBox.exec_()
