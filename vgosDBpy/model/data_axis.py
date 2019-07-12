class DataAxis:

    def __init__(self, axis, data):

        self.axis = axis
        self.data = data
        self.marked_data  = []

    def getAxis(self):
        return self.axis

    def getData(self):
        return self.data

    def getMarkedData(self):
        print(self.marked_data)
        return self.marked_data

    def addLine(self, line):
        return self.axis.add_line(line)


    def updateMarkedData(self, data):
        for point in data.iteritems():
            print(point)
            if point in self.marked_data:
                self.marked_data.remove(point)
            else:
                self.marked_data.append(point)

    def clearMarkedData(self):
        '''
        Unselect all marked data points
        '''
        self.marked_data = []


    def removeMarkedData(self):
        '''
        Delete all marked data from current data
        '''
        print(self.data[0])
        for mark in self.marked_data:
            print(mark)
