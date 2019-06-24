from wrapper import Wrapper
from os import getcwd
import sys
import pprint
pp = pprint.PrettyPrinter()

wrapper_path = getcwd() + '/' + sys.argv[1]

class Parser:
    def __init__(self):
        self.wrapper = Wrapper(getcwd())
        self._active_scope = []


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

    def parseWrapper(self,path):
        active_folder = None

        with open(path,'r') as src:
            for line in src:
                line = line.lower().strip('\n')
                if line.startswith('!'):
                    continue

                elif line.startswith('begin'):
                    keyword = line.split()[1]
                    self.addScope(keyword)

                elif line.startswith('end'):
                    keyword = line.split()[1]
                    self.removeScope(keyword)
                    active_folder = None

                elif line.startswith('default_dir'):
                    active_folder = line.split()[1]
                    if not Wrapper.inScope(active_folder):
                        self.wrapper.addFolder(active_folder, self.getActiveScope())

                elif line.endswith('.nc'):
                    file_name = line.split()[-1]
                    self.wrapper.addFile(file_name, self.getActiveScope(), active_folder)

                print(line, active_folder, self.getActiveScope())
        return self.wrapper


if __name__ == "__main__":
    p = Parser()
    w = p.parseWrapper(wrapper_path)
    print(w)
    print('Files in Session:',w.getRoot().returnChildNode('session').getChildren())
