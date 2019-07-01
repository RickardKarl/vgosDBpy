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
            if end == "nc"
                return True
        return False

    def getFileFormat(str):
        name,end = str.split('.')
        return end

    def getFileName(str):
        name,end = str.split('.')
        return name

    class netCDFPath():
        path
        ncPath={}
        def __init__(self, path):
            self.path = path

        def addVar(name):
            ncPath["variable"]=names

        def getVar():
            return ncPath["variable"]
