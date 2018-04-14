#!/usr/bin/python36

import ipaddress 

ip1=input("startip:")

ip2=input("endip:")

startip = ipaddress.IPv4Address(ip1)

endip = ipaddress.IPv4Address(ip2)


cidr = [ipaddr for ipaddr in ipaddress.summarize_address_range(startip, endip)]

for k, v in enumerate(cidr):
    iplist = v
    print(iplist)