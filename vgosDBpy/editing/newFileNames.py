
import os
import re

"""
Takes in a path to a netCDF-file and decides what the next version of the file in the path should be named
input: path: [string]
output: file_path: [string]
"""
def new_netCDF_name(path):
    path_split= path.split("/")

    # Create path to the actual folder by removing last item in path
    path_to_file = path_split[0:-1]
    path_to_file = '/'.join(path_to_file)

    # Get filename
    filename=path_split[-1]

    # Remove ending of filename and check if last character is a digit
    lhs,rhs = filename.split(".")
    file_name_non_digit = ""
    file_digit = ""

    # Split filename in non-digit part and digit part
    for char in lhs:
        if char.isdigit():
            file_digit = file_digit + char
        else:
            file_name_non_digit = file_name_non_digit + char

    # If no digit exists
    if file_digit == "":
        new_file_name = lhs +"_V001."+rhs

    # Else if digit exists
    else:
        file_digit = _getStringDigit(file_digit)
        new_file_name = file_name_non_digit + file_digit + '.' + rhs

    file_path = path_to_file + '/' + new_file_name

    # Checks if the generated name currently exists, if so call method recurvsively
    if os.path.isfile(file_path):
        return new_netCDF_name(file_path)
    # Else return new file name
    else:
        return file_path

"""
Takes in a path to a wrp-file and decides what the next version of the file in the path should be named
input: path: [string]
output: string]
"""
def new_wrapper_path(wrapper_path):
    path_splits = wrapper_path.split('/')
    wrapper_name = path_splits[-1]
    root_path = '/'.join(path_splits[0:-1])

    if not wrapper_name.endswith('.wrp'):
        new_wrp_name = new_wrp_name + '.wrp'

    name_splits = wrapper_name.split('_')

    version_number = None
    regexp = re.compile(r'V\d{3}')
    index = 0
    for s in name_splits:
        if regexp.match(s):
            version_number = s
            break
        index += 1

    if version_number == None:
        raise ValueError('Can not find version number in wrapper file.') # Should be fixed so that it adds a version number

    name_splits[index] = 'V' + _getStringDigit(version_number[1:])

    return root_path + '/' + '_'.join(name_splits)

"""
Help function in getting a new name for a file
input: str_digit: [string]
output: file_digit: [string]
"""
def _getStringDigit(str_digit):
    ## Expects string on format 'XXX' where X is an integer 0-9
    int_file_digit = int(str_digit)
    if int_file_digit <= 9:
        if int_file_digit+1 != 10:
            file_digit = '00' + str(int_file_digit+1)
        else:
            file_digit = '010'
    elif int_file_digit <= 99:
        if int_file_digit+1 != 100:
            file_digit = '0' + str(int_file_digit+1)
        else:
            file_digit = '100'
    elif int_file_digit <= 999:
        if int_file_digit+1 != 1000:
            file_digit = str(int_file_digit+1)
        else:
            if int_file_digit+1 >= 1000:
                raise ('Can not create anymore files, excedded limit of 999 versions')

    return file_digit
