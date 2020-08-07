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

def id(reportjson,params,logger):

    """
    report id:id - return all results with specific ID and, in case of master_submission, the list of node without result
    report id:id#hostname - return one specific result of hostname selected by ID
    """

    if(params == None):
        return "ERROR - report id - expected id or id#hostname"

    hpc =[]
    all_res =[]
    hostname=False
    #check if there is only id parameter or also hostname and save the values in var
    if "#" in params:
        x = params.split("#")
        print(x)
        id = str(x[0])
        hostname=True
        hpc.append(x[1])
    else:
        id = params

    #the method scans the json dictonary and detects all object "master_submission" and "RESULT"
    for cur in reportjson["all"]:
            #for each object "master_submission" that have the same input id parameter, 
            # the process save the list of hostnames defined in "hpc", 
            # but only if there are not the hostname parameter in input            
        if "master_submission" in cur and not(bool(hostname)):
            cur_mst = cur["master_submission"]
            cur_id = cur_mst["id"]
            if cur_id == id:
                hpc = cur_mst["hpc"].encode("utf8").split(",")
        #for each objcet "RESULT" that have the same input id parameter, 
        #the process save the object in all_res
        elif "RESULT"  in cur:
            cur_id = cur["id"]
            if cur_id == id:
                all_res.append(cur)
    
    map_res={}
    list_noRes=[]
    #remove from hpc list all randomic hostname (defined by syntax <..> )
    new_hpc = [x for x in hpc if not x.startswith('<')]

    #for each hostname in the new_hpc list
    #the method define a new map (map_res) with all partial result of the node
    #create also a list of all hostname without partial result (list_noRes)
    for node in new_hpc:
        loc_res=""
        for res_node in all_res:
            if res_node["hostname"]==node:
                loc_res=res_node["RESULT"].encode("utf8")
                map_res[node]=loc_res
                continue
        if loc_res=="":
            list_noRes.append(node)

    #print all partial for each hostname and the list of all hostname not completed
    output=""
    output+="\n--------------- RESULT : "+str(len(map_res))
    for x in map_res:
        output+="\n"+str(x)+" : "+str(map_res[x]) 
    output+= "\n--------------- NO RESULT("+str(len(list_noRes))+"): "+str(utils.list_to_String(list_noRes,","))
    return output

####--------------------------------------------------------------------------------------------------------------

def node(reportjson,params,logger):

    """
     report node:hostname - return all checktests and results selected by hostname
     report node:hostname#checktest - return a specific (linpack or Stream, ..) checktest and results selected by hostname
    """

    if(params == None):
        return "ERROR - report node - expected hostname or hostname#checktest"

    all_res ={}
    checktest=False
    ctType=""

    #check if there is only hostname parameter or also checktest and than save the values in var
    if "#" in params:
        x = params.split("#")
        print(x)
        hostname = str(x[0])
        checktest=True
        ctType = x[1]
    else:
        hostname = params

    #the method scans the json dictonary and detects all object "RESULT" 
    #that have the hostname equals to the input and save in all_res only 
    for cur_res in reportjson["all"]:
        loc_res=""
        if "RESULT"  in cur_res:
            cur_node = cur_res["hostname"]
            if cur_node == hostname:
                loc_res=cur_res
                nameNode = cur_res["id"]+"_"+cur_res["hostname"]
                all_res[nameNode]=loc_res


    #print all result and checktest (specific or all) of hostname in input
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

def master(reportjson,params,logger):

    """
     report master:n - print last n master_submission [if n=0 --> all, def n = 1] 
    """
    output=""
    all_master= []

    #the method scans the json dictonary and detects all object "master_submission"
    for cur in reportjson["all"]:
        if "master_submission" in cur:
            all_master.append(cur["master_submission"])

    #parameter is optional, if not specified is set to 1, if 0 equals to all
    if(params==None):
        params=1
    else:
        params = int(params)

    all = True
    if params!=0:
        all=False
    

    #sort the master_submission list by descendent date    
    masterSorted =sorted(all_master, key = lambda i: i['Date'], reverse=True)

    count=0

    #print a determinated number of master_submission (see parameter) ordered by descendent date
    for x in masterSorted:
        output+="\nId: "+x["id"]+" - Date: "+x["Date"]+"\n\tarch: "+x["arch"]+"\n\tcheck: "+x["check"]+"\n\thpc:\n"
        hpcs = x["hpc"].split(",")

        for hpc in hpcs:
            output+="\t\t"+hpc+"\n"
        output+="\n"
        count+=1
        if not(all) and count>=params:
            break

    return output

