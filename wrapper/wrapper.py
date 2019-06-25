
'''
TODO:

Introduce netCDF reading so that arrays are another type of Node

There is a problem with the pointer_map when files have the same name,
have not seen any consequences yet but reduces generality
'''


class Wrapper:
    '''
    Class for representing a wrapper in a tree data structure
    '''

    # Pre-defined scopes will have the folder made automatically
    scopes = ['session','scan', 'observation', 'station']

    def __init__(self, root_path):
        '''
        Constructor

        root_path [string] is the path to the root folder
        '''
        self.root_path = root_path
        self.root = Node('root', None, root_path)
        self.pointer_map = {} # Keep track of pointers with a hash-map

        for s in Wrapper.scopes:
            self.addNode(s, type = 'folder')


    def addNode(self, name, parent = None, type = 'netCDF'):
        '''
        Add node in the tree, may be a file, data array or a folder

        name [string] is the node's name
        parent [string] is the name of the parent, if None then
        it have root as parent
        type [string] is the type of node, currently there exist 'folder' or 'netCDF'
        '''

        if parent == None:
            parent_node = self.root
        else:
            parent_node = self.getNode(parent)

        path = self.generatePath(name, parent_node)

        if type == 'folder':
            new_node = Node(name, parent_node, path)
        elif type == 'netCDF':
            new_node = NetCDF_File(name, parent_node, path)
        else:
            raise InvalidArgument('Invalid type in', type)
        parent_node.addChildNode(new_node)
        self.addPointer(new_node)

    def addPointer(self, node):
        '''
        Set new pointers

        node [Node] is the node to point to
        '''
        self.pointer_map[node.getName()] = node

    def getNode(self, name):
        '''
        Get a node by using the map of pointers

        name [string] is the name of the desired node
        '''
        return self.pointer_map[name]

    def getRoot(self):
        '''
        Returns the root node
        '''
        return self.root

    def inScope(name):
        '''
        Checks if a name is defined in the scopes

        name [string]
        '''
        return name in Wrapper.scopes

    def generatePath(self, name, parent):
        '''
        Return file path to a desired node with the given name

        name [string]
        parent [Node]
        '''

        if name == 'root':
            return self.root_path
        elif parent is self.root:
            return self.root_path + '/' + name
        else:
            path = name
            while parent is not self.root:
                path = str(parent) + '/' + path
                node = parent
                parent = node.getParent()
            return self.root_path + '/' + path


    def __str__(self):
        indent = " " * 4
        s = ''
        for child in self.root.getChildren():
            line = str(child).upper() + '\n'
            s = s + line
            if type(child) == Node:
                for sub_child in child.getChildren():
                    s = s + indent + str(sub_child).capitalize() + '\n'
                    if type(sub_child) == Node:
                        for subsub_child in sub_child.getChildren():
                            s = s + indent*2 + str(subsub_child.getPath()) + '\n'
        return s


### Tree structure
class Node(object):
    '''
    Defining a Node class for the tree data structure
    '''

    def __init__(self, name, parent, path):
        '''
        name [string]
        parent [string]
        '''
        self.name = name
        self.children = []
        self.parent = parent
        self.path = path


    def addChildNode(self, node):
        '''
        Add another node as a child to the current node

        node [Node]
        '''
        if self.childNodeExists(node) == False:
            self.children.append(node)

    def getParent(self):
        '''
        Returns parent to the current node [Node]
        '''
        return self.parent

    def getChildren(self):
        '''
        Returns list of children to the current node [list of Nodes]
        '''
        return self.children

    def returnChildNode(self, name):
        '''
        Returns a child node with the desired name

        name [string]

        Raises error if name not found
        '''
        for obj in self.getChildren():
            if obj.compareName(name):
                return obj
        raise AttributeError(name + ' was not found in the ' + str(self) + ' folder')

    def getName(self):
        '''
        Return name of current node [string]
        '''
        return self.name

    def getPath(self):
        return self.path

    def childNodeExists(self, name):
        '''
        Returns True if a childnode with the desired name exists
        Otherwise False

        name [string]
        '''
        for obj in self.getChildren():
            if obj.compareName(name):
                return True
        return False

    def compareName(self, name):
        '''
        Checks if a given name is equal to the name of the current node

        name [string]
        '''
        return self.name == str(name)


    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name



class NetCDF_File(Node):

    def __init__(self, name, parent, path):
        super().__init__(name, parent, path)
        self.children = None

    def addChildNode(self, obj):
        raise TypeError('Tried assigning files to another file, needs to be a folder.')


if __name__ == "__main__":
    print('Hello world!')
