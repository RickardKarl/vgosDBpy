"""
EX:
begin plot
pathToNetCDF var
pathToNetCDF var
end plot

begin table
pathToNetCDF & var
pathToNetCDF & var
end table
"""

from matplotlib.figure import Figure

from vgosDBpy.view.plot_widget_new import PlotFigure

def script(path):
    print('in script')

    plot_list = []
    table_list = []
    # Parse the string
    plot= False
    table = False

    with open(path, 'r') as txt:
        for line in txt:
            l= str(line).lower().strip()
            if l  ==  'begin plot':
                print(line + '1')
                plot = True
                temp_plot_list = []
            elif l == 'end plot':
                print(line + '2')
                plot_list.append(temp_plot_list)
                temp_plot_list = []
                plot = False
            elif l == 'begin table' :
                print(line + '3')
                table = True
                temp_table_list = []
            elif l == 'end table':
                print(line + '4')
                table = False
                table_list.append(temp_table_list)
                temp_table_list = []
            elif plot == True:
                print(line + '5')
                temp_plot_list.append(line)
            elif table == True:
                print(line + '6')
                temp_table_list.append(line)

    # call on functions to create plots and tables
    for plot in plot_list:
        print('plot create')
        script_plot(plot)
    for table in table_list:
        script_table(table)

def script_plot(list):
    print('in script_plot')
    plot_figure = PlotFigure(parent=None)

    paths = []
    vars = []
    for itm in list:
        path, var = itm.split('&')
        print(path)
        print(var)
        path = path.strip()
        var = var.strip()
        paths.append(path)
        print('added')
        print(paths[-1])
        vars.append(var)

    fig  = Figure(tight_layout = True)
    i=0
    for path in paths:
        print(path)
        #axis, data = plot_function.plotFunction(paths[i],vars[i])
        plot_figure.plot_script(paths,vars,fig, -1)
        i += 1
        plot_figure.saveCanvas('hannas_bild.png')




def table_script(list):
    paths = []
    vars = []
    for itm in list:
        path, var = itm.split('&')
        paths.append(path.strip())
        vars.append(var.strip())
