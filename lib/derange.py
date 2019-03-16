#!/usr/bin/env python
import threading
import os, sys
import subprocess
import logging
import ConfigParser
import time
import tarfile
import os.path
import json
import xml.etree.ElementTree as ET
import re
import yaml
import socket
import struct
from intspan import intspan
import os, sys
def derangify(nodes):
    data_array = []
    for node in nodes:
	match = re.match('(.*)\[(.*)\](\-.*)', node)
#	vsccwn[100-300]-brn.vscc.vrsn.com
#	^([a-zA-Z]+)(\d+)([a-zA-Z0-9-]+)(\..*)$', node
        if match:
            (prefix,nrange,suffix) = match.groups()
            length = 0
            if re.match('.*\-.*',nrange):
                (r1,r2) = nrange.split('-')
                length = len(str(r2))
            for num in intspan(nrange):
                data_array.append("%s%s%s" %(prefix,str(num).zfill(length),suffix))
        else:
            data_array.append(node)

    return data_array

def main():
  print derangify(sys.argv[1])

if __name__=="__main__":
  main()
