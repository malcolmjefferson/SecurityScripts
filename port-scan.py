#!/bin/bash/env python

import nmap
import optparse

def nmapScan(tgtHost, tgtPort):
	nmScan = nmap.PortScanner()
	nmScan.scan(tgtHost, tgtPort)
	state=nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
	print " [*] ",tgtHost,"tcp/",tgtPort," ",state
def main():
#	parser = optparse.OptionParser('usage%prog '+\
#	'-H <target Host> -p <target port>')
#	parser.add_option('-H', dest='tgtHost', type='string',\
#	help='specify target host')
#	parser.add_option('-p', dest='tgtport', type='string', \
#	help='specify target port[s] separated by comma')
#	(options, args) = parser.parse_args()
#	tgtHost = options.tgtHost
#	tgtPorts= str(options.tgtPort).split(', ')
#	exit(0)
#	for tgtPort in tgtPorts:
#		nmapScan(tgtHost, tgtPort)

	Hostname = raw_input("Enter the ip address:")
	try:
		ports = raw_input("Enter the port[s] you wish to scan(with a comma separating them):")
		tgtPorts = ports.split(", ")
		print (tgtPorts)
		for port in tgtPorts:
			print port
			nmapScan(Hostname, port)
	except Exception, e:
		print "There was a problem...",e
if __name__ == "__main__":
	main()
