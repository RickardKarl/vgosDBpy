"""
Equal method for wrapper
takes in two wrappers and prints all the lines that differs.
"""
from vgosDBpy.wrapper.tree import Wrapper
from vgosDBpy.wrapper.parser import Parser

def equal(path_1, path_2):
    parser_1= Parser(path_1)
    parser_2= Parser(path_2)

    str_1 = str(parser_1.parseWrapper(path_1)).splitlines()
    str_2 = str(parser_2.parseWrapper(path_2)).splitlines()
    c=0
    if len(str_1) >= len(str_2):
        for line in str_1:
            if c < len(str_2):
                line_2 = str_2[c]
                c = c+1
                if line.strip() != line_2.strip():
                    print(line + "differs from" + line_2)
    else:
        for line in str_2:
            if c <= len(str_1):
                line_1 = str_1[c]
                c = c+1
                if line.strip() != line_1.strip():
                    print(line + "differs from" + line_1)
