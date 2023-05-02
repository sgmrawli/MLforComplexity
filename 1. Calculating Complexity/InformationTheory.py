import numpy as np
from pymatgen.io.cif import CifParser
from pymatgen.analysis.local_env import CrystalNN
import crystIT
import os.path

def InformationTheory(data, volume, structure):
    "This function is designed to calculate all three information theory parameters from the given structure"
    "This is used as a backup in case crystIT fails due to complications with disorder"
    # V is the number of sites, Ig is information content
    V = 0; Ig = 0; DoF = 0 
    
    # Initialise the nearest neighbour algorithm for degrees of freedom
    nn = CrystalNN()
    
    # Add up all the orbits in the structure
    for ICount in range(0, len(data)):
        V = V + float(data[ICount, 2])
    
    # Loop over all the sites in the structure to sum their information content
    for JCount in range(0, len(data)):
        PI = ((float(data[JCount, 2])) * (float(data[JCount, 6]))) / V
        SumTerm = np.log2(PI) * PI
        Ig = Ig + SumTerm
    
    # Compare expected and calculated coordination numbers to determine any degrees of freedom
    try:
        for S in range(0, len(SPrim)):
            expectedCN = nn.get_cn(SPrim, S)
            calculatedCN = len(nn.get_nn_info(SPrim, S))
            if expectedCN != calculatedCN:
                DoF += 1
    
    # If occupancy is not 1, add a degree of freedom, failsafe if everything breaks
    except:
        if float(data[JCount, 6]) < 1:
            DoF += 1
    
    # Sort out the numbers to match the formulae in paper and return
    Ig = Ig * -1
    IgTot = Ig * V 
    InfDensity = IgTot / volume
    return DoF, Ig, IgTot, InfDensity

def ExtractCif(cif):
    "This function extracts the necessary information for the calculations from the ICSD cif file"
    # Flag for recording coords and an array for storing the coordinate data
    startC = False; fracCoords = []
    
    # Split the cif by line and run through each line
    modcif = cif.split("\n")
    for j in range(0, (len(modcif))):                            
        
        # Failsafe if the cif doesn't have a defined last line
        if startC == True and j == len(modcif)-1:
            startC = False
        
        # When the flag is on, extract the required coordinate data
        if startC == True:
            cifline = modcif[j].split()
            atom = cifline[0]
            fracCoords.append(atom)
            ion = cifline[1]
            fracCoords.append(ion)
            mult = cifline[2] 
            fracCoords.append(mult)
            x = cifline[4]                                                     
            fracCoords.append(x)
            y = cifline[5]
            fracCoords.append(y)
            z = cifline[6]
            fracCoords.append(z)
            occ = cifline[-1]
            fracCoords.append(occ)
        
        # Flag when the module should starting recording the coordinates
        if modcif[j] == "_atom_site_occupancy":
            startC = True
        if startC == True:
            if modcif[j+1] == "loop_" and modcif[j+2] == "_atom_site_aniso_label":
                startC = False
            if modcif[j+1].split()[0] == "#End":
                startC = False
    
    # Convert and reshape for use with information theory
    fracCoords = np.array(fracCoords)
    fracCoords = fracCoords.reshape(-1 ,7)
    return fracCoords

"------------------------------------------------------------------------------"

Output = open('outputs/InformationOutput.txt', "w")
# Loop across the downloaded cifs from FetchCifs
for i in range(1, 10000000):
    cif = ""
    
    # Copy original cif to a string
    CifFile = "cifs/icsd_" + str(i).zfill(6) + ".cif" 
    if os.path.exists(CifFile) == True:
        try:
            OldCif = open(CifFile, "r")
            for line in OldCif:
                cif += str(line)
            
            # Uses ExtractCif to get just the coordinate data for the information theory function
            data = ExtractCif(cif)
            Sites = 0
            for c in range(0, len(data)):  
                Sites += float(data[c,2])
            
            # Finding the primitive structure using pymatgen cifparser and primitive functions
            cifparsed = CifParser(CifFile)                                     
            structure = cifparsed.get_structures()[0]
            SPrim = structure.get_primitive_structure()
            Scale = Sites / len(SPrim)
            CellVol = SPrim.volume                                 
            
            # Scale the multiplicities from the original cif to the primitive structure
            for Count in range(0, len(data)):
                data[Count,2] = float(data[Count,2]) / Scale                 
            
            # Filepath of modified cifs for crystIT to read
            newCifFile = "modcifs/icsd_" + str(i).zfill(6) + ".cif"
            
            CrystOut = crystIT.processFile(newCifFile, False, False, 0.001)
            infdata = CrystOut[0]
            
            # Extract the Degress of Freedom, Inf. Content, Total Inf. Content and Inf. Density
            try:
                out = str(i) + " " + str(infdata[18]) + " " + str(infdata[19]) + " " + str(infdata[22]) + " " + str(infdata[23])
                Output.write(out)
                Output.write("\n")
            
            # In case crystIT fails, use the function above
            except IndexError: 
                InfData = InformationTheory(data, CellVol, SPrim)
                out = str(i) + " " + str(InfData[0]) + " " + str(InfData[1]) + " " + str(InfData[2]) + " " + str(InfData[3])
                Output.write(out)
                Output.write("\n")
        
        # In case there are any problems
        except:
            out = str(i)+" Failed"
            Output.write(out)
            Output.write("\n")
            pass
        
Output.close()