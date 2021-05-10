########################################################################################################
##       Project 3                                                                                 #####
##       CSCE 5320      : Computer Networks (Spring 2021 1)                                        #####
##       Author         : Mahima Sunmoriya                                                         ##### 
##       Date           : 04/06/2021                                                               #####
##       Description    : This is a TCP server for listenting to multiple clients and performing   #####
##                      : action based on command JOIN, LIST, MESG,BSCT, QUIT                      #####
########################################################################################################

# Importing required libraries

import socket
import select
import sys
from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# checks number of arguments have been provided
if len(sys.argv) != 2:
        print ("Correct usage: <program name > <port number>")
        exit()

#Current IP 
IP_address = ""

# takes second argument from command prompt as port number
Port = int(sys.argv[1])
# BIND THE PORT. IF not successfull through and error and exit program
try:
    server.bind((IP_address, Port))
    server.listen(100)
except socket.error as errnm:
        if errnm[0] == 98:
            server.close()
            print("socket is in use. Please try again in some time")
            sys.exit()
#variable defination
list_of_fd =[]
list_of_clients = []
list_of_conn =[]
print("Waiting for Incoming Connections...")

# Method for JOIN command. ADD the client to database. Only upto 10 clients can be uploaded.
def joinmethod(fd,message,conn):
    splitmess = message.split()
    if(len(splitmess)!=2):
        msgtoclient="incorrect format Please enter in following format JOIN> <Username>\n"
        conn.send(msgtoclient)
    elif(len(list_of_clients) <= 10):
        if(fd in list_of_fd):
            index = list_of_fd.index(fd)
            username = list_of_clients[index]
            filedesc = list_of_fd[index]
            msgtoclient = "User already Register: Username " +username +", FD" + str(filedesc) +"\n"
            conn.send(str.encode(msgtoclient))
            print("Requeste Denied : User already exist corresponding to FD:" + str(filedesc)+":"+str(username))
        else:
            print("Client[" +str(fd) + "] " + str(message))
            list_of_clients.append(splitmess[1])
            list_of_conn.append(conn)
            list_of_fd.append(fd)
            msgtoclient = message + "Request Accepted \n"
            conn.send(str.encode(msgtoclient))
    else:
        msgtoclient ="Error: Too manny clients \n"
        conn.send(str.encode(msgtoclient))
        print("Client[" +str(fd) + "] : Database Full. Disconnecting User.")
# MEthod for LIST command. If client is registered LIST of ALL clients will be displayed otherwise proper message to register will be displayed
def listmethod(fd,msg,conn):
    message = msg.split()
    if(len(message)!=1):
        mestoclient = "usage <LIST> \n"
        conn.send(str.encode(mestoclient))
    elif(fd in list_of_fd):
        clientmessage = "USER NAME  FD \n" + "-------------------------\n"
        conn.send(str.encode(clientmessage))
        for i in range(len(list_of_clients)):
              conn.send(list_of_clients[i]+"\t" + str(list_of_fd[i])+"\n")

        conn.send("--------------\n")
    else:
        print("Unable to Locate Client["+ str(fd)+"] in Database. Discarding LIST.")
        mestoclient = "Unregistered User. Use 'JOIN <username>' to Register.\n"
        conn.send(mestoclient)
#METHOD for MESG command To send mesg to particular client specified by user name.  Otherwise display proper error message      
def mesgfunction(fd, message,conn):
    msglist =message.split(' ', 2)
    if (conn in list_of_conn):
        if(msglist[1] in list_of_clients):
            cliindex = list_of_clients.index(msglist[1])
            sendconn = list_of_conn[cliindex]
            sending_cli_inx = list_of_conn.index(conn)
            sendingCli = list_of_clients[sending_cli_inx]
            msgtoclient = "From user: "+sendingCli +"\t" + str(msglist[2])
            sendconn.send(str.encode(msgtoclient))
        else:
            if(len(message.split())== 2):
                msglist =message.split()
                print("Unable to Locate Recipent[" + (msglist[1])+ "] in Database. Discarding MESG")
                msgtoclient = "Unknown Recipient (" + (msglist[1])+ ") . MESG Discarded \n"
                conn.send(str.encode(msgtoclient))

            else:
                print("Unable to Locate Recipent[" + (msglist[1])+ "] in Database. Discarding MESG")
                msgtoclient = "Unknown Recipient (" + (msglist[1])+ ") . MESG Discarded \n"
                conn.send(str.encode(msgtoclient))
    else:
        msgtoclient = "Unregistered User. Use 'JOIN <username>' to Register.\n"
        msgonserver = "Unable to Locate Client[" +str(fd)+"] in Database. Discarding MESG"
        conn.send(str.encode(msgtoclient))
        print(msgonserver)
# Thread to handle multiple clients
def clientthread(conn, addr):
    fd = conn.fileno()
    while True:
        try:
            message = conn.recv(2048)
            checkmsg = message.split()
            if(checkmsg[0]=="JOIN"):
                joinmethod(fd,message,conn)
            if(checkmsg[0] == "LIST"):
                listmethod(fd,message,conn)
            if(checkmsg[0] == "MESG"):
                mesgfunction(fd,message,conn)
            if (checkmsg[0] == "BCST"):
                broadcast(fd,message, conn)
            if(checkmsg[0] == "QUIT"):
                remove(conn,message)
            if(checkmsg[0] not in ["JOIN","LIST","MESG","BCST","QUIT"]):
                msgtoclient = "Unrecognizable Message. Discarding UNKNOWN Message.\n"
                conn.send(str.encode(msgtoclient))
                print(msgtoclient)
        except:
            continue
# TMETHOD for BCST . TO broadcast message to all client except self
def broadcast(fd,message, connection):
    print("Broadcast method" , message)
    if(fd in list_of_fd):
        index = list_of_fd.index(fd)
        for i in range(len(list_of_conn)):
            if(i != index):
                try:
                    msgsplit = message.split(" ",1)
                    msgtoclient = "From " + str(list_of_clients[index]) +"\t " + str(msgsplit[1]+"\n")
                    list_of_conn[i].send(str.encode(msgtoclient))
                except:
                    list_of_conn[i].close()
    else:
        msgtoclient = "Unregistered User. Use 'JOIN <username>' to Register.\n"
        msgonserver = "Unable to Locate Client" +str(fd)+" in Database. Discarding BCST"
        conn.send(str.encode(msgtoclient))
        print(msgonserver)

#METHOD for QUIT. To remove the client from database and close the connection.
def remove(connection,message):
      if connection in list_of_conn:
          rmvindex = list_of_conn.index(connection)
          client = list_of_clients[rmvindex]
          clientfd = list_of_fd[rmvindex]
          msgtoclient =" connection closed for Username:" + str(client) +"\n"
          list_of_clients.remove(client)
          list_of_conn.remove(connection)
          list_of_fd.remove(clientfd)
          connection.send(str.encode(msgtoclient))
          print("Client[" +str(clientfd) + "] :" + str(message))
          print("Client[" +str(clientfd) + "] :" + "Diconnecting User")
          connection.close()
      else:
          msgtoclient =" connection closed by foriegn host \n"
          connection.send(str.encode(msgtoclient))
          connection.close()
#Waiting for clients to connect
while True:
    conn, addr = server.accept()
    # prints the address of the user that just connected
    print ("Client[" +str(conn.fileno()) + "] connection Accepted")
    print("Client[" +str(conn.fileno()) + "] Connection Handler Assigned")
    # creates and individual thread for every user
    # that connects
    start_new_thread(clientthread,(conn,addr))
conn.close()
server.close()

                           