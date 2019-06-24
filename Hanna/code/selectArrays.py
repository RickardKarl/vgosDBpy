
import cmd, sys
from turtle import *

test = {"hej":2, "heej":3, "heeej":4}

def select_arrays(map):
    print(list(map))
    done=0
    while done is not 1:
        var = input("\nPlease type two or three of the names, seperate by blank space: \n")
        count = var.count(" ")

        if count == 1:
            key1, key2 = var.split(" ")
            if key1 not in map or key2 not in map:
                print("You choose names that were not in list, please try again\n")
            else:
                if key1 == key2:
                    print("You chose tha same array twice, please try again\n")
                else:
                    return map[key1], map[key2]
        elif count == 2 :
            key1, key2, key3 = var.split(" ")
            if key1 not in map or key2 not in map or key3 not in map:
                print("You choose names that were not in list, please try again\n")
            else:
                if key1 == key2 or key1 == key3 or key2 == key3:
                    print("You choose the same name several times, please try again\n")
                else:
                    return map[key1], map[key2], map[key3]
        else:
            print("Something went wrong, please try again")

select_arrays(test)
