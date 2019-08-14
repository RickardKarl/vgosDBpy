##  data_axis.py:
###### DataAxis
Stores a *matplotlib.Axis*, the corresponding data in *pandas.Series* and a *Variable* instance from standardtree.py
Might actually be a better idea to overwrite *matplotlib.Axis* with this one? It basically acts as one, but it keep track of changes.

Should do more internal stuff such as automatically create a new line with the edited data.
Move edited_curve variable to this one?

## qtree.py (Qt-dependent)

This file contains the data structure needed to store the data in a model as required by QT,
it basically copies another data structure that is used when reading the wrapper.
The item classes are also used by the table models that are QT-based in table.py.

###### TreeModel (Inherits from QStandardItemModel)
Tree structure model that is used to represent the wrapper internally.
Makes calls to the wrapper-folder that parses the wrapper, it reads another tree structure and
copies nodes from another tree structure (*Wrapper* class in tree.py) that contains the
needed information.

###### QNodeItem (Inherits from QStandardItem)
Node class that is used in *TreeModel*. This node points to another node (*Node* in tree.py)
which contains all the information about a file/folder or similar.


###### NetCDFItem (Inherits from QNodeItem)
A version of QNodeItem for nodes that points to a netCDF-file (.nc)


###### Variable (Inherits from QNodeItem)
A version of QNodeItem for nodes that points to a variable that is saved in a netCDF-file


###### DataValue (Inherits from QNodeItem)
A version of QNodeItem for nodes that points to one data_point contained in each variable.


## table.py (Qt-dependent)

###### TableModel (Inherits from QStandardItemModel)
Qt-model for all of the tables used in the interface.

###### VariableModel (Inherits from TableModel)
Qt-model to store variables from a netCDF file in a table

###### DataModel (Inherits from TableModel)
Qt-model to store data values from a netCDF variable in a table
