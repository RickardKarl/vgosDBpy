class DataAxis:

    def __init__(self, axis, data):

        self.axis = axis
        self.data = data

    def getAxis(self):
        return self.axis

    def getData(self):
        return self.data

    def addLine(self, line):
        return self.axis.add_line(line)
