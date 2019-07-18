# How to copy a file
from vgosDBpy.wrapper.parser import Parser
from vgosDBpy.data.PathParser import PathParser
from vgosDBpy.data.VersionName import NewVersionName
from vgosDBpy.wrapper.equalWrapper import equal

    # from split find directory by going trough all words
    # and see if they matches any in the predefined list of directories possible, which is found by
    # looping through the wrapper that one reads in and seraches for the keyword "default_dir"

def create_new_wrapper(pathToChangedFile, path_to_old_wrp, new_wrp_name): #actuall path in computer mening wrpPath style

    parser = Parser(path_to_old_wrp)

    parsed_path  = pathToChangedFile.split('/')
    #Collect old and new file name
    old_file_name = pathToChangedFile.split('/')[-1]
    new_file_name = NewVersionName(pathToChangedFile)
    #print('Old file name:' + old_file_name)
    #print('New file name:' + new_file_name)
    # marks if there were any directort in path if not default to non
    marker = 0

    # get all possible directories from the old wrapper
    # OBS need to get Wrp path
    possible_directories = parser.find_all_directories(path_to_old_wrp)

    for dir in possible_directories:
        if dir in parsed_path:
            target_directory = dir
            marker = 1
            break
    if marker == 0 :
        target_directory = 'non'
    #print('Target: ' + target_directory)
    # False at start since we have not yet enterd any directory,
    # if target_directory == non it is fine
    in_right_directory = False

    path_to_new_wrp = new_wrp_path(path_to_old_wrp, new_wrp_name)
    #print('New path: ' + path_to_new_wrp)
    with open(path_to_old_wrp, 'r') as old_wrapper:
        with open(path_to_new_wrp , 'w+') as new_wrapper:

            for line in old_wrapper:
                # if target_directory is non
                if target_directory == 'non':
                    if line.strip() == old_file_name.strip():
                        new_wrapper.write(new_file_name)
                    else:
                        new_wrapper.write(line)
                # if target_directory != non
                else:
                    l = line.lower().strip()
                    if l.startswith('default_dir'):
                        if line.split()[1] == target_directory:
                            in_right_directory = True
                        else:
                            in_right_directory = False
                    #if in_right_directory is True:
                        #print(line)
                        #print(old_file_name)
                    #if line.endswith(target_directory):
                    #if line.find(target_directory) != -1:
                    #    in_right_directory= True
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

def new_wrp_path(old_wrp_path, new_wrp_name):
    splits = old_wrp_path.split('/')
    splits[-1] = new_wrp_name
    return '/'.join(splits)

# DEBUG Function
def print_wrapper_file(pathToWrp):
    with open(pathToWrp, 'r') as wrp :
        for line in wrp:
            print(line)

def test():
    old= '../../Files/10JAN04XK/10JAN04XK_V005_iGSFC_kall.wrp'
    new= '10JAN04XK_V005_iGSFC_kall_testa.wrp'
    new_path = '../../Files/10JAN04XK/10JAN04XK_V005_iGSFC_kall_testa.wrp'
    file = '../../Files/10JAN04XK/10JAN04XK/WETTZELL/Met.nc'
    create_new_wrapper(file, old, new)
    #print_wrapper_file(new_path)
    #print_wrapper_file(old)
    equal(old, new_path)
