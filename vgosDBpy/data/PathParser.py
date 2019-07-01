"""
reads in a path and get information from it
"""

"./../../../../Files/10JAN04XU/TimeUTC.nc"
class PathParser():
    path = ""
    parts =[]
    sessionName=" "
    def __init__(self, str, session):
        self.path = str
        self.sessionName = str.fins(session)
        self.parts = self.path.split("/")

    def getEnd():
        return(parts[-1])

    def isNetCDF():
        last = self.getEnd()
        if last.find('.') is not -1:
            end = self.getFileFormat(last)
            if end == "nc":
                return True
        return False

    def getFileFormat(self,str):
        name,end = str.split('.')
        return end

    def getFileName(self, str):
        name,end = str.split('.')
        return name

    def isTime(self):
        for part in parts:
            if part == "TimeUTC":
                return True
        return False

def findCorrespondingTime(path):
    parts = path.split("/")
    timePath = "."
    for i in range(1,len(parts)-1 ):
        timePath = timePath + "/" + parts[i]
    timePath =  timePath + "/" + "TimeUTC.nc"
    return timePath


class netCDFPath():
    path
    ncPath={}
    def __init__(self, path):
        self.path = path

    def addVar(name):
        ncPath["variable"]=names

    def getVar():
        return ncPath["variable"]
