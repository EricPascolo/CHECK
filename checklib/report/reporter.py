#
# CHECK
#
# @authors : Adele Castellani
#

import traceback
import logging
import subprocess
import json
import platform
from datetime import datetime
from checklib.common import utils
from checklib.inout import file_reader

def id(reportjson,opt,logger):

    """
    report id:id - return all result for master_submission and list of node without result
    report id:id#hostname - return one specific node result for master_submission
    """
    if(opt == None):
        return "ERROR - report id - expected id or id#hostname"
    master = 0
    result = 0
    count  = 0
    other = 0
    hpc =[]
    all_res =[]
    hostname=False
    if "#" in opt:
        x = opt.split("#")
        print(x)
        id = str(x[0])
        hostname=True
        hpc.append(x[1])
    else:
        id = opt

    for cur in reportjson["all"]:
            
        if "master_submission" in cur:
            cur_mst = cur["master_submission"]
            cur_id = cur_mst["id"]
            if cur_id == id and not(bool(hostname)):
                #print("json ",count," is MASTER") 
                hpc = cur_mst["hpc"].encode("utf8").split(",") ##
                master += 1
            count += 1

        elif "RESULT"  in cur:
            cur_id = cur["id"]
            if cur_id == id:
                #print("json ",count," is RESULT") 
                result += 1
                all_res.append(cur)
            count += 1 
        else:
            #print("json ",count," is OTHER") 
            count += 1  
            other += 1
    #print("TOT ",count," - Master: ",master," - Result ",result," size ", len(all_res))
    #print(hpc)
    map_res={}
    list_noRes=[]
    for node in hpc:
        loc_res=""
        for res_node in all_res:
            if res_node["hostname"]==node:
                loc_res=res_node["RESULT"].encode("utf8")
                map_res[node]=loc_res
                continue
        if loc_res=="":
            list_noRes.append(node)
    output=""
    output+="\n--------------- RESULT : "+str(len(map_res))
    for x in map_res:
        output+="\n"+str(x)+" : "+str(map_res[x]) 
    #print (map_res)
    output+= "\n--------------- NO RESULT("+str(len(list_noRes))+"): "+str(utils.list_to_String(list_noRes,","))
    return output

####--------------------------------------------------------------------------------------------------------------

def node(reportjson,opt,logger):

    """
    *report node:hostname - return all checktest and result for a specific hostname
     report node:hostname#checktest - return a specific (linpack or Stream, ..) checktest and result for a specific hostname
    """

    if(opt == None):
        return "ERROR - report node - expected hostname or hostname#checktest"
    result = 0
    count  = 0
    other = 0
    all_res ={}

    checktest=False
    ctType="all"
    if "#" in opt:
        x = opt.split("#")
        print(x)
        hostname = str(x[0])
        checktest=True
        # hpc.append(x[1])
        ctType = x[1]
    else:
        hostname = opt

    for cur_res in reportjson["all"]:

        loc_res=""
        if "RESULT"  in cur_res:
            cur_node = cur_res["hostname"]
            if cur_node == hostname:
                #print("json ",count," is RESULT") 
                result += 1
                loc_res=cur_res
                all_res[cur_res["id"]]=loc_res
            count += 1 
        else:
            #print("json ",count," is OTHER") 
            count += 1  
            other += 1
    #print("TOT ",count," - Master: ",master," - Result ",result," size ", len(all_res))
    #print(hpc)

    output=""
    output+="\n--------------- Node with hostname "+hostname 
    if(checktest):
        output+=" and checktest "+ctType
    outtest=""
    outresult=""
    for x in all_res:
        t = all_res[x]
        outresult="\nId: "+str(x)+" - Date: "+str(t["Date"])+" - Result: "+str(t["RESULT"])+"\n"
        outtest=""
        for p in t["PARTIAL"]:
            if not(checktest) or p.keys()[0]== ctType:
                outtest += "\t"+p.keys()[0]+"\n"
                for s, sv in sorted(utils.get_iter_object_from_dictionary(p.values()[0])):
                    outtest += "\t\t"+s +" : "+str(sv)+"\n"
        if len(outtest)>0:
            output+=outresult+outtest
    return output
        
####--------------------------------------------------------------------------------------------------------------

def master(reportjson,logger,opt):

    """
    Master 
     report master:n - print last n master_submission [if n=0 --> all, def n = 1] 
    """
    output=""
    all_master= []

    for cur in reportjson["all"]:
        if "master_submission" in cur:
            #all_master[cur["master_submission"]["Date"]]=(cur["master_submission"])
            all_master.append(cur["master_submission"])

    # for s, sv in sorted(utils.get_iter_object_from_dictionary(all_master),all_master.keys(),reverse=True):
    #     print("\t\t"+s +" : "+str(sv))
    # for s, sv in sorted(utils.get_iter_object_from_dictionary(all_master)):
    #     outtest += "\t\t"+s +" : "+str(sv)+"\n"
    
    # print(outtest)
    # for x in all_master:
    #     # output+="\n"+str(x)+" : "+str(all_master[x]) 
    #     output+= "\n"+str(x).encode("utf8")
    if(opt==None):
        opt=1
    else:
        opt = int(opt)
    a =sorted(all_master, key = lambda i: i['Date'], reverse=True)
    all = True
    if opt!=0:
        all=False
    count=0
    for x in a:
        output+="\nId: "+x["id"]+" - Date: "+x["Date"]+"\n\tarch: "+x["arch"]+"\n\tcheck: "+x["check"]+"\n\thpc:\n"
        hpcs = x["hpc"].split(",")
        for hpc in hpcs:
            output+="\t\t"+hpc+"\n"
        output+="\n"
        count+=1
        if not(all) and count>=opt:
            break

    return output

####--------------------------------------------------------------------------------------------------------------


def main(check_core):

    """
    Id
     report id:id - return all result for master_submission and list of node without result
     report id:id#hostname - return one specific node result for master_submission
    Node
     report node:hostname - return all checktest and result for a specific hostname
     report node:hostname#checktest - return a specific (linpack or Stream, ..) checktest and result for a specific hostname
    Checktest 
    *report checktest:checktest - return all partial of a specific checktest (id,hostname,checktest)
    *report checktest:checktest#id - return all partial of a specific checktest and id(hostname,checktest)
    Master 
     report master:n - print last n master_submission [if n=0 --> all, def n = 1] 
    """

    # define logger
    logger = logging.getLogger(check_core.setting["logger_name"])
    logger.debug("Start REPORT") 
    option = check_core.setting["report"]
    x = option.split(":")
    rep_option = x[0]
    rep_id = None
    if(len(x)>1):
        rep_id = x[1]
    logger.debug("OPTION: "+rep_option+" - ID: "+str(rep_id))
    rep_jsonfile = check_core.setting["resultfile"]


    data = []
    with open(rep_jsonfile) as f:
        for line in f:
            data.append(json.loads(line))

    reportjson = {}
    reportjson["all"]=data

    if reportjson == -999:
        logger.debug("ERROR - void file "+ rep_jsonfile)
    else:
        if "id"  in rep_option: 
            logger.critical(id(reportjson,rep_id,logger))
        elif "node"  in rep_option: 
            logger.critical(node(reportjson,rep_id,logger))
        elif "master" in rep_option: 
            logger.critical(master(reportjson,logger,rep_id))
        else:
            logger.critical("Invalid option "+option)


####--------------------------------------------------------------------------------------------------------------
