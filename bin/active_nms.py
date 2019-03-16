#! /usr/bin/env python

import requests
import pprint

pp = pprint.PrettyPrinter(indent=4)

req = requests.get("http://dilithiumblue-jt1.blue.ygrid.yahoo.com:8088/ws/v1/cluster/nodes")

#pp.pprint(req.json())

active_nodes = []
used_mem_total = 0
avail_mem_total = 0

rm_info = req.json()

for entry in rm_info["nodes"]["node"]:
  for val in entry:
   # pp.pprint(val)
    if val == "nodeHostName":
     # pp.pprint(val)
     # pp.pprint(entry[val])
      active_nodes.append(entry[val])
    if val == "usedMemoryMB":
      used_mem_total += entry[val]
    if val == "availMemoryMB":
      avail_mem_total += entry[val]

pp.pprint(active_nodes)

print "Number of active NMs: ", len(active_nodes)
print "used Mem total is: ", used_mem_total
print "avail Mem total is: ", avail_mem_total
print "Mem total is: ", avail_mem_total+used_mem_total
