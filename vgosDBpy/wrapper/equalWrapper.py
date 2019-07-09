"""
Equal method for wrapper
takes in two wrappers.
"""
#from vgosDBpy.data.
"""
from readNetCDF import read_netCDF_variables as get_vars, get_dtype_for_var

def contains_same_vars(path1, path2):

    variables_1 = get_vars(path1)
    variables_2 = get_vars(path2)

    if len(variables_1) != len(variables_2):
        return False

    for var in variables_1:
        if var not in variables_2:
            return False
    return True

def contains_same_data(path1, var1, path2, var2):
     dtypes_1 = get_dtype_for_var(path1, var1)
     dtypes_2 = get_dtype_for_var(path2, var2)

"""
from tree import Wrapper
from parser import Parser

def equal(path_1, path_2):
    parser_1= Parser(path_1)
    parser_2= Parser(path_2)

    str_1 = str(parser_1.parseWrapper(path_1)).splitlines()
    str_2 = str(parser_2.parseWrapper(path_2)).splitlines()
    #str_1 = str(wrapper_1)
    #str_2 = str(wrapper_2)
    c=0
    if len(str_1) >= len(str_2):
        for line in str_1:
            if c < len(str_2):
                line_2 = str_2[c]
                c = c+1
                if line != line_2:
                    print(line + "\ndiffers from\n" + line_2)
            else:
                print(line)
    else:
        for line in str_2:
            if c <= len(str_1):
                line_1 = str_1[c]
                c = c+1
                if line != line_1:
                    print(line + "\ndiffers from\n" + line_1)
            else:
                print(line)

path1='./../../../../Files/10JAN04XK/10JAN04XK_V005_iGSFC_kall.wrp'

path2='./../../../../Files/10JAN04XK/10JAN04XK_V005_iGSFC_kngs.wrp'

equal(path1, path2)
