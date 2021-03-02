########################################################################################################
##       Project 1                                                                                 #####
##       CSCE 5320      : Computer Networks (Spring 2021 1)                                        #####
##       Author         : Mahima Sunmoriya                                                         ##### 
##       Date           : 02/11/2021                                                               #####
##       Description    : This is a client program which will send 10 pings to specified port on   #####
##                      : the server. Given the server is listening on the same port, this program #####
##                      : will display the messages recieved from server. It will also display the #####
##                      : number of packets sent/lost/lost percentage. It will also calculate RTT  #####
##                      : for each ping and display Minimum/Maximum and Average RTT                ##### 
########################################################################################################

# Importing required libraries
import socket
import sys
import time

# Function to prompt user to provide combination of server name and port combination in case incorrect format enter
def arguCheck():
     if len(sys.argv) == 1 and len(sys.argv) > 2 :
        print("Incorrect format  please specify in following way:")
        print("Input Format: <file name> <server name> <port number>")
        sys.exit()

# Calling user prompt function 
arguCheck()

# defining varaibles for program
msgFromClient       = "PING"
bytesToSend         = str.encode(msgFromClient)
UDP_IP = socket.gethostbyname(sys.argv[1])
UDP_Port = sys.argv[2]
serverAddressPort   = (UDP_IP, int(UDP_Port))
bufferSize          = 1024
Resp_Avg = []
sendCount = 10
recvCount = 0

# Round Trip Time function in ms
def RTT_Cal(a,b):
    rtt_val = (a-b) * 1000
    return str(rtt_val)

# Send  to server using created UDP socket and recieveing message from server
def Messages():
    for i in range(10):
        clientSendTime = time.time()
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        UDPClientSocket.settimeout(1)
        try:
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            serverMsg = "Server: {}".format(msgFromServer[0])
            serverRespondTime = time.time()
            resp_time = RTT_Cal(serverRespondTime,clientSendTime)
            print(serverMsg + ":RTT= :" +  resp_time + " ms")
            Resp_Avg.append(resp_time)

        except socket.timeout:
            print('Time Out')               #if the packet does not recieve within 1 sec client assume packet lost
            continue

# Function to calculate Max/Min Average RTT in ms 
def Resp_fun():
    min_Resp = min(Resp_Avg)
    max_Resp = max(Resp_Avg)
    roundResp = []
    for i in range(len(Resp_Avg)):
        roundRTT = round(float(Resp_Avg[i]),6)
        #roundRTT = round(float(i),5)
        roundResp.append(roundRTT)
    avg_Resp = sum(roundResp)/ len(roundResp)
    print("Minimum RTT :" + str(min_Resp) +" ms")
    print("Maximum RTT :" + str(max_Resp) +" ms")
    print("Average RTT :" + str(avg_Resp) +" ms")

# Function to display the Total transimitted/ Received packets and Packet loss percentage
def Packet_count_fun():
    print ("Tranmitted Packets: " + str(sendCount))
    print ("Packet recieved from server " +  str(len(Resp_Avg)))
    lostPck = (sendCount - len(Resp_Avg))
    percLostPck = ((lostPck * 100) / sendCount)
    print("Packet Loss Percentage :" + str(percLostPck)+ "%")

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Calling function to display PONG  message with RTT  and Time Out in case packet lost at server end 
Messages()

# Calling Funcion to calculate Max/Min Average RTT in ms 
Resp_fun()

# Calling function to display the Total transimitted/ Received packets and Packet loss percentage
Packet_count_fun()


################################   END OF PROGRAM     #################################################################
                        