#!/usr/bin/env python
import intspan
import re
def rangify(nodes):
    data_array = []
    info_hash = dict()
    for node in nodes:
	match = re.match('^([a-zA-Z]+)(\d+)([a-zA-Z0-9-]+)(\..*)$', node)
        if match:
          (prefix,number,suffix,random)=match.groups()
          if suffix not in info_hash.keys(): info_hash[suffix] = dict()
          if prefix not in info_hash[suffix].keys(): info_hash[suffix][prefix] = dict()
          info_hash[suffix][prefix][number] = 1

          if re.match('.*\[.*\].*', node):
            logging.warn(node+" : already in range")
            data_array.append(node)

    for suffix in sorted(info_hash.keys()):
        for prefix in sorted(info_hash[suffix].keys()):
            length = 0
            for num in info_hash[suffix][prefix].keys():
                length = len(str(num))
            ints = []
            ints = [int(x) for x in info_hash[suffix][prefix].keys()]
            ints.sort()
            min = -1
            max = 0
            last = -1
            for i in ints:
                if min == -1 or i < min:
                    min = i
                else:
                    if last > -1 and i != int(last + 1):
                        if min == max:
                            data_array.append("%s%s%s" %(prefix,str(max).zfill(length),suffix))
                        else:
                            data_array.append("%s[%s-%s]%s" %(prefix,str(min).zfill(length),str(max).zfill(length),suffix))
                        min = i
                        max = i
                if i > max: max = i
                last = i
            if min == max:
                data_array.append("%s%s%s" %(prefix,str(max).zfill(length),suffix))
            else:
                data_array.append("%s[%s-%s]%s" %(prefix,str(min).zfill(length),str(max).zfill(length),suffix))
    return data_array
     
