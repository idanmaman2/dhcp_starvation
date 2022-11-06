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
```
# Examples
## before the  attack : 
<img width="1029" alt="Screen Shot 2022-11-06 at 23 29 38" src="https://user-images.githubusercontent.com/90776557/200196854-ae2474ed-e29c-40b9-9efb-c1033a559eb7.png">

## after the attack : 

<img width="908" alt="Screen Shot 2022-11-06 at 23 30 12" src="https://user-images.githubusercontent.com/90776557/200196862-9cc45ded-4d95-4443-91ea-4ee154cfca8f.png">
<img width="1279" alt="Screen Shot 2022-11-06 at 23 40 45" src="https://user-images.githubusercontent.com/90776557/200196871-661b744d-9e4a-4a81-a9c1-3b569a4b3542.png">

# persistent - Mantian connection on 50% and 87.5% time 

<img width="477" alt="Screen Shot 2022-11-06 at 23 45 51" src="https://user-images.githubusercontent.com/90776557/200196919-9d274bbe-a020-4d13-bd6e-44b2af89b153.png">
<img width="1231" alt="Screen Shot 2022-11-06 at 23 46 42" src="https://user-images.githubusercontent.com/90776557/200196931-759fd53c-11a0-4ed5-a2ce-6e5d62139cce.png">

### reconnection
ר
<img width="848" alt="Screen Shot 2022-11-06 at 23 50 40" src="https://user-images.githubusercontent.com/90776557/200197086-af0e9dec-69b5-4c3c-9491-0c29f4e0b82e.png">




