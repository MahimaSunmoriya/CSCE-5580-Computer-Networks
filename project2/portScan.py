########################################################################################################
##       Project 2                                                                                 #####
##       CSCE 5320      : Computer Networks (Spring 2021 1)                                        #####
##       Author         : Mahima Sunmoriya                                                         ##### 
##       Date           : 03/19/2021                                                               #####
##       Description    : This Program is to scan the port on TCP and UDP. In TCP it will give the #####
##                      : list of all open ports and for UDP it will randomly show the output for  #####
##                      : open and close port. In both case service name corresponding to that port#####
##                      : will be displayed. In case no service is specified it will show "svc name#####
##                      : unavil"                                                                  ##### 
########################################################################################################
                       
# Importing required libraries
import socket
import time
import os
import sys

# vaiable declaration
hostname =''     #for taking host name from console
protocol = ''    #for taking protocol name from console
portlow = ''     #for taking port low range from console
porthigh = ''    #for taking port high range from console
service = ''      #for storing service name recieved by getservbyport

# method for getting service name for both UDP and TCP
def getServiceName(port, proto):
        try:
            name = socket.getservbyport(int(port), proto)
        except:
            return 'svc name unavail'
        return name

# protocol name Validation Method
def protocolcheck():
        if protocol not in ('tcp','udp'):
                        print('invalid protocol: '+ protocol + '. Specify "tcp" or "udp"')
                        quit()

# Driving method to Scan (host, port) in TCP and UDP and displayed at console. In UDP closed port will be displayed too.
def scanhost():
     try:
            t_IP = socket.gethostbyname(hostname)
            protocolcheck()
            print ('scanning host=: ' + hostname + ', protocol=' + protocol + ', ports: ' + portlow + '  -> '  +  porthigh)
            portlowint = int(portlow)
            porthighint = int(porthigh)
            if protocol == 'tcp':
                for i in range(portlowint, porthighint):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    conn = s.connect_ex((t_IP, i))
                    service = getServiceName(i,protocol)
                    if(conn == 0) :

                        print ('Port  ' + str(i) + '         open:' + service)
                    s.close()

            elif protocol == 'udp' :
                     for i in range(portlowint, porthighint):
                         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                         conn = s.connect_ex((t_IP, i))
                         if(conn == 0):
                            try:
                                s.sendto(str.encode('ping'),(t_IP,i))
                                s.settimeout(1)
                                recv =s.recv(1024)
                            except socket.error as errm:
                                if errm[0] != 111:
                                    service = getServiceName(i,protocol)
                                    res = os.system("nc -vnzu "+t_IP+" "+str(i)+" > /dev/null 2>&1")
                                    service = getServiceName(i,protocol)
                                    if(res == 0 ) :
                                        print ('Port ' + str(i) + '          open: ' + service)
                                    else:
                                        print ('Port ' + str(i) + '          closed: ' +service)
                                s.close()
                                continue

# If invalid hostname given by user(example cse07)
     except socket.gaierror:
         print('error: host ' + hostname +  ' not exist')
         sys.exit()
# Keyborad Exception for CLT + C
     except KeyboardInterrupt:
         print("CLT + C detected")
         s.close()
         sys.exit()

# validation of inputs given by user:
if len(sys.argv) != 5:
        print ('usage: portScan.py <hostname> <protocol> <portlow> <porthigh>')
        quit()
else:
        hostname = sys.argv[1]
        protocol = sys.argv[2]
        portlow = sys.argv[3]
        porthigh = sys.argv[4]

#calling to scanhost method
scanhost()


