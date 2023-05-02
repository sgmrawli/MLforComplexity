import numpy as np
import os.path
from pymatgen.io.cif import CifParser
from pymatgen.analysis.local_env import CrystalNN
from pymatgen.transformations.standard_transformations import DiscretizeOccupanciesTransformation

def TopIndex(PData):
    "This function finds the distinct topological sites according to Baur et al"
    "Finds the coordinated sites, and their coordination numbers"
    "Generates a list of all unique sites, the length of this is 't' from equation"
    SiteArray = []
    
    # Pymatgen tools to find nearest neighbour and to remove disorder from structures
    NN = CrystalNN(porous_adjustment=False)
    DisorderFix = DiscretizeOccupanciesTransformation(max_denominator=1, tol=1e06)
    DSetting = 'take_max_species'
    
    # For all the sites, get their coordination numbers and environments
    for j in range(0, len(PData)):
        CN = NN.get_cn(PData, j, on_disorder =DSetting)
        try:
            NNDict = NN.get_nn_info(PData, j)
        except AttributeError:
            PData = DisorderFix.apply_transformation(PData)                                              
        NNDict = NN.get_nn_info(PData, j)  
        
        # Append the ion and its CN to a list of bonded sites
        SiteArray.append(str(PData[j]).split(" ")[-1])
        SiteArray.append(str(CN))
        
        # For every site in the coordinated sites, obtain the atom label and CN
        SiteList = []
        for x, site in enumerate(NNDict):
            AtomLabel = (str(NNDict[x]['site'])).split(" ")[-1]
            AtomCN = str(NN.get_cn(PData, (NNDict[x]['site_index']), on_disorder =DSetting))
            SiteList.append(AtomLabel + AtomCN)
        
        # Get all the sites from the list and make them into one string
        # This keeps the array an X by 4, in order to use the unique command
        SiteStr = ""
        for x in range(0, len(SiteList)):
            SiteStr = SiteStr + str(SiteList[x]) + " "
        SiteArray.append(SiteStr)

    # Convert the list of every site into a list of only unique sites (by row)
    SiteArray = np.array(SiteArray)
    SiteArray = SiteArray.reshape(-1, 3)
    SiteArray = np.unique(SiteArray, axis=0)
    
    # Return the value for t, used in the equation It = (t-e) / t
    return len(SiteArray)

"------------------------------------------------------------------------------"

Output = open('outputs/IndicesOutput.txt', "w")
# Loop across the downloaded cifs from FetchCifs
for i in range(1, 1000000):
    
    # Open the cif and convert to a primitive structure 
    CifFile = "cifs/icsd_" + str(i).zfill(6) + ".cif" 
    if os.path.exists(CifFile) == True:
        try:
            cifparsed = CifParser(CifFile)                                     
            structure = cifparsed.get_structures()[0]
            SPrim = structure.get_primitive_structure()
            
            # e is the number of elements in the formula
            e = len(SPrim.formula.split()) 
            
            # Try using the TopIndex function but if not, write failed
            try:
                t = TopIndex(SPrim)
                
                # Calculate IT based on Baur et al Equations
                IT = (t-e)/t
                if IT < 0:
                    IT = 0
            except:
                IT = "Failed"
        
            # c is the number of sites in the structure
            c = len(SPrim)
        
            # Avoids a divide by zero, just in case - shouldn't be used but a failsafe
            if c == 0:                                                                 
                c = e                                                    
            IC = (c-e)/c
            
            out = str(i) + " " + str(IC) + " " + str(IT)
            Output.write(out)
            Output.write("\n")
        
        # In case there are any problems
        except:
            out = str(i)+" Failed"
            Output.write(out)
            Output.write("\n")
            pass
    
Output.close()