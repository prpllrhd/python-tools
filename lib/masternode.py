#!/home/y/bin/python

import threading
import os, sys
import subprocess
import logging
import time
import tarfile
import os.path
import math
import Ygrid.Common.Utilities as Util
from Ygrid.Common.Collection import RunTasks as RT
from Ygrid.Common.HTTPlib import HTTP
from Ygrid.ClusterTools import Cluster


class Namenode():
    
    def __init__(self,cluster_name):
        logging.debug("Namenode Constructor : "+cluster_name)
        self.cluster_name = cluster_name
        (self.cluster, self.colo) = cluster_name.split('.')
        self.__info = dict()

    def computeInfo(self):
        http_req = HTTP()
        for inst in ('ha1','ha2'):
            hostname = self.cluster+self.colo+"-nn1-"+inst+"."+self.colo+".ygrid.yahoo.com"
            try:
                retval, data = http_req.get("http://"+hostname+":50070/jmx?qry=Hadoop:*")
                status, jsondata = Util.isJSON(data)
            except:
                raise Exception("Unexpected error, while fetching Namenode status : "+self.cluster_name)
            else:
                if retval == 200 and status:
                    self.__info[hostname] = dict()
                    for metric in jsondata['beans']:
                        if metric['name'] == 'Hadoop:service=NameNode,name=NameNodeInfo':
                            status, self.__info[hostname]['LiveNodes'] = Util.isJSON(metric['LiveNodes'])
                            status, self.__info[hostname]['DeadNodes'] = Util.isJSON(metric['DeadNodes'])
                            status, self.__info[hostname]['DecomNodes'] = Util.isJSON(metric['DecomNodes'])
                            self.__info[hostname]['TotalSpace'] = metric['Total']
                            self.__info[hostname]['UsedSpace'] = metric['Used']
                            self.__info[hostname]['Version'] = metric['Version']
                            self.__info[hostname]['Safemode'] = metric['Safemode']
                            self.__info[hostname]['TotalBlocks'] = metric['TotalBlocks']
                            self.__info[hostname]['TotalFiles'] = metric['TotalFiles']
                            self.__info[hostname]['Safemode'] = metric['Safemode']
                            self.__info[hostname]['MissingBlocks'] = metric['NumberOfMissingBlocks']

                        elif metric['name'] == 'Hadoop:service=NameNode,name=FSNamesystemMetric':
                            self.__info[hostname]['MissingBlocks'] = metric['MissingBlocks'];
                            self.__info[hostname]['UnderReplicatedBlocks'] = metric['UnderReplicatedBlocks'];

                        elif metric['name'] == 'Hadoop:service=NameNode,name=FSNamesystem':
                            self.__info[hostname]['MissingBlocks'] = metric['MissingBlocks'];
                            self.__info[hostname]['UnderReplicatedBlocks'] = metric['UnderReplicatedBlocks'];
                            
                        elif metric['name'] == 'Hadoop:service=NameNode,name=NameNodeStatus':
                            self.__info[hostname]['State'] = metric['State'];
                            
                        elif metric['name'] == 'Hadoop:service=NameNode,name=FSNamesystemState':
                            self.__info[hostname]['FSState'] = metric['FSState'];
                            self.__info[hostname]['UnderReplicatedBlocks'] = metric['UnderReplicatedBlocks'];
                            self.__info[hostname]['CapacityTotal'] = metric['CapacityTotal'];
                            self.__info[hostname]['CapacityUsed'] = metric['CapacityUsed'];
                            self.__info[hostname]['CapacityRemaining'] = metric['CapacityRemaining'];
                            self.__info[hostname]['CapacityUsedPercent'] = math.ceil((metric['CapacityUsed']*100)/metric['CapacityTotal']);
                else:
                    raise Exception("Unable to query "+self.cluster+"."+self.colo+" cluster namenode")

    def getInfo(self):
        return self.__info
                
class ResourceManager():
    
    def __init__(self,cluster_name):
        self.cluster_name = cluster_name
        (self.cluster, self.colo) = cluster_name.split('.')
        self.__info = dict()
        self.rm_api = ['/ws/v1/cluster/info','/ws/v1/cluster/metrics','/ws/v1/cluster/nodes','/ws/v1/cluster/scheduler']

    def computeInfo(self):
        hostname = self.cluster+self.colo+"-jt1."+self.colo+".ygrid.yahoo.com"
        http_req = HTTP()
        info = dict()
        for api in self.rm_api:
            try:
                retval, data = http_req.get("http://"+hostname+":8088"+api)
                status, info = Util.isJSON(data)
                if status == False:
                    info = util.xmlString(data)
            except:
                raise Exception("Unexpected error, while fetching RM status : "+self.cluster_name)
            else:
                if retval == 200 and status:
                    for key in info.keys():
                        if key == 'nodes':
                            self.__info['nodes'] = info[key]['node']
                        else:
                            self.__info[key] = info[key]

    def getClusters(self):
        return self.__cluster_data.keys()

    def getInfo(self):
        return self.__info
    
   
