from scapy.all import sniff,UDP,DHCP,BOOTP,IP,Ether,RandInt,RandMAC,srp1,sendp,DHCPRevOptions
from scapy.utils import mac2str
import random
from threading import Thread,get_ident 
class DHCPClient:
	__count__=0
	__BROADCASTMAC__ = "ff:ff:ff:ff:ff:ff"
	__BROADCASTIP__ = "255.255.255.255"
	def __init__(self) : 
		self.mac = str(RandMAC())
		self.ip = None  
		DHCPClient.__count__+=1
		self.name = DHCPClient.__count__ 
		self.Frame = Ether(dst = DHCPClient.__BROADCASTMAC__, src = self.mac) 
		self.Datagram = IP( dst = DHCPClient.__BROADCASTIP__, src= "0.0.0.0" ) 
		self.Segment = UDP(dport=67,sport=68)
		self.Bootp = BOOTP(chaddr=mac2str(self.mac) , xid = RandInt()) 
	def __requestyou__(self,packet):
		print(packet.show())
		self.ip = packet["IP"].dst
		print(f"IPPPPPPP:{self.ip} , {get_ident()}")


	def __offerme__(self):
		sniff(lfilter= lambda packet :Ether in packet and packet[Ether].dst == self.mac and  UDP in packet and packet["UDP"].sport  == 67 and DHCP in packet and (print(packet[DHCP].options) or True) and ('message-type', 2 ) in packet[DHCP].options , 
          	prn=self.__requestyou__,
          	store=0,count=1)

	def discover(self):  
		print(self.mac , self.name , self.mac) 
		DHCPPACK = DHCP ( options = [('message-type','discover'),('hostname','kali'),('param_req_list', [
		1,2,5,12,15,26,28,121,3,33,40,41,42,119,249,252,17

		] )   ,'end'] )
		pack = self.Frame / self.Datagram/self.Segment /self.Bootp / DHCPPACK
		print(pack.show())
		Thread(target=self.__offerme__).start()
		sendp(pack,iface='eth0')

print(get_ident())
client = DHCPClient()
client.discover() 
