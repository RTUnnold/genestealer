#!/usr/bin/env python3

import sys
import socket
import subprocess
import re

#basic scanning utility class
class scanner:
    #class doesn't need external arguments upon instantiation
    def __init__(self):
        #declare socket and regex matcher objects up here to save the headache
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_find = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        return

    #figure out what the current ip address is from the system
    def get_self_ip(self):
        """
        Function to obtain the current ip address of the attacking machine
        """
        curr_platform = sys.platform
        #windows calls it 'ipconfig' instead of 'ifconfig'
        if curr_platform != 'linux':
            return self.ip_find.findall(str(subprocess.check_output('ipconfig')))[0]
        else:
            return self.ip_find.findall(str(subprocess.check_output('ifconfig')))[0]

    #rudimentary ping scan
    def ping_scan(self, ip_addr):
        """
        Function to initiate an nmap ping scan on the immedate network of the attacking machine
        """
        #assume 24 bit netmask
        ip_mask = '.'.join(ip_addr.split('.')[:-1]) + '.0/24'
        cmd = ['nmap', '-sn', ip_mask]
        return self.ip_find.findall(subprocess.run(' '.join(cmd), shell=True)).remove(ip_addr)

    #use the socket library to attempt to connect to a port; returns 0 if successful
    def port_scan(self, target_ip, portnum):
        return self.sock.connect_ex((target_ip, portnum))

    def os_scan(self, target_ip):
        """
        Function to run a quick nmap OS detection scan
        """
        cmd = ['nmap', '-O', target_ip]
        output = subprocess.check_output(' '.join(cmd), shell=True)
        #OS info in most human readable format occurs 6 lines from the bottom
        sysline = output.decode('utf-8').split('\n')[-6]
