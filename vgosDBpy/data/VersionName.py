# read wrp and try to change it
import os

"""
DOES: takes in a string as a path. Then decides what the next version should be called,
plus checks if that version already exists.
"""
def NewVersionName(path):
    #filename= "Met.nc" #
    path= "./Files/10JAN04XK/WETTZELL/Met.nc"#+filename
    path_split= path.split("/")
    path_to_file = path_split[0:-2]
    print(path_to_file)
    filename=path_split[-1]
    parts =[]
    parts = filename.split(".")
    lhs,rhs = filename.split(".")
    last= lhs[-1]
    NewName = " "

    if last.isdigit():
        lastPlace = len(lhs) -1 ;
        print(lastPlace)
        newLast= int(last)+1
        newName=lhs[0:lastPlace]+str(newLast)+"."+rhs
    else:
        newName = lhs+"_V001."+rhs

    exists = os.path.isfile(newName)
    if exists:
        NewVersionName(newName)

    return NewName

path= "./Files/10JAN04XK/WETTZELL/Met.nc"
print(NewVersionName(path))