from PySide2.QtWidgets import QMessageBox, QPushButton, QInputDialog

def popUpBoxEdit(msg):

    msgBox = QMessageBox()

    msgBox.setText('Confirm saving your changes:')
    msgBox.setDetailedText(msg)

    save_button = msgBox.addButton(QMessageBox.Save)
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


def history_information():
    dialogBox= QInputDialog()
    info = []
    dialog = QInputDialog.getText(dialogBox, 'Enter the history iformation', 'Version:')
    info.append(dialog[0])
    dialog = QInputDialog.getText(dialogBox, 'Enter the history iformation', 'Author:')
    info.append(dialog[0])
    dialog = QInputDialog.getText(dialogBox, 'Enter the history iformation', 'RunTimeTag:')
    info.append(dialog[0])
    return info


def popUpChooseCurrentAxis(plotted_data_axis):
    '''
    A window pops up and allows you to choose one of the given DataAxis in plotted_data_axis

    Return the selected one
    '''
    if len(plotted_data_axis) > 1:
        button_pressed_map = {}
        button_list = []

        for ax in plotted_data_axis:
            name = str(ax.getItem())
            button = QPushButton(name)

            button_list.append(button)
            button_pressed_map[button] = ax

        dialog_box = QMessageBox()
        dialog_box.setText('Choose which variable that you want to have control over currently:')

        for button in button_list:
            dialog_box.addButton(button, QMessageBox.AcceptRole)

        dialog_box.exec_()

        pressed_button = dialog_box.clickedButton()

        return button_pressed_map.get(pressed_button)

    elif len(plotted_data_axis) == 1:
        dialog_box = QMessageBox()
        dialog_box.setText('Only one variable being plotted.')
        dialog_box.addButton(QMessageBox.Ok)
    else:
        dialog_box = QMessageBox()
        dialog_box.setText('Nothing is plotted currently.')
        dialog_box.addButton(QMessageBox.Ok)
