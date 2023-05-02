import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

 # Plot a histogram using matplotlib
def Histogram(Arr):
    SArr = np.sort(Arr)
    mean = np.mean(SArr)
    mode = (stats.mode(SArr, keepdims="False"))[0][0]
    median = np.median(SArr)
    plt.hist(SArr, bins= 'fd', color = 'black')
    plt.xlabel('Information Content (bits/atom)')
    plt.ylabel('Frequency')
    plt.title('Histogram of Information Content')
    plt.axvline(mean, color = 'blue', linestyle = 'dashed', linewidth = 0.75, label = 'Mean '+str('%.2f' %mean))
    plt.axvline(mode, color = 'red', linestyle = 'dashed', linewidth = 0.75, label = 'Mode '+str('%.2f' %mode))
    plt.axvline(median, color = 'green', linestyle = 'dashed', linewidth = 0.75, label = 'Median '+str('%.2f' %median))
    plt.legend()
    plt.show()
    
    
Density = open("outputs/DensitiesOutput.txt", "r")
Information = open("outputs/InformationOutput.txt", "r")

# Take all of the information from 
Densities = []; eDensities = []; Volumes = []; SGNumbers = []
for line in enumerate(Density):
    x = line[1].split(" ")
    try:
        # print(x[1:-6]) # Structural Formula
        # print(x[-5]) # Space Group Symbol
        SGNumbers.append(x[-4]) # Space Group Number
        Volumes.append(np.log10(float('%.4f' % float(x[-3])))) # Volume
        Densities.append(np.log10(float('%.4f' % float(x[-2])))) # Density
        eDensities.append(np.log10(float('%.4f' % float(x[-1])))) # e- Density
    except IndexError:
        pass

cDoF = []; InfContent = []; TotInf = []; InfDensity = []
for line in enumerate(Information):
    y = line[1].split(" ")
    if y[1] == "Failed":
        pass
    try:
        cDoF.append(float(np.sqrt(int(y[1])))) # degrees of freedom
        if np.isnan(float(y[2])) == False:
            InfContent.append(float('%.8f' % float(y[2]))) # inf content
        if np.isnan(float(y[3])) == False:
            TotInf.append(np.sqrt(float('%.8f' % float(y[3])))) # total inf content
        if np.isnan(float(y[4])) == False:
            InfDensity.append(np.sqrt(float('%.8f' % float(y[4])))) # inf density
    except:
        pass

Histogram(np.array(InfContent))
