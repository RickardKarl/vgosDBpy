# How to copy a file
from vgosDBpy.wrapper.parser import Parser
from vgosDBpy.data.PathParser import PathParser
from vgosDBpy.data.VersionName import NewVersionName
from vgosDBpy.wrapper.equalWrapper import equal
import os

    # from split find directory by going trough all words
    # and see if they matches any in the predefined list of directories possible, which is found by
    # looping through the wrapper that one reads in and seraches for the keyword "default_dir"

def create_new_wrapper(list_changed_files, new_file_names, path_to_old_wrp, new_wrp_name):

    path_to_new_wrp = new_wrp_path(path_to_old_wrp, new_wrp_name)

    if os.path.isfile(path_to_new_wrp):
        raise ValueError('Path to new wrapper already exists, can not overwrite.')

    parser = Parser(path_to_old_wrp)

    possible_directories = parser.find_all_directories(path_to_old_wrp)

    old_file_names = []
    #new_file_names = []
    target_directory = []

    # goes through the list of paths to all changed files.
    for pathToChangedFile in list_changed_files:
        #Collect old and new file name
        old_file_names.append(pathToChangedFile.split('/')[-1] )
        #new_file_names.append(NewVersionName(pathToChangedFile) )
        parsed_path = pathToChangedFile.split('/')
        # find where the files is
        marker = 0
        #parsed_path  = pathToChangedFile.split('/')
        for dir in possible_directories:
            if dir in parsed_path:
                target_directory.append(dir)
                marker = 1
                break
        if marker == 0 :
            target_directory.append('non')

    map = {} # connects a name of directory to list of strings on the fotmat 'old_name-new_name'
    c = 0
    for dir in target_directory:
        #not target_directory not in map yet
        dir = dir.lower().strip()
        if dir not in map:
            #dir = dir.lower().strip()
            map[dir] = []
        map[dir].append(old_file_names[c]+'@'+new_file_names[c])
        c += 1

    # initialy we are not in a direcotory
    changes_files_in_current_directory = []
    current_directory = 'non'

    #if current_directory in map:
    #    changes_files_in_current_directory = map[current_directory]

    with open(path_to_old_wrp, 'r') as old_wrapper:
        with open(path_to_new_wrp , 'w+') as new_wrapper:
            for line in old_wrapper:
                l = line.lower().strip()
                # checks if the line is entry to new directory
                # and if so updates the current_directory
                if l.startswith('default_dir'):
                    current_directory = l.split()[1]

                if current_directory in map:
                    changes_files_in_current_directory = map[current_directory]
                else:
                    changes_files_in_current_directory = []

                written = False

                for itm in changes_files_in_current_directory:
                    names = itm.split('@')
                    old_name = names[0]
                    new_name = names[1]

                    if l == old_name.lower().strip():
                        new_wrapper.write(new_name+'\n')
                        written = True

                if written is False :
                    new_wrapper.write(line)

        new_wrapper.close()
    old_wrapper.close()

## old version with only one changed file below somwhat intact
"""
    in_right_directory = False
    current_directory = 'non'
    with open(path_to_old_wrp, 'r') as old_wrapper:
        with open(path_to_new_wrp , 'w+') as new_wrapper:

            for line in old_wrapper:
                # if target_directory is non
                if target_directory == 'non':
                    if line.strip() == old_file_name.strip():
                        new_wrapper.write(new_file_name)
                    else:
                        new_wrapper.write(line)
                else:
                    l = line.lower().strip()
                    if l.startswith('default_dir'):
                        if line.split()[1] == target_directory:
                            in_right_directory = True
                        else:
                            in_right_directory = False
                    if in_right_directory is True:
                         if line.strip() == old_file_name.strip():
                             new_wrapper.write(new_file_name+ "\n")
                             in_right_directory = False
                         else:
                             new_wrapper.write(line)
                    else:
                        new_wrapper.write(line)
        new_wrapper.close()
    old_wrapper.close()
"""
def new_wrp_path(old_wrp_path, new_wrp_name):
    splits = old_wrp_path.split('/')

    if not new_wrp_name.endswith('.wrp'):
        new_wrp_name = new_wrp_name + '.wrp'

    splits[-1] = new_wrp_name
    return '/'.join(splits)

# DEBUG Function
def print_wrapper_file(pathToWrp):
    with open(pathToWrp, 'r') as wrp :
        for line in wrp:
            print(line)

def test():
    old= '../../Files/10JAN04XK/10JAN04XK_V005_iGSFC_kall.wrp'
    new= '10JAN04XK_V005_iGSFC_kall_testa_2.wrp'
    new_path = '../../Files/10JAN04XK/10JAN04XK_V005_iGSFC_kall_testa_2.wrp'
    file = ['../../Files/10JAN04XK/10JAN04XK/Head.nc','../../Files/10JAN04XK/10JAN04XK/WETTZELL/Met.nc']
    new_names = ['Head_V001.nc', 'Met_v001.nc']
    create_new_wrapper(file, new_names, old, new)
    print_wrapper_file(new_path)
    #print_wrapper_file(old)
    #equal(old, new_path)
