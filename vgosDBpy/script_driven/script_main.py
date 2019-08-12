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
from vgosDBpy.data.getName import create_wrp_path, createFullPath


from vgosDBpy.data.plotTable import Tablefunction
from vgosDBpy.data.tableToASCII import convertToAscii_script

from vgosDBpy.editing.newFileNames import new_netCDF_name

class script_class():

    def __init__(self):
        self._wrp_path = ''
        self._save_path = '.'
        self._session = ''

    def get_wrp_path(self):
        return self._wrp_path

    def get_save_path(self):
        return self._save_path

    # function that is called from outisde, takes in a path to a txt file with info of what to do.
    def script(self,path):

        plot_list, table_list = self._parse_script(path)

        for plot in plot_list:
            self._script_plot(plot)
        for table in table_list:
            self._script_table(table)

    # private function that parses the .txt file and creates a list of things to plot and put in tables
    def _parse_script(self,path):

        plot_list = []
        table_list = []

        plot= False
        table = False
        wrapper = False
        save_file = False

        with open(path, 'r') as txt:

            for line in txt:

                l= line.lower().strip()
                if l == '!' or l =='':
                    pass
                elif l.startswith('save_at'): # line before giving a new save_path
                    split = line.split(' ')
                    self._save_path = split[1].strip()

                #elif save_file == True:
                #    split = line.split(' ')
                #    self._save_path = split[1]
                #    #save_file= False

                elif l.startswith('new_wrapper'): #line before giving a new wrapper
                    split = line.split(' ')
                    self._wrp_path = split[1].strip()

                #elif wrapper == True:
                #    self._wrp_path = create_wrp_path(line)
                #    wrapper = False

                elif l  ==  'begin_plot':
                    plot = True
                    temp_plot_list = []

                elif l == 'end_plot':
                    plot_list.append(temp_plot_list)
                    plot = False

                elif l == 'begin_table' :
                    table = True
                    temp_table_list = []

                elif l == 'end_table':
                    table = False
                    table_list.append(temp_table_list)

                elif plot == True:
                    words = line.split('--')
                    path = createFullPath(self._wrp_path,words[0])
                    str = path
                    for i in range(1,len(words)):
                        str += '--' + words[i]

                    temp_plot_list.append(str)

                elif table == True:
                    words = line.split('--')
                    path = createFullPath(self._wrp_path,words[0])
                    str = path
                    for i in range(1,len(words)):
                        str += '--' + words[i]

                    temp_table_list.append(str)
                    #temp_table_list.append(createFullPath(self.wrp_path,line))


                else:
                    print('The format of the file is not correct')
                    break
        return plot_list, table_list


    # private function that takes in a list of strings in the form 'path' -- 'var', loopse though the list and creates and saves the
    #plots
    def _script_plot(self,list):

        plt_function = Plotfunction_class()

        paths = []
        vars = []
        for itm in list:
            fig  = plt.figure()

            words = itm.split('--')
            path = words[0].strip()

            #path, var = itm.split('--')
            for i in range(1,len(words)):
                paths.append(path)
                vars.append(words[i].strip())

        ex_name = self._save_path+'/plot.png'
        new_name = new_netCDF_name(ex_name)

        axis, data = plt_function.plotFunction(paths,vars,fig,-1)
        plt.savefig(new_name)

    ## private function that takes in a list of strings in the form 'path' -- 'var',
    # loopse though the list and creates and saves the
    # tables with the content of the varibales
    def _script_table(self,list):
        table_function = Tablefunction()

        paths = []
        vars = []
        for itm in list:
            words = itm.split('--')
            path = words[0].strip()
            for i in range(1,len(words)):
                paths.append(path)
                vars.append(words[i].strip())

        ex_name = self._save_path+'/table.txt'
        new_name = new_netCDF_name(ex_name)
        info = 'Session: ' + self._wrp_path.split('/')[-1].split('_')[0]

        directory = table_function.tableFunctionGeneral(paths,vars)
        convertToAscii_script(directory, info, new_name)
