
"""
In this file there are methods and other to prepare for plotting and tabular show.
It takes in a map where keys that are variable paths, meaning they cointain the path and the variable name.
"""

def checkLength(map):
    pastLength = -1
  for itm in list(map):
      length = len(map[itm])
      if pastLength is not -1:
          if length != pastLength:
              return False
          else:
              pastLength = length
    return True

def checkNbrOfArrays(map):
    if len(list(map)) <= 3 or len(list(map)) >= 2:
        return True
    else:
        return False
