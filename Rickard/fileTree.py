class FileTree:
    '''
    TODO:

    Removing folder and files?

    '''
    root = 'root'

    def __init__(self):
        self._graph = {}
        self._graph[root]

        self._parent_graph = {}
        self._parent_graph[root] = None

    def add_folder(self, folder_name, parent_folder = root):
        self._graph[folder_name] = []
        self._graph[root].append(folder_name)

        self._parent_graph[folder_name] = parent_folder

    def add_file(self, file_name, parent_folder = root):
        self._graph[parent_folder].append(file_name)

        self._parent_graph[file_name] = parent_folder

    def get_content(self, folder_name):
        return self._graph[folder_name]

    def get_parent(self, pointer):
        return self._parent_graph[pointer]

    def get_path_to_file(self, file_name):
        path = ''
        assert file_name != root, 'root is an incorrect file name'
        while file_name != root:
            path = '/'.join(path,file_name)
            file_name = get_parent(file_name)
        return path

t = FileTree()
print(t.root)
t.add_folder('Folder 1')
t.add_folder('Folder 2')
t.add_file('File1', 'Folder 1')
print(get_path_to_file('File1'))
