#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Really Simple AREDN Load Test
This sciprt allows you to  simulate .

The way this works is, we look for localnode.local.mesh, find all connected nodes
then we loop over each connected node to find their neighbors, unless we have already
visted them.  And we continues on each loop in a very much brute force mannor
"""

import argparse
import os
import sys
from urllib import request
import json

__author__ = "Joe Porcelli, KT3I"
__copyright__ = "Copyright 2020, Joe Porcelli"
__credits__ = ["Author Name"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Joe Porcelli"
__email__ = "joe@kt3i.com"
__status__ = "Development"

parser = argparse.ArgumentParser(description='AREDN Mesh Load simulater.')

# Positional Arguments
parser.add_argument('-n', '--host',
                    help="Specify hostname")


args = parser.parse_args()


def getHostsFromMachine(hostname=None):
    if hostname is None:
        print("\t*** Error fetching hosts ***")
        return None

    print("Visiting %s" % (hostname))    
    
    nodes = []

    url = "http://%s/cgi-bin/sysinfo.json?hosts=1" % (hostname)

    try:
        node_info = json.loads(request.urlopen(url).read()) # 
        hosts = node_info['hosts']
        this_name = node_info['node']
        for host in hosts:
            icon = "-"
            msg = ""
            if host['name'] == this_name:
                icon = '*' 
                msg = "<-- This node"
            else: 
                nodes.append(host['name'])
            print("\t%s %s [%s] %s" % (icon, host['name'], host['ip'], msg))

    except:
       print("\t*** Error fetching hosts ***")
       return None
    
    return  {'name': this_name, 'hosts': nodes}


def remove_dupe_dicts(l):
    list_of_strings = [
        json.dumps(d, sort_keys=True)
        for d in l
    ]
    list_of_strings = set(list_of_strings)

    return [
        json.loads(s)
        for s in list_of_strings
    ]


def main():
    hosts = ["localnode.local.mesh"]
    if args.host:
        hosts = [args.host]
    
    visited = []

    while(len(hosts)>0):
        node = getHostsFromMachine(hostname=hosts.pop())
        try:
            visited.append(node['name'])
            hosts.extend(node['hosts'])
            hosts = remove_dupe_dicts(hosts)
        except:
            pass

        hosts = list(set(hosts) - set(visited))
        print(pprint(hosts))




if __name__ == '__main__':
    # while(1):
    main()