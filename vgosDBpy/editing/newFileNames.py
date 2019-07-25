# read wrp and try to change it
import os

"""
DOES: takes in a string as a path. Then decides what the next version should be called,
plus checks if that version already exists.
"""
def newVersionName(path):
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
        int_file_digit = int(file_digit)
        if int_file_digit <= 9:
            if int_file_digit+1 != 10:
                file_digit = '00' + str(int_file_digit+1)
            else:
                file_digit = '010'
        elif len(file_digit) <= 99:
            if int_file_digit+1 != 100:
                file_digit = '0' + str(int_file_digit+1)
            else:
                file_digit = '100'
        elif len(file_digit) <= 999:
            if int_file_digit+1 != 1000:
                file_digit = str(int_file_digit+1)
            else:
                if int_file_digit+1 >= 1000:
                    raise ('Can not create anymore files, excedded limit of 999 versions')

        new_file_name = file_name_non_digit + file_digit + '.' + rhs

    file_path = path_to_file + '/' + new_file_name

    # Checks if the generated name currently exists, if so call method recurvsively
    if os.path.isfile(file_path):
        return newVersionName(file_path)
    # Else return new file name
    else:
        return file_path

def newWrapperName(wrapper_path):
    pass



def newHistFileName(hist_path):
    hist_path = hist_path.split('/')
    hist_file = hist_path.pop().split('.')

    hist_name = '/'.join(hist_path) + '/' + hist_file[0] + '_test' + '.' + hist_file[1]
    return hist_name
