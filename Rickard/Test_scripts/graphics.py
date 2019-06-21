
import netCDF4
from os import listdir
from os.path import isfile, join

session = '10JAN14XE'
path = '../../../Data/' + session + '/'
wrp_file1 = session + '_V005_iGSFC_kall.wrp'
wrp_file2 = session + '_V005_iGSFC_kngs.wrp'

wrapper1 = open(path+wrp_file1,'r')
wrapper2 = open(path+wrp_file2,'r')

stations_dir = {}
stations = []
for line in wrapper1:
    if line.startswith('Begin Station'):
        station_name = line.split(' ')[2].rstrip()
        stations.append(station_name)
        stations_dir[station_name] = [f for f in listdir(path + station_name + '/') if isfile(join(path + station_name + '/', f))]





import tkinter as tk
from tkinter.ttk import Treeview


root = tk.Tk()
tree = Treeview(root)

# Define columns
tree["columns"]=("one")
tree.column("#0", width=270, minwidth=270)# stretch=tk.NO)
tree.column("one", width=150, minwidth=150) #stretch=tk.NO)

# Define hedaings
tree.heading("#0",text="Name",anchor=tk.W)
tree.heading("one", text="Type",anchor=tk.W)
print(stations)
stations_folder = []
count = 1
for station in stations:
    print(station)
    parent = ', ' + str(count) + ','
    stations_folder.append(tree.insert(parent, text=station, values=("File folder"), index = count))
    count += 1

tree.pack(side=tk.TOP,fill=tk.X)

root.mainloop()
