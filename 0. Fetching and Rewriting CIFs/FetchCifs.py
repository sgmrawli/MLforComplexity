import os.path
from ICSDClient import ICSDClient
# Instantiate a new client using the login information
cl = ICSDClient("AVV9002683","icsd591")

# Loop over a range of collection codes to get the cif files out
flag = 0
for i in range(1, 10000000):
    
    # Added this statement, if the file already exists, don't redownload - useful for future work
    CifFile = "cifs/icsd_" + str(i).zfill(6) + ".cif"
    if os.path.exists(CifFile) == True:
        pass
    else:
        try:
            cl.logout()
            cl = ICSDClient("AVV9002683","icsd591")
            sd = {"collectioncode": str(i)}
            newsearch = cl.advanced_search(sd) 
            item = list(newsearch[0])                                          
            cif = cl.fetch_cif(item[0])
    
            # Call the writeout method to save the cif to a file
            cl.writeout(cif)                                                   
        except IndexError:
            pass