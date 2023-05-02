
def Rewrite(OCif, ModifiedCif):
    "This function takes the original cif and modifies/fixes to meet crystIT standards to get information theory data"
    
    # Open a new cif and split line by line
    newCif = open(ModifiedCif, "w")
    SplitCif = OCif.split("\n")
    
    # Write the standard formatting for a cif, required for crystIT
    newCif.write("#\n")
    newCif.write(SplitCif[1])                                                  
    newCif.write("\n")
    newCif.write("loop_\n")                                                    
    newCif.write("_citation_author_citation_id\n")
    newCif.write("_citation_author_name\n")
    newCif.write("primary ''\n")
    # Author field left as null to prevent any errors
    
    # Loop across the split cif to write the old data into the new cif
    CoordFlag = 0; ParameterFlag = 0                                           
    for i in range(0, len(SplitCif)):
        
        # Coordinate data
        if CoordFlag == 1 and SplitCif[i] != "loop_":                          
            newCif.write(SplitCif[i])                                          
            newCif.write("\n")
        elif CoordFlag == 1 and SplitCif[i] == "loop_":
            CoordFlag = 0                                                      
        if SplitCif[i] == "_atom_site_label":
            CoordFlag = 1
            newCif.write("loop_")
            newCif.write("\n")
            newCif.write(SplitCif[i])                                          
            newCif.write("\n")
        
        # Cell parameter / infomation data
        if SplitCif[i].split(" ")[0] == "_cell_length_a":                      
            ParameterFlag = 1
            newCif.write(SplitCif[i])
            newCif.write("\n")
        if ParameterFlag == 1 and SplitCif[i] != "loop_":
            newCif.write(SplitCif[i])
            newCif.write("\n")
        if ParameterFlag == 1 and SplitCif[i] == "loop_":
            ParameterFlag = 0
    
    # Write the last line and close to save
    newCif.write("#")
    newCif.close()

"------------------------------------------------------------------------------"

# Loop across the downloaded cifs from FetchCifs
for i in range(1, 10000000):
    cif = ""
    
    # Copy original cif to a string
    CifFile = "cifs/icsd_" + str(i).zfill(6) + ".cif" 
    try:
        OldCif = open(CifFile, "r")
        for line in OldCif:
            cif += str(line)
        
        # Path for new cif
        newCifFile = "modcifs/icsd_" + str(i).zfill(6) + ".cif" 
        Rewrite(cif, newCifFile)
    # In case there is no cif with this number
    except:
        pass