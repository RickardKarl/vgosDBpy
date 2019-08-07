"""
reads in a path and get information from it
"""

import os

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

    def get_parts(self):
        return self.parts
