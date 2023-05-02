This work is for the prediction of total information content of crystal structure CIFs, using the ICSD.

The project is separated into 4 sections:
0. Fetching the CIFs
1. Calculating the data
2. Investigating the data
3. Extra Trees ML model for predicting complexity

Notes:
1. ICSDClient (https://github.com/lrcfmd/ICSDClient) is required for use in sections 0 and 1.
2. ICSD API access is required to make use of ICSDClient, only base level access is needed as code to refresh access is used here.
3. crystIT (https://github.com/GKieslich/crystIT) is required for section 1 (Information Theory.py)
