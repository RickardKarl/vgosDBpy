from PySide2.QtWidgets import QToolBox, QPushButton


class Tools(QToolBox):

    def __init__(self, parent = None):
        super(Tools,self).__init__(parent)


        button1 = QPushButton('Test')

        self.addItem(button1,'More test')

        button2 = QPushButton('Even more test')

        self.addItem(button2,'Final test')
