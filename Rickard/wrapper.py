



class Wrapper:

    scopes = ['Session','Scan', 'Observation', 'Station']

    def __init__(self, root_path):

        self.root_path = root_path
        self.root = Node('root', None)

        for s in Wrapper.scopes:
            self.root.addChildNode(Node(s, self.root))

    def addFile(self, name, scope = None, parent = None):

        if scope == None or parent == None:
            self.root.addChildNode(NetCDF_File(name, self.root))

        else:
            scope_folder = self.root.returnName(scope)
            if parent in self.scopes:
                scope_folder.addChildNode(NetCDF_File(name, scope))
            else:
                scope_folder.returnName(parent).addChildNode(NetCDF_File(name, parent))

    def addFolder(self, name, scope = None):
        if scope == None:
            self.root.addChildNode(Node(name, self.root))
        else:
            self.root.returnName(scope).addChildNode(Node(name, scope))

    def returnRoot(self):
        return self.root

    def __str__(self):
        return str(self.root.getChildren())




### Tree structure

class Node(object):

    def __init__(self, name, parent):
        self.name = name
        self.children = []
        self.parent = parent

    def addChildNode(self, obj):
        if self.nameExists(obj):
            self.children.append(obj)

    def getParent(self):
        return self.parent

    def getChildren(self):
        return self.children

    def returnName(self, name):
        for obj in self.getChildren():
            if obj.compareName(name):
                return obj
        raise AttributeError(name + ' was not found in the ' + str(self) + ' folder')

    def compareName(self, name):
        return self.name == name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class NetCDF_File(Node):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.children = None

    def addChildNode(self, obj):
        raise TypeError('Tried assigning files to another file, needs to be a folder.')




if __name__ == "__main__":
    t = Wrapper('h')
    scope = 'Scan'
    t.addFile('h', parent = scope, scope = scope)
    print(t)
