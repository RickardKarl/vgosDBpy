from wrapper import Wrapper
from os import getcwd
import sys
import pprint
pp = pprint.PrettyPrinter()

wrapper_path = getcwd() + '/' + sys.argv[1]

class Parser:
    def __init__(self):
        self.wrapper = Wrapper(getcwd())
        self.active_scope = []


    def getActiveScope(self):
        if len(self.active_scope) == 0:
            return None
        else:
            return self.active_scope[-1]

    def addScope(self, scope):
        self.active_scope.append(scope)

    def removeScope(self, scope):
        self.active_scope.remove(scope)

    def parseWrapper(self,path):
        active_folder = None
        active_scope = self.getActiveScope()

        with open(path,'r') as src:
            for line in src:
                if line.startswith('!'):
                    continue
                elif line.startswith('Begin'):
                    keyword = line.split()[1].rstrip()
                    self.addScope(keyword)
                    if keyword not in Wrapper.scopes:
                        continue
                    else:
                        active_scope = self.getActiveScope()

                elif line.startswith('End'):
                    keyword = line.split()[1].rstrip()
                    self.removeScope(keyword)

                elif line.startswith('Default_dir'):
                    active_folder = line.split()[1].rstrip()
                    if active_folder not in Wrapper.scopes:
                        self.wrapper.addFolder(active_folder, active_scope)

                elif line.endswith('.nc'):
                    file_name = line.split()[-1].rstrip()
                    self.wrapper.addFile(file_name, active_scope, active_folder)


        return self.wrapper


if __name__ == "__main__":
    p = Parser()
    w = p.parseWrapper(wrapper_path)
    print(w)
