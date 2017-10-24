#!/usr/bin/python
from scapy.all import *

#Name of the interface we will be scanning for probe requests. 
interface = "mon0"

#List of hosts that have already been observed probing the network.
#Will ensure the same data is not read.
observedclients = []

#Function that is called each time a packet is recieved.
def sniffmgmt(p):
	#contains the probe request type
	stamgmtstypes = (0,2,4)

	if p.haslayer(Dot11):
		#Checking that this is a management frame(request probe)
		if p.type == 0 and p.subtype in stamgmtstypes:
			if p.subtype == 4:
				#printing out the MAC address of clients that have
				#not been printed. Will add clients not observed to
				#a list
				if p.addr2 not in observedclients:
					print vendor(p.addr2), p.addr2
					observedclients.append(p.addr2)

def vendor(addr):
	lists = open('/root/Desktop/vendorMacs.csv','r')
	for line in lists:	
		vendorNames = line.split(",")
		ID = addr[:8]
		if vendorNames[0] == ID:
			return vendorNames[1]
#sniffmgmt function complete
#invoking the sniff function to tell scapy to call sniffmgmt() for each packet
#recieved.
sniff(iface = interface, prn = sniffmgmt)
