import numpy as np
import pandas as pd

# Open outputs
Density = open("outputs/DensitiesOutput.txt", "r")
Information = open("outputs/InformationOutput.txt", "r")
Indices = open("outputs/IndicesOutput.txt", "r")

# Read densities output
density = []
for x in enumerate(Density):
    D = x[1].split(" ")
    if D[1] != "Failed\n":
        density.append(D)

# Read indices output
indices = []
for z in enumerate(Indices):
    IN = z[1].split(" ")
    if IN[1] == "Failed\n":
        pass
    else:
        indices.append(IN)

# Read information output
information = []
for y in enumerate(Information):
    IF = y[1].split(" ")
    if IF[1] == "Failed\n":
        pass 
    elif np.isnan(float(IF[2])) == True:
        pass
    elif np.isnan(float(IF[3])) == True:
        pass
    elif np.isnan(float(IF[4])) == True:
        pass
    else:
        information.append(IF)

# Add each entry to array based on ICSD code across the three outputs
Data = []
for i in range(0, len(density)):
    print(i)
    for j in range(0, len(information)):
        for l in range(0, len(indices)):
            if information[j][0] == density[i][0] and information[j][0] == indices[l][0]:
                Formula = "".join(density[i][1:-6])
                Data.append(int(density[i][0]))
                Data.append(Formula)
                Data.append(float('%.4f' % float(density[i][-4])))   #SG Number
                Data.append(float('%.4f' % float(density[i][-3]))) #Volume
                Data.append(float('%.4f' % float(density[i][-2]))) #Density
                Data.append(float('%.4f' % float(density[i][-1]))) #eDensity
                Data.append(int(information[j][1]))                 #Coordinational degrees of freedom
                Data.append(float('%.4f' % float(information[j][2]))) # inf content
                Data.append(float('%.4f' % float(information[j][3]))) # total inf content
                Data.append(float('%.4f' % float(information[j][4]))) # inf density
                Data.append(float(indices[l][1]))
                break
            pass

# Output array to a .csv file to investigate correlations
arr = np.array(Data)
arr = arr.reshape(-1, 11)
c = ['ICSD Code', 'Formula', 'Space Group Number', 'Volume', 'Density', 'Electron Density', 'Coordinational Degrees of Freedom', 'Information Content', 'Total Information Content', 'Information Density', 'Crystallographic Index']
df = pd.DataFrame(arr, columns = c)
df.to_csv('CleanData.csv')