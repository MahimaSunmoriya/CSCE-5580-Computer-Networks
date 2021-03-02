1. To execute the code in the UNT CSE machine, Follow below instruction.
	
	1. First, run the server program project1srv python file 
	   followed by a port number:
	2. On other Linux machine, run client program project1cli 
	   python file followed by IP address of the server and port number

Follow below command

server machine: cse01
	python project1svr.py 8090     # any port number you can give
Client machine: cse02
	 python project1cli.py cse01 8090

After connection, you can see the results, such as a message sent, dropped.

On the client-side, I have displayed RTT and transmitted packets count and loss packet %.

----------------------------------------------------------------------
IMPORTANT:
 IN EVERY RUN SERVER IS RANDOMLY SELECTING A NUMBER BETWEEN 2 to 4 FOR 
EATING  MESSAGE!! 
AFTER THAT, IT IS RANDOMLY EATING the MESSAGES. LIKE 0, 4, 6 IF THE DROP
COUNT FOR PACKET DROP IS PICKED BY RANDOM SELECTION 3.

-----------------------------------------------------------------------

FOR EVERY RUN THE PACKET LOST VARY IN RANGE OF 20% to 40%. 
EVERY RUN WILL HAVE DIFFERENT PACKET LOST COUNT.

