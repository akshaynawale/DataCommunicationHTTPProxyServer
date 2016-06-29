#!/usr/bin/env python3

#Author  : Akshay Satyendra Navale akshay.nawale@colorado.edu
#Name    : Webproxy.py (Homework 6.1)
#Purpose : HTTP proxy server
#Date    : 11/22/2015
#Version : 3.2

import threading
import socket
import hashlib
import re
import time
from time import strftime, gmtime
import os
import urllib2
import sys
import requests

TimeStat={}

size=999999

## Function for removing old data from data base    ##
def WipeOut(TimeStat, TimeOut):
    while True:
        #print("Inside WipeOut")
        time.sleep(60)
        TimeStatCopy=TimeStat.copy()
        #print(TimeStat)
        try:
            Times=TimeStatCopy.values()
            for t in Times:
                CurrentTime=time.time()
                if (int(CurrentTime)-int(t)) > TimeOut  :
                    for name, times in TimeStatCopy.iteritems():
                        if times == t:
                            del TimeStat[name]
                            os.remove("backup/"+name)
        except:
            print()
            #print('unable to clear the data ERROR OCCURED')
        
##    Fetch Port number     ##
def GetData():
    if len(sys.argv)==2 or len(sys.argv)==3:
        PortNumber=sys.argv[1]
        try:
            PortNumber=int(PortNumber)
        except:
            print("Argument must be a number (Port Number)")
            sys.exit()
        if (PortNumber > 65535) or (PortNumber < 1024):
            print("The port Number must be between 1024 and 65535")
            sys.exit()
        if len(sys.argv)==3:
            try:
                TimeOut=sys.argv[2]
                TimeOut=int(TimeOut)
            except:
                print("The secound argument must be a number (Timeout)")
                sys.exit()
        else:
            TimeOut=120
        return PortNumber, TimeOut
    else:
        print("Please provide Port Number as a argument of this program (and time out as optional parameter)")
        sys.exit()
        
##    Parsing the request    ##
def ParseReq(RequestC, Status):
    try:
        data=RequestC
        line1=data.splitlines()[0]
        line1s=line1.split(" ")
        method=line1s[0]
        path=line1s[1]
        version=line1s[2]
        line2=data.splitlines()[1]
        line2s=line2.split(' ')
        host=line2s[1]
        if method!="GET" or version!="HTTP/1.0":
            Status="BAD"
        return method, path, version, host, Status
    except:
        print('Bad Request')
        Status="BAD"
        method="BAD"
        path="BAD"
        version="BAD"
        host="BAD"
        return method, path, version, host, Status

## Function to find the extension    ##
def FindExt(path):
    try:
        filelist=path.split('/')
        l=len(filelist)
        filename=filelist[l-1]
        filesplit=filename.split('.')
        l2=len(filesplit)
        ext=filesplit[l2-1]
        return ext
    except:
        return "html"
##    Function to get the hash    ##
def getHash(name):
    hash=hashlib.sha256()
    hash.update(name)
    name=hash.hexdigest()
    return name
##    Function for storing athe data    ##
def storeasFile(filename, path, TimeStat):
    try:
        r = requests.get(path, stream=True)
        print(filename)
        if r.status_code == 200:
            with open("backup/"+filename, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        t=int(time.time())
        TimeStat[filename]=t
    except:
        print("unable to store the file")

##    Function for getting the web page data    ##
def GetPageWget(path):
    try:
        page=urllib2.urlopen(path).read()
        return page
    except:
        print('unable to read')

##    Process that take care of each request    ##
def ProcessRequest(RequestC, socCLI, address, TimeStat):
    Status="GOOD"
    method, path, version, host, Status=ParseReq(RequestC, Status)
    if Status == 'GOOD':
        pathhash=getHash(path)
        ext=FindExt(path)
        filename=pathhash+"."+ext
        if os.path.isfile("backup/"+filename):
            print("found in local database "+path)         
            h=open("backup/"+filename,'rb')
            page=h.read()
            h.close()
            socCLI.sendto(page,address)
        else:
            try:
                print("New Request = "+path)
                page=GetPageWget(path)
                storeasFile(filename, path, TimeStat)
                socCLI.sendto(page,address)
            except:
                print("cant find IP ")
            socCLI.close()

#### Start of Main Program    #####
PortNumber, TimeOut=GetData()
print("Web proxy running at "+str(PortNumber))
print("Timeout : "+str(TimeOut))
## Start a Thread for WipeOut program ##
t1=threading.Thread(target=WipeOut, args=(TimeStat, TimeOut,))
t1.start()
print('thread started')

## Create a socket for accepting connection    ##
soc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(('', PortNumber))
soc.listen(5)
print("Created socket on port number "+str(PortNumber))

##    Check for backup folder and if not present then create one    ##
if not os.path.exists('backup'):
    os.makedirs('backup')

##    get into a main loop    ##t
while True:
    socCLI, address=soc.accept()
    RequestC=socCLI.recv(size)
    print(RequestC)
    threading.Thread(target=ProcessRequest(RequestC, socCLI, address, TimeStat))
