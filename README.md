# DHCP STARVATION
## to first start : 
```
python3 dhcpStarvation.py -h 
```
## dhcp server config - ubuntu server  : 
```
>> sudo apt-get update
>> sudo apt install isc-dhcp-server
>> sudo nano /etc/netplan/OO-installer-config.yaml
network:
  ethernets:
    <your interface>:
      dhcp4:no
      addresses:
        - <personal local network  address> /<cidr>
     version:2
>> sudo nano /etc/dhcp/dhcpd.conf
subnet <personal local network  address> <sub network mask> {
  range <start given address> <end of seq of addresses> ;
  option subnet-mask <sub network mask > ;
  option broadcast-address <broadcast address>;
  default-lease-time 400 ; 
  max-lease-time 800; 
>> sudo nano /etc/default/isc-dhcp-server
 change only that line ::: INTERFACESv4="<your interface>" 
>> sudo service isc-dhcp-server start 
}
```
# watch logs and conected users : 
```
full list : >> dhcp-lease-list --lease
get only ip : >> dhcp-lease-list --lease | cut -d " " -f 3 | grep -E '^((25[0-5]|2[0-4][0-9]|[1]?[1-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[1]?[1-9]?[0-9])$' | sort
get num of ip's :  >>   dhcp-lease-list --lease | cut -d " " -f 3 | grep -E '^((25[0-5]|2[0-4][0-9]|[1]?[1-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[1]?[1-9]?[0-9])$' | wc -l 
get status : >> service isc-dhcp-server status 
