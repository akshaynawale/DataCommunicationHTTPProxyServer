###################### AUTHOR ####################################################
Name: Akshay Satyendra Navale
Occupation: ITP Student at University of Colorado, Boulder.USA.
Contact Details: akna8887@colorado.edu
Phone Number: 720-345-4053
##################################################################################

Welcome!!! 
This is a README file for webproxy.py program.
The python code is written in python version 2.7.

############### Required configurations on browser ##################################################

To use this proxy use must set a proxy setting into your browser. This code runs at 127.0.0.1 IP. 
The port number can be given as a argument for this program. So configure the portnumber on which you are 
going to run this program in the browser.

################## webproxy arguments ##################################################################
This file is a Sender file which takes 2 arguments in following fashion (and 2nd is optional).
1) Port number between 1024 to 65535.
2) Secound argument is option which sets timeout value in secounds.

to run this file fire the command as below,
webproxy.py [Port number] [Timeout]
e.g.:
webproxy.py 5000 120
5000 is port number and 100 is timeout value in secounds

This program check for 
1) Validity of Port Number (Port number must be greter than 1024 and less than 65535)
3) The value of the portnumber and the timeout must be integer.

############### Operation Method ######################################################
In this program proxy takes the request from browser then it parse it and check for nay errors.
Then it check the requested file availability in the local database. (local database is stored in database folder).
If the file is available then sends it directly to the client. 
If the file is not available then it requests the page from the actual server. 
Ans stores it in the local database. and send it to client.

################### Clearing old files from database ################################
This program runs a background process called "WipeOut" which check the files system and 
removes the files for which the timeout is reached.
 
##########Default Functioning#############################################################
The timeout for database file is by default set to 120sec (2 min).
The Wipeout program runs in background at every one minute.

##########################################################################################
Thank You. For your precious time!!!  

 