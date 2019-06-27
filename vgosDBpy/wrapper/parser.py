
from os import getcwd
import sys
import pprint
import importlib
pp = pprint.PrettyPrinter()

def import_func(file, path):
    spec = importlib.util.spec_from_file_location(file, path)
    pack = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pack)
    return pack

Wrapper = import_func('tree', '/Users/rickardkarlsson/Documents/NVI/vgosDBpy-git/vgosDBpy/wrapper/tree.py').Wrapper
#wrapper_path = getcwd() + '/' + sys.argv[1]

class Parser:
    '''
    Class for parsing wrapper files (*.wrp) in vgosDB format
    '''

    # Constructor
    def __init__(self, root_path = getcwd()):
        self.wrapper = Wrapper(root_path)
        self._active_scope = []

    ##################################################
    # Methods which keep track of the current scope in the wrapper_path
    # Represented as a queue which keeps the most recent mentioned scope
    # Scopes are defined in wrapper.py

    def getActiveScope(self):
        if len(self._active_scope) == 0:
            return None
        else:
            for i in range(len(self._active_scope)):
                if Wrapper.inScope(self._active_scope[-1-i]):
                    return self._active_scope[-1-i]
            return None

    def addScope(self, scope):
        self._active_scope.append(scope)

    def removeScope(self, scope):
        self._active_scope.remove(scope)

    ##################################################


    def getWrapperRoot(self):
        return self.wrapper.getRoot()

    def parseWrapper(self,path):
        '''
        Methods that parses the wrapper files which contains information and
        pointers to relevant files in one VLBI session

        path [string] is the path to the wrapper file (*.wrp)
        '''
        # Define current folder, None if the wrapper has no default_dir
        active_folder = None

        # Open file
        with open(path,'r') as src:

            # Loop through each file
            for line in src:

                # Correct format of line
                line = line.lower().strip()

                # Skip comments in wrapper
                if line.startswith('!'):
                    continue

                # Check for beginning of sections
                elif line.startswith('begin'):
                    keyword = line.split()[1]
                    self.addScope(keyword)

                # Check for end of sections
                elif line.startswith('end'):
                    keyword = line.split()[1]
                    self.removeScope(keyword)
                    active_folder = None

                # Check for setting the default_dir (active_folder)
                elif line.startswith('default_dir'):
                    active_folder = line.split()[1]
                    if not Wrapper.inScope(active_folder):
                        self.wrapper.addNode(active_folder, self.getActiveScope(), 'folder')

                # Checks if line is giving a netCDF pointer
                elif line.endswith('.nc'):
                    #print(line)
                    file_name = line.split()[-1]
                    self.wrapper.addNode(file_name, active_folder, 'netCDF')
                else:
                    pass
                    #print(line) # For debugging
        return self.wrapper


if __name__ == "__main__":
    p = Parser()
    w = p.parseWrapper(wrapper_path)