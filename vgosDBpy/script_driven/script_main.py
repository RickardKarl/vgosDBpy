"""
FORMAT FOR .TXT FILE INPUT:
begin plot
pathToNetCDF -- var_1 -- var_2 -- ... -- var_n
pathToNetCDF --  var
end plot

begin table
pathToNetCDF -- var
pathToNetCDF -- var
end table
"""

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from vgosDBpy.data.plotFunction import Plotfunction_class


from vgosDBpy.data.plotTable import Tablefunction
from vgosDBpy.data.tableToASCII import convertToAscii_script

from vgosDBpy.editing.newFileNames import new_netCDF_name

# function that is called from outisde, takes in a path to a txt file with info of what to do.
def script(path):

    plot_list, table_list = _parse_script(path)

    for plot in plot_list:
        _script_plot(plot)
    for table in table_list:
        _script_table(table)

# private function that parses the .txt file and creates a list of things to plot and put in tables
def _parse_script(path):

    plot_list = []
    table_list = []

    plot= False
    table = False

    with open(path, 'r') as txt:
        for line in txt:
            l= str(line).lower().strip()
            if l  ==  'begin plot':
                plot = True
                temp_plot_list = []
            elif l == 'end plot':
                plot_list.append(temp_plot_list)
                plot = False
            elif l == 'begin table' :
                table = True
                temp_table_list = []
            elif l == 'end table':
                table = False
                table_list.append(temp_table_list)
            elif plot == True:
                temp_plot_list.append(line)
            elif table == True:
                temp_table_list.append(line)

    return plot_list, table_list


# private function that takes in a list of strings in the form 'path' -- 'var', loopse though the list and creates and saves the
#plots
def _script_plot(list):

    plt_function = Plotfunction_class()

    paths = []
    vars = []

    for itm in list:
        fig  = plt.figure()

        line = itm.split('--')
        path = line[0].strip()
        # adds all variables in the netCDF file to the list
        for i in range(1,len(line)):
            paths.append(path)
            vars.append(line[i].strip())

    ex_name = './plot.png'
    new_name = new_netCDF_name(ex_name)

    axis, data = plt_function.plotFunction(paths,vars,fig,-1)
    plt.savefig(new_name)

## private function that takes in a list of strings in the form 'path' -- 'var',
# loopse though the list and creates and saves the
# tables with the content of the varibales
def _script_table(list):
    table_function = Tablefunction()

    paths = []
    vars = []

    for itm in list:
        line = itm.split('--')
        # adds all variables in the netCDF file to the list
        for i in range(1,len(line)):
            paths.append(line[0].strip())
            vars.append(line[i].strip())

    ex_name = './table.txt'
    new_name = new_netCDF_name(ex_name)
    info = ''

    directory = table_function.tableFunctionGeneral(paths,vars)
    convertToAscii_script(directory, info, new_name)
