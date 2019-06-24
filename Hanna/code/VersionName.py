# read wrp and try to change it

def NewVersionName(path,filename):
    filename= "Met.nc" #
    path= "./Files/10JAN04XK/WETTZELL/"+filename

    lhs,rhs = filename.split(".")
    last= lhs[-1]

    if last.isdigit():
        lastPlace = len(lhs) -1 ;
        print(lastPlace)
        newLast= int(last)+1
        newName=lhs[0:lastPlace]+str(newLast)+"."+rhs
    else:
        newName = lhs+"_V001."+rhs

    exists = os.path.isfile('/path/to/file')
    if exist:
        NewVersionName(path,newName)

    return NewName
