#
# CHECK
#
# @authors : Eric Pascolo
#

import traceback
import logging
import subprocess
import json
import platform
from datetime import datetime
from checklib.common import utils
from checklib.inout import file_reader

def result(reportjson,id,logger):


    #rep_jsonfile = check_core.setting["resultfile"]
    master = 0
    result = 0
    count  = 0
    other = 0
    hpc =[]
    all_res =[]
    # if reportjson == -999:
    #     logger.debug("ERROR - void file "+ rep_jsonfile)
    # else:
    for cur_res in reportjson["all"]:
            
        if "master_submission" in cur_res:
            cur_mst = cur_res["master_submission"]
            cur_id = cur_mst["id"]
            if cur_id == id:
                #print("json ",count," is MASTER") 
                hpc = cur_mst["hpc"].encode("utf8").split(",")
                master += 1
            count += 1

        elif "RESULT"  in cur_res:
            cur_id = cur_res["id"]
            if cur_id == id:
                #print("json ",count," is RESULT") 
                result += 1
                all_res.append(cur_res)
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
    #logger.debug("\n--------------- RESULT : "+str(len(map_res)))
    for x in map_res:
        output+="\n"+str(x)+" : "+str(map_res[x]) 
        #logger.debug(str(x)+" : "+str(map_res[x]) )
    #print (map_res)
    output+= "\n--------------- NO RESULT("+str(len(list_noRes))+"): "+str(utils.list_to_String(list_noRes,","))
    #logger.debug("\n--------------- NO RESULT("+str(len(list_noRes))+")"+str(list_noRes))
    return output

####--------------------------------------------------------------------------------------------------------------

def node(reportjson,hostname,logger):


    #rep_jsonfile = check_core.setting["resultfile"]
    result = 0
    count  = 0
    other = 0
    all_res ={}
    # if reportjson == -999:
    #     logger.debug("ERROR - void file "+ rep_jsonfile)
    # else:
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
    # map_res={}
    # list_noRes=[]
    # for node in hpc:
    #     loc_res=""
    #     for res_node in all_res:
    #         if res_node["hostname"]==node:
    #             loc_res=res_node["RESULT"].encode("utf8")
    #             map_res[node]=loc_res
    #             continue
    #     if loc_res=="":
    #         list_noRes.append(node)
    output=""
    output+="\n--------------- Node with hostname "+hostname+": "+str(len(all_res))
    #logger.debug("\n--------------- RESULT : "+str(len(map_res)))
    for x in all_res:
        t = all_res[x]
        output+="\nId: "+str(x)+" - Result: "+str(t["RESULT"])+"\n"
        for p in t["PARTIAL"]:
            output += "\t"+p.keys()[0]+"\n"
            for s, sv in sorted(utils.get_iter_object_from_dictionary(p.values()[0])):
                output += "\t\t"+s +" : "+str(sv)+"\n"
        # output+="\n"+checkparameter_string+"\n"
    return output
        
####--------------------------------------------------------------------------------------------------------------


def main(check_core):

    """
    *report id:id - return all result for master_submission and list of node without result
     report id:id#hostname - return one specific node result for master_submission
    *report node:hostname - return all checktest and result for a specific hostname
     report node:hostname#checktest - return a specific (linpack or Stream, ..) checktest and result for a specific hostname
     report checktest:checktest - return all partial of a specific checktest (id,hostname,checktest)
     report checktest:checktest#id - return all partial of a specific checktest and id(hostname,checktest)
     report master:n - print last n master_submission if 0 = all def = 1 
    """

    # define logger
    logger = logging.getLogger(check_core.setting["logger_name"])
    logger.debug("Start REPORT") #check_core.setting["resultfile"]
    option = check_core.setting["report"]
    x = option.split(":")
    rep_option = x[0]
    rep_id = x[1]
    logger.debug("OPTION: "+rep_option+" - ID: "+rep_id)
    rep_jsonfile = check_core.setting["resultfile"]
    reportjson = file_reader.json_reader(rep_jsonfile)
    if reportjson == -999:
        logger.debug("ERROR - void file "+ rep_jsonfile)
    else:
        if "id"  in rep_option: 
            logger.critical(result(reportjson,rep_id,logger))
        if "node"  in rep_option: 
            logger.critical(node(reportjson,rep_id,logger))
        else:
            logger.critical("Invalid option "+option)


####--------------------------------------------------------------------------------------------------------------
