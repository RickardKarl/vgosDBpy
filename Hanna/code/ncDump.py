def ncDump(key):
    from netCDF4 import Dataset
    pathName= key
    with Dataset(pathName,"r", format="NETCDF4_CLASSIC") as file:

        with open("TOC.txt","w+") as f:
            parts =pathName.split("/")
            nbrSlash = pathName.count("/")
            #for i in range[0,nbrSlash]:
            name = parts[nbrSlash]
            f.write("netCDF "+name+"\n")
            #Global atributes
            nc_attrs = file.ncattrs()
            if len(nc_attrs) != 0:
                f.write("Global Attributes:\n")
                for attr in nc_attrs:
                    f.write("   %s %s:" % attr + repr(nc_fid.getncattr(attr) ) + "\n" )
            #else:
            #    f.write(" No Global Attributes\n")

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
            f.write("\nVarisables:\n")
            for keys in variables:
                #print(i, nc.variables[i].units, nc.variables[i].shape)
                str = keys
                f.write(" Name:" + str+"\n")
                f.write("        Type: %s\n" % (file.variables[str].dtype) )
                f.write("        Dimensions %s\n"%(file.variables[str].dimensions))
                f.write("        Size: %s \n" %(file.variables[str].size) )
