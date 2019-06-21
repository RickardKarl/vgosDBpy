def ncDump(key):
    from netCDF4 import Dataset
    try:
        file = Dataset(key,"r",format="NETCDF4_CLASSIC")
    except KeyError:
            print("key not valid")


    f= open("TOC.txt","w+")
    #Global atributes
    nc_attrs = file.ncattrs()
    f.write("Global Attributes:\n")
    if len(nc_attrs) != 0:
        for attr in nc_attrs:
            f.write( "   %s:" % attr + repr(nc_fid.getncattr(attr) ) + "\n" )
    else:
        f.write(" No Global Attributes\n")

    #Dimension
    f.write("\nDimensions:\n")
    dimensions = file.dimensions
    for dim in dimensions:
        str=dim
        f.write(" Name:" + dim)
        f.write("        Value: %s \n" %len(file.dimensions[dim]) )

        #print(file.dimensions[str].value)

    #Variables
    variables = file.variables
    f.write("\nVariables:\n")
    for keys in variables:
        str = keys
        f.write(" Name:" + str+"\n")
        f.write("        Type: %s\n" % (file.variables[str].dtype) )
        f.write("        Dimensions %s\n"%(file.variables[str].dimensions))
        f.write("        Size: %s \n" %(file.variables[str].size) )
