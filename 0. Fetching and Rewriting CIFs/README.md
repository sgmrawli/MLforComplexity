Fetching the cifs from scratch takes a very long time on a standard PC, the cifs directory here includes the cifs used at the time of uploading. 
The code was created to check for existing cifs 1 by 1, instead of downloading multiple at once which is also possible using ICSDClient

ICSD Access is required for the use of this code, alongside ICSDClient (https://github.com/lrcfmd/ICSDClient)
There should not be a problem with timing out with this code, as each cif is downloaded one by one and a refresher statement is included.
