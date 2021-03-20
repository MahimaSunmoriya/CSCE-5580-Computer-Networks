1. Code is in python. So no need to compile explictily
2. Run it using command
	python portScan.py <hostname> <protocol> <port low> <port high>
3. Please jpeg file having all screnerio tested.
4. For cross validating UDP open and closed port , I have used netcat utility
5. with below command you can validate:
 nc -vznu <host IP > <port number>
 where v -verbose
       z- zero i/o mode(use for scanning)
       n-numeric
       u- udp protocol			  
if the port is open it will return succeeded message else it wont return anything.

6. https://www.commandlinux.com/man-page/man1/nc.1.html
