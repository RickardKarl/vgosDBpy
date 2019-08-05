from vgosDBpy.editing.createNetCDF import create_netCDF_file
from vgosDBpy.editing.createWrapper import create_new_wrapper

import os
from datetime import datetime

class EditTracking:

    '''
    Keep track of changes in data
    Allows us to display them and save them in new files
    '''

    def __init__(self, wrapper):
        self._edited_variables = []
        self._edited_data = {}
        self._wrapper = wrapper

    ############# Getters & setters

    def getEditedData(self):
        return self._edited_data

    def getEditedVariables(self):
        return self._edited_variables

    def addEdit(self, variable, data_array):
        '''
        Add or update an edited data array for the corresponding variable

        variable [model.standardtree.Variable]
        data_array [numpy array] is the edited data
        '''
        if not variable in set(self._edited_variables):
            self._edited_variables.append(variable)
        self._edited_data[variable] = data_array

        print('Current changes:')
        for var in self._edited_variables:
            print(var.getPath())

    def removeEdit(self, variable):
        '''
        variable [model.standardtree.Variable]
        '''
        if variable in self._edited_data:
            self._edited_data.pop(variable)
            self._edited_variables.pop(variable)
        else:
            raise ValueError('Variable is not listed in the object:', self)

    def reset(self):
        self._edited_variables = []
        self._edited_data = {}

    ########### Methods for saving edits

    def saveEdit(self):
        '''
        Saves the changes made in the edited variables
        Creates new netCDF files and a wrapper that points to the new file(s)
        Also creates a new history file
        '''
        sort_by_parent = {}
        for variable in self._edited_variables:
            # Get parent of variable and check if it is a netCDF file
            parent = variable.getNode()
            if parent.isNetCDF():
                # Check if this is a new parent or if it is shared with some other variable
                if parent in sort_by_parent:
                    sort_by_parent.get(parent).append(variable)
                else:
                    sort_by_parent[parent] = [variable]
            else:
                raise ValueError('Can not find netCDF that variable belongs to', variable)

        path_to_file_list = [] # Saves path to the file that is replaced
        new_file_name_list = [] # Saves name of all newly created files

        for parent_key in sort_by_parent:
            # Get variables that belongs to the same parent
            var_list = sort_by_parent.get(parent_key)
            # Create temporary dict for these variables
            edited_variables = {}

            # Add these variables to the dict
            for var_item in var_list:
                edited_variables[str(var_item)] = self._edited_data.get(var_item)

            # Get netCDF path of the parent (which is a netCDF file, it has been checked)
            netCDF_path = parent_key.getPath()

            new_file_path = create_netCDF_file(netCDF_path, edited_variables)
            new_file_name = new_file_path.split('/')[-1]

            path_to_file_list.append(parent_key.getPath())
            new_file_name_list.append(new_file_name)

        print(path_to_file_list)
        print('Created the following files:', new_file_name_list)

        # Create new history file and add it to the wrapper changes
        new_hist_path, timestamp = self.createNewHistFile(sort_by_parent, path_to_file_list, new_file_name_list)
        hist_file_name = new_hist_path.split('/')[-1]

        # Create new wrapper
        new_wrp_path = create_new_wrapper(path_to_file_list, new_file_name_list, self._wrapper.wrapper_path,
                            hist_file_name, timestamp)

        print('Created the following wrapper:', new_wrp_path)
        print('Created the following history file:', new_hist_path)



    def createNewHistFile(self, sort_var_by_file, path_to_file_list, new_file_name_list):
        '''
        Create a new .hist-file

        Returns path to new history file
        '''

        # Get folders
        folder = []
        for path in path_to_file_list:
            f = path.split('/')[-2]
            folder.append(f)

        # Getting timestamp of creation of file
        timestamp = datetime.now()

        # Generate new path
        session_name = self._wrapper.session_name
        new_hist_path = self._wrapper.getNode('History').getPath() + '/' + session_name + '_vgosDBpy_V' + timestamp.strftime('%Y%m%d%H%M%S') + '.hist'


        # Check if it exists already so it wont overwrite anything
        if os.path.isfile(new_hist_path):
            raise ValueError('File', new_hist_path,'already exists. Can not overwrite it.')

        # Creating and writing to the new files with the tracked changes
        with open(new_hist_path,'w') as dest:
            str_line = 'The following changes were made ' + timestamp.strftime('%Y-%m-%d %H:%M:%S') + '\n'
            dest.write(str_line)

            file_index = 0
            for old_file in sort_var_by_file:
                str_line = 'Made changes to ' + str(old_file) + ' in ' + folder[file_index] + ', which are saved in ' + new_file_name_list[file_index] + '\n'
                dest.write(str_line)
                file_index += 1
                for var in sort_var_by_file.get(old_file):
                    str_line = '    Variable ' + str(var) + ' was edited.\n'
                    dest.write(str_line)

        ####### Returns path to the new .hist file
        return new_hist_path, timestamp
