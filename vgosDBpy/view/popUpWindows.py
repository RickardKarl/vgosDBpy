from PySide2.QtWidgets import QMessageBox, QPushButton, QInputDialog

def popUpBoxEdit(msg):
    '''
    A pop-up window to confirm if one should save tracked changes

    msg [string] is the displayed information in the window

    Will return buttonRole of pressed button

    '''

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
    '''
    A pop-up window to confirm if one should save a table in ASCII

    path [string] is the displayed path to the new history file

    Will return buttonRole of pressed button
    '''

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
    info = ''
    dialog = QInputDialog.getText(dialogBox, 'Enter the history iformation', 'Author:')
    info=dialog[0]
    return info


def popUpChooseCurrentAxis(plotted_data_axis):
    '''
    A window pops up and allows you to choose one of the given DataAxis in plotted_data_axis

    plotted_data_axis [list of DataAxis] is the data_axis to choose between

    Return the selected data_axis
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
