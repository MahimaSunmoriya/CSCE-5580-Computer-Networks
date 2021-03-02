########################################################################################################
##       Project 1                                                                                 #####
##       CSCE 5320      : Computer Networks (Spring 2021 1)                                        #####
##       Author         : Mahima Sunmoriya                                                         ##### 
##       Date           : 02/11/2021                                                               #####
##       Description    : This is a Server program which will accept packets transmitted by client #####
##                      : until a Control + C (ControlBreak) is detected, also it will randomly    #####
##                        lose some packets                                                        #####
########################################################################################################



# Importing required libraries
import socket
import sys
import random

# Function to prompt user to provide any port to listen
def check_argu():
    if(len(sys.argv) == 1 or len(sys.argv)>2):
        print(" Please input in following format: filename <port number>")
        sys.exit()
# Calling user prompt function 
check_argu()
# defining varaibles for program
UDP_IP = ""
UDP_Port = int(sys.argv[1])
bufSize = 1024
msgFrmServer = "PONG"
drop_pack_size = random.randint(2,4)   # for Randomly selecting packet lost between 2 to 4
packLoss =[]

# Function for randomly dropping packages
def rand_pack_to_loss():
    for i in range(drop_pack_size):
        packLoss.append(random.randint(0,9))

# Create a datagram socket For UDP Server socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((UDP_IP, UDP_Port))

# Display message to ensure the program is ready to accept messages on port
print("ready to accept data")

# Listen for incoming datagrams
rand_pack_to_loss()
count = 0
while(True):
   try:
     bytesAddressPair = UDPServerSocket.recvfrom(bufSize)

     message = bytesAddressPair[0]

     address = bytesAddressPair[1]


     if count in packLoss:
            clientMsg = "Client:{}".format(message)
            srvMsg = "Server: Dropped Packet"
            msgFrmServer = ''
            losspack = True
     else :
            clientMsg = "Client:{}".format(message)
            msgFrmServer = 'PONG'
            losspack = False

    # No reply will be sent to client if the packet is lost on server   
     if losspack == True:
        print(clientMsg)
        print(srvMsg)

    # Sending a reply to client if packet is not lost
     else:
        print(clientMsg)
        bytesToSend = str.encode(msgFrmServer)

    
        UDPServerSocket.sendto(bytesToSend, address)

     count = count +1
     
# Handling of Keyboard Interrupt 
   except KeyboardInterrupt:
        print ("[CTRL+C detected, exiting program]")
        sys.exit()

################################   END OF PROGRAM     #################################################################