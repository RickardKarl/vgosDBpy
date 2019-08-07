"""
EX:
begin plot
pathToNetCDF -- var
pathToNetCDF --  var
end plot

begin table
pathToNetCDF -- var
pathToNetCDF -- var
end table
"""

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from vgosDBpy.data.plotFunctionNew import Plotfunction_class


from vgosDBpy.data.plotTable import Tablefunction
from vgosDBpy.data.tableToASCII import convertToAscii_script

from vgosDBpy.editing.newFileNames import new_netCDF_name


def script(path):

    plot_list, table_list = parse_script(path)

    for plot in plot_list:
        script_plot(plot)
    for table in table_list:
        script_table(table)


def parse_script(path):

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
    # call on functions to create plots and tables

def script_plot(list):

    plt_function = Plotfunction_class()

    paths = []
    vars = []

    for itm in list:
        fig  = plt.figure()

        path, var = itm.split('--')
        paths.append(path.strip())
        vars.append(var.strip())

    ex_name = './plot'
    new_name = new_netCDF_name(ex_name)

    axis, data = plt_function.plotFunction(paths,vars,fig,-1)
    plt.savefig(new_name)

def script_table(list):
    table_function = Tablefunction()

    paths = []
    vars = []

    for itm in list:
        path, var = itm.split('--')
        paths.append(path.strip())
        vars.append(var.strip())

    ex_name = './table.txt'
    new_name = new_netCDF_name(ex_name)
    info = ''

    directory = table_function.tableFunctionGeneral(paths,vars)
    convertToAscii_script(directory, info, new_name)