####--------------------------------------------------------------------------------------------------------------

def checktest(reportjson,params,logger):

    """
     report checktest:checktest - return all partial of a specific checktest (id,hostname,checktest - (linpack or Stream, ..))
     report checktest:checktest#id - return all partial of a specific checktest (linpack or Stream, ..) selected by id(hostname,checktest)
    """

    if(params == None):
        return "ERROR - report checktest - expected checktest or checktest#id"
    all_res ={}

    onlyOneId=False
    specID=""

    #check if there is only checktest parameter or also id and save the values in var
    if "#" in params:
        x = params.split("#")
        print(x)
        ctType = str(x[0])
        onlyOneId=True
        specID = x[1]
    else:
        ctType = params

    #the method scans the json dictonary and detects all "PARTIAL" object selected by specific checktest (in input) 
    #and save this in all_res. If is specified also the id, save only partial with this id
    for cur_res in reportjson["all"]:
        loc_res=None
        if "PARTIAL" in cur_res: 
            partials = cur_res["PARTIAL"]
            for cur_p in partials:
                if ctType in cur_p:
                    nameNode = cur_res["id"]+"_"+cur_res["hostname"]
                    if not(onlyOneId) or (cur_res["id"]== specID):
                        loc_res=cur_res
                        all_res[nameNode]=loc_res


    #print all partial of specific checktest (and eventually specific id)
    output=""
    output+="\n--------------- Partial for checkTest "+ctType 
    if(onlyOneId):
        output+=" and ID "+specID
    outtest=""
    outresult=""
    for x in all_res:
        t = all_res[x]
        outresult="\nId: "+str(t["id"])+" - hostname "+str(t["hostname"])+" - Date: "+str(t["Date"])+"\n"
        outtest=""
        for p in t["PARTIAL"]:
            if p.keys()[0]== ctType:
                for s, sv in sorted(utils.get_iter_object_from_dictionary(p.values()[0])):
                    outtest += "\t\t"+s +" : "+str(sv)+"\n"
                outtest+="\n"
        if len(outtest)>0:
            output+=outresult+outtest
    return output
        
####--------------------------------------------------------------------------------------------------------------

def main(check_core):

    """
    Id
     report id:id - return all results with specific ID and, in case of master_submission, the list of node without result
     report id:id#hostname - return one specific result of hostname selected by ID
    Node
     report node:hostname - return all checktests and results selected by hostname
     report node:hostname#checktest - return a specific (linpack or Stream, ..) checktest and results selected by hostname
    Checktest 
     report checktest:checktest - return all partial of a specific checktest (id,hostname,checktest - (linpack or Stream, ..))
     report checktest:checktest#id - return all partial of a specific checktest (linpack or Stream, ..) selected by id(hostname,checktest)
    Master 
     report master:n - print last n master_submission [if n=0 --> all, def n = 1] 
    """

    # define logger
    logger = logging.getLogger(check_core.setting["logger_name"])
    logger.debug("Start REPORT") 

    #The structure of flag Report is optionName:parameter[#optionalParameter]
    reportSet = check_core.setting["report"]
    x = reportSet.split(":")
    optionName = x[0]
    parameters = None
    if(len(x)>1):
        parameters = x[1]
    logger.debug("OPTION: "+optionName+" - Parameters: "+str(parameters))

    #read the file defined in resultfile parameter and convert it in a json dictionary
    rep_jsonfile = check_core.setting["resultfile"]
    data = []
    with open(rep_jsonfile) as f:
        for line in f:
            data.append(json.loads(line))
    if not data:
        logger.critical("the file "+rep_jsonfile+" is empty")
        return

    reportjson = {}
    reportjson["all"]=data

    if reportjson == -999:
        logger.debug("ERROR - void file "+ rep_jsonfile)
    else:
        #if json dictionary is not empty, the function calls a specific method according to the optionName
        if "id"  in optionName: 
            logger.critical(id(reportjson,parameters,logger))
        elif "node"  in optionName: 
            logger.critical(node(reportjson,parameters,logger))
        elif "checktest" in optionName: 
            logger.critical(checktest(reportjson,parameters,logger))
        elif "master" in optionName: 
            logger.critical(master(reportjson,parameters,logger))
        else:
            logger.critical("Invalid setting for flag Report "+reportSet)
    logger.debug("End REPORT") 

####--------------------------------------------------------------------------------------------------------------
