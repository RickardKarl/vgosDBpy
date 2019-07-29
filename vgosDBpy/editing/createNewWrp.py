# How to copy a file
from vgosDBpy.wrapper.parser import Parser
from vgosDBpy.data.PathParser import PathParser
from vgosDBpy.editing.newFileNames import newVersionName, newWrapperPath
from vgosDBpy.wrapper.equalWrapper import equal
import os

    # from split find directory by going trough all words
    # and see if they matches any in the predefined list of directories possible, which is found by
    # looping through the wrapper that one reads in and seraches for the keyword "default_dir"

def create_new_wrapper(list_changed_files, new_file_names, path_to_old_wrp, hist_file_name, timestamp):

    path_to_new_wrp = newWrapperPath(path_to_old_wrp)
    #print('Creating wrapper with path:', path_to_new_wrp)

    if os.path.isfile(path_to_new_wrp):
        path_to_new_wrp = newWrapperPath(path_to_new_wrp)

    #print(path_to_new_wrp)

    parser = Parser(path_to_old_wrp)

    possible_directories = parser.find_all_directories(path_to_old_wrp)

    old_file_names = []
    target_directory = []

    # goes through the list of paths to all changed files.
    for pathToChangedFile in list_changed_files:

        #Collect old and new file name
        old_file_names.append(pathToChangedFile.split('/')[-1])
        parsed_path = pathToChangedFile.split('/')

        # find where the files is
        marker = 0

        for dir in possible_directories:
            if dir in parsed_path:
                target_directory.append(dir)
                marker = 1
                break
        if marker == 0 :
            target_directory.append(None)

    map = {} # connects a name of directory to list of strings on the fotmat 'old_name-new_name'
    c = 0
    for dir in target_directory:
        #not target_directory not in map yet
        dir = dir.lower().strip()
        if dir not in map:
            map[dir] = []
        map[dir].append(old_file_names[c])
        map[dir].append(new_file_names[c])
        c += 1
    # initialy we are not in a direcotory
    changes_files_in_current_directory = []
    current_directory = None

    with open(path_to_old_wrp, 'r') as old_wrapper:
        with open(path_to_new_wrp , 'w+') as new_wrapper:
            for line in old_wrapper:
                l = line.lower().strip()
                # checks if the line is entry to new directory
                # and if so updates the current_directory
                if l.startswith('default_dir'):
                    current_directory = l.split()[1]
                elif l == 'end history':
                    writeHistoryBlock(new_wrapper, hist_file_name, timestamp)

                if current_directory in map:
                    changes_files_in_current_directory = map[current_directory]
                else:
                    changes_files_in_current_directory = []

                written = False

                if changes_files_in_current_directory != []:
                    old_name = changes_files_in_current_directory[0]
                    new_name = changes_files_in_current_directory[1]

                    keywords = l.split()
                    if old_name.lower().strip() in keywords:
                        new_wrapper.write(new_name+'\n')
                        written = True

                if written is False:
                    new_wrapper.write(line)

        new_wrapper.close()
    old_wrapper.close()

def writeHistoryBlock(file, hist_file_name, timestamp):
    file.write('!\n')
    file.write('Begin Process vgosDBpy\n')
    file.write('Version ----\n')
    file.write('CreatedBy ---\n')
    file.write('Default_dir History\n')
    file.write('RunTimeTag ----\n')
    file.write('History ' + hist_file_name + '\n')
    file.write('End Process vgosDBpy\n')

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
