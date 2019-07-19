from vgosDBpy.editing.editNetCDF import create_netCDF_file
from vgosDBpy.editing.createNewWrp import create_new_wrapper

class EditTracking:

    '''
    Keep track of changes in data
    Allows us to display them and save them in new files
    '''

    def __init__(self, wrapper_path):

        self._edited_variables = []
        self._edited_data = {}
        self._wrapper_path = wrapper_path

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

    def saveEdit(self):
        '''
        Saves the changes made in the edited variables
        Creates new netCDF files and a wrapper

        NEED TO CREATE A NEW WRAPPER
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

        for parent_key in sort_by_parent:
            # Get variables that belongs to the same parent
            var_list = sort_by_parent.get(parent_key)
            # Create temporary dict for these variables
            edited_variables = {}

            # Add these variables to the dict
            for var_item in var_list:
                edited_variables[var_item] = self._edited_data.get(var_item)

            # Get netCDF path of the parent (which is a netCDF file, it has been checked)
            netCDF_path = parent_key.getPath()

            create_netCDF_file(netCDF_path, edited_variables)
            path_to_var_list = []
            for var in var_list:
                path_to_var_list.append(var.getPath())
            print(path_to_var_list)
            create_new_wrapper(path_to_var_list, self._wrapper_path, 'new_wrapper_1')
