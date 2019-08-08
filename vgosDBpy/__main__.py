# Main method
import sys
from PySide2.QtWidgets import QApplication
from netCDF4 import Dataset
from vgosDBpy.view.app import App
from vgosDBpy.read_log.plotter import plotSeries
from vgosDBpy.script_driven.argparser import CommandLineInterface

#Hanna
from vgosDBpy.data.netCDFdebug import print_name_dtype_dim_length, get_dimensions
#sfrom vgosDBpy.data.readNetCDF import #getDataFromVar_multDim,#get_dataBaseline
from vgosDBpy.editing.createWrapper import test
from vgosDBpy.script_driven.script_main import script_class


if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1] == 'Hanna':

            #path = "./../../Files/10JAN04XK/ObsDerived/Cal-SlantPathIonoGroup_bX.nc"
            #path = "./../../Files/10JAN04XU/Session/GroupBLWeights.nc"
            #path = "../../Files/10JAN04XK/10JAN04XK_V005_iGSFC_kall.wrp"
            #path = "./../../Files/10JAN04XU/Head.nc"
            #path = "./../../Files/10JAN04XK/Observables/QualityCode_bS.nc"
            #path2 = "./../../Files/10JAN04XK/Observables/QualityCode_bX.nc"

            #path = "./../../Files/10JAN04XK/TSUKUB32/Part-HorizonGrad_kNMF.nc"
            #path = "./../../Files/10JAN04XK/Observables/Source.nc"
            #path = "./../../Files/10JAN04XK/TSUKUB32/AzEl.nc"
            #path2 = './../../Files/10JAN04XK/TSUKUB32/Part-AxisOffset.nc'
            #path =  './../../Files/10JAN04XK/Apriori/Station.nc'
            #path = './../../Files/10JAN04XK/CrossReference/ObsCrossRef.nc'
            #path = "./../../Files/10JAN04XK/Scan/ERPApriori.nc"

            """
            print_name_dtype_dim_length(path)


            #t= get_dataBaseline(path)
            with Dataset(path, 'r', format = 'NETCDF4_CLASSIC') as nc:
                vars = nc.variables
                for var in vars:
                    print(var+ ':')
                    dimension = nc.variables[var].get_dims()
                    try:
                        print(nc.variables[var].Units)
                    except:
                        print('--')
                    print('lengtht of dims')
                    print(len(dimension))
                    dtypes = nc.variables[var].dtype
                    for dim in dimension:
                        print('.    '+ dim.name)
            """
            path = './../../Files/format_script.txt'
            with open(path , 'w+') as txt:
                txt.write('begin table\n')
                txt.write('./../../Files/10JAN04XK/TSUKUB32/Met.nc -- AtmPres\n')
                txt.write('./../../Files/10JAN04XK/TSUKUB32/Met.nc -- TempC\n')
                txt.write('end table\n')
                txt.write('begin plot\n')
                txt.write('./../../Files/10JAN04XK/TSUKUB32/Met.nc -- AtmPres\n')
                txt.write('./../../Files/10JAN04XK/TSUKUB32/Met.nc -- TempC\n')
                txt.write('end plot')
            #script(path)
            """
            print_name_dtype_dim_length(path2)
            with Dataset(path2, 'r', format = 'NETCDF4_CLASSIC') as nc:
                vars = nc.variables
                for var in vars:
                    print(var+ ':')
                    dimension = nc.variables[var].get_dims()
                    print('lengtht of dims')
                    print(len(dimension))
                    dtypes = nc.variables[var].dtype
                    for dim in dimension:
                        print('.    '+ dim.name)
            """
            #find_dimensions(path)
            #getDataFromVar_multDim(path,'obs2Scan')
            #print(read_netCDF_data_info(path))
            #print(get_constants(path))
            #create_new_wrapper(path)
            #path = '../../Files/10JAN04XK/10JAN04XK_V005_iGSFC_kall.wrp'
            #print_wrapper_file(path)
            #test()
        else:
            interface = CommandLineInterface()

    else:
        interface = CommandLineInterface()
