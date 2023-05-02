import numpy as np
import pymatgen.core as pmg
from pymatgen.io.cif import CifParser
import os.path

def ExtractData(cif):
    "This function extracts the necessary information for the calculations from the ICSD cif file"
    SpaceGroup = []; startC = False; AtomData = []
    modcif = cif.split("\n")
    for j in range(0, (len(modcif))):
        
        # Failsafe if the cif doesn't have a defined last line
        if startC == True and j == len(modcif)-1:
            startC = False
            
        # When the flag is on, extract the required coordinate data
        if startC == True:
            cifline = modcif[j].split()
            atom = cifline[0]
            AtomData.append(atom)
            mult = cifline[2] 
            AtomData.append(mult)
            
        # Flag when the module should starting recording the coordinates
        if modcif[j] == "_atom_site_occupancy":
            startC = True
        if startC == True:
            if modcif[j+1] == "loop_" and modcif[j+2] == "_atom_site_aniso_label":
                startC = False
            if modcif[j+1].split()[0] == "#End":
                startC = False
                
        # Get the space group symbol and number
        if modcif[j].split(" ")[0] == "_space_group_name_H-M_alt":
            SpaceGroup.append((modcif[j].split(" "))[1:])
        if modcif[j].split(" ")[0] == "_space_group_IT_number":
            SpaceGroup.append((modcif[j].split(" "))[1:])
    
    # Reshape into a NumPy array
    AtomData = np.array(AtomData)
    AtomData = AtomData.reshape(-1 ,2)
    
    return AtomData, SpaceGroup

def EDensity(AData):
    "This function returns the electron count for a crystal"
    eSum = 0
    # Get the electron count for each element in the structure
    for i in range(0, len(AData)):
        elem = AData[i,0]
        elem = ''.join(x for x in elem if not x.isdigit())
        # Pymatgen can't interpret D as an atom, made a function to deal with this
        try:
            eSum += ((pmg.Element(elem)).Z * float(AData[i,1]))
        except:
            eSum += RareAtoms(elem, 2)
    # Return the total number of electrons in the structure
    return eSum

def Density(A, Vol):
    "This function returns the density if it fails in pymatgen"
    aSum = 0
    for i in range(0, len(A)):
        elem = A[i,0]
        elem = ''.join(x for x in elem if not x.isdigit())
        # Pymatgen can't interpret D as an atom, made a function to deal with this
        try:
            aSum += pmg.Element(elem).atomic_mass
        except:
            aSum = RareAtoms(elem,1)
    d = aSum / Vol
    return d

def RareAtoms(A, flag):
    "This function returns the atomic or electron number for atoms pymatgen can't handle"
    # flag is 1 for atomic mass
    if A == "D" and flag == 1:
        return 2
    # flag is 2 for electron number
    if A == "D" and flag == 2:
        return 1
"------------------------------------------------------------------------------"

Output = open('outputs/DensitiesOutput.txt', "w")
for i in range(1, 1000000):
    
    # Name of the cif file to be opened
    CifFile = "cifs/icsd_" + str(i).zfill(6) + ".cif" 
    if os.path.exists(CifFile) == True:
    
        # Write the contents of a cif to a string to get electron density data
        cif = ""
        
        try:
            OldCif = open(CifFile, "r")
            for line in OldCif:
                cif += str(line)
            
            # Turn the cif into a structure object from pymatgen
            cifparsed = CifParser(CifFile)                                     
            structure = cifparsed.get_structures()[0]
            SPrim = structure.get_primitive_structure()
            
            # Pull the atoms, multiplicity and space group data from the cif
            dat = ExtractData(cif)
            CrystData = dat[0]
            SGData = dat[1]
            
            # Write the space group symbol as a single string
            SGSymbol = ""
            for g in range(0, len(SGData[0])):
                SGSymbol += SGData[0][g]
            
            # Find the density and electron density
            # Pymatgen doesn't recognise D as an atom - made a workaround
            try:
                Dens = (str(SPrim.density).split(" "))[0]
            except:
                Dens = Density(CrystData, SPrim.volume)
                Dens = str((Dens * 1.660578))
            EDens = (EDensity(CrystData) / SPrim.volume)
            
            # Coll. Code, Formula, Space Group, Space Group Number, Volume, Density, e- Density written to file
            out = str(i)+" "+str(SPrim.formula)+" "+ SGSymbol+" "+str(SGData[1][0])+" "+str(SPrim.volume)+" "+Dens+" "+str(EDens)
            Output.write(out)
            Output.write("\n")
    
        # In case there are any problems
        except:
            out = str(i)+" Failed"
            Output.write(out)
            Output.write("\n")
            pass
        
Output.close()