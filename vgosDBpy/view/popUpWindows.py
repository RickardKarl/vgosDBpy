from PySide2.QtWidgets import QMessageBox

def popUpBoxEdit(msg):

    msgBox = QMessageBox()

    msgBox.setText('Confirm the following changes:')
    msgBox.setInformativeText(msg)

    msgBox.addButton(QMessageBox.Save)
    msgBox.addButton(QMessageBox.Cancel)
    msgBox.addButton(QMessageBox.Reset)

    msgBox.exec_()

    pressed_button = msgBox.clickedButton()
    return msgBox.buttonRole(pressed_button)

def popUpBoxTable(path):

    msgBox = QMessageBox()

    msgBox.setText('Confirm the following action:')
    text = 'Save table in ASCII-format as:' + path
    msgBox.setInformativeText(text)

    msgBox.addButton(QMessageBox.Save)
    msgBox.addButton(QMessageBox.Cancel)

    msgBox.exec_()

    pressed_button = msgBox.clickedButton()
    return msgBox.buttonRole(pressed_button)
