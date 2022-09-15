#
# CHECK
#
# @authors : Adele Castellani
#

import logging
import json
from checklib.common import utils


def id(reportjson, params, logger):
    """
    report id:id - return all results with specific ID and, in case of master_submission, the list of node without result
    report id:id#hostname - return one specific result of hostname selected by ID
    """

    if params is None:
        return "ERROR - report id - expected id or id#hostname"

    hpc = []
    all_res = []
    hostname = False
    # check if there is only id parameter or also hostname and save the values in var
    if "#" in params:
        x = params.split("#")
        print(x)
        id_ = str(x[0])
        hostname = True
        hpc.append(x[1])
    else:
        id_ = params

    # the method scans the json dictonary and detects all object "master_submission" and "RESULT"
    for cur in reportjson["all"]:
        # for each object "master_submission" that have the same input id parameter,
        # the process save the list of hostnames defined in "hpc",
        # but only if there are not the hostname parameter in input
        if "master_submission" in cur and not (bool(hostname)):
            cur_mst = cur["master_submission"]
            cur_id = cur_mst["id"]
            if cur_id == id_:
                hpc = cur_mst["hpc"].split(",")
        # for each objcet "RESULT" that have the same input id parameter,
        # the process save the object in all_res
        elif "RESULT" in cur:
            cur_id = cur["id"]
            if cur_id == id_:
                all_res.append(cur)

    map_res = {}
    list_no_res = []
    # remove from hpc list all randomic hostname (defined by syntax <..> )
    new_hpc = [x for x in hpc if not x.startswith('<')]

    # for each hostname in the new_hpc list
    # the method define a new map (map_res) with all partial result of the node
    # create also a list of all hostname without partial result (list_noRes)
    for node_ in new_hpc:
        loc_res = ""
        for res_node in all_res:
            if res_node["hostname"] == node_:
                loc_res = res_node["RESULT"]
                map_res[node_] = loc_res
                continue
        if loc_res == "":
            list_no_res.append(node_)

    # case with only random nodes
    if len(new_hpc) == 0:
        for res_node in all_res:
            map_res[res_node["hostname"].encode("utf8")] = res_node["RESULT"].encode("utf8")
            # print("loc "+res_node["hostname"].encode("utf8"))

    # print all partial for each hostname and the list of all hostname not completed
    output = ""
    output += f"\n--------------- RESULT : {len(map_res)}"

    for x in map_res:
        output += f"\n{x} : {map_res[x]}"

    output += f"\n--------------- NO RESULT({len(list_no_res)}): {utils.list_to_String(list_no_res, ',')}"

    return output


####--------------------------------------------------------------------------------------------------------------

def node(reportjson, params, logger):
    """
     report node:hostname - return all checktests and results selected by hostname
     report node:hostname#checktest - return a specific (linpack or Stream, ..) checktest and results selected by hostname
    """

    if params is None:
        return "ERROR - report node - expected hostname or hostname#checktest"

    all_res = {}
    checktest_ = False
    ct_type = ""

    # check if there is only hostname parameter or also checktest and than save the values in var
    if "#" in params:
        x = params.split("#")
        print(x)
        hostname = str(x[0])
        checktest_ = True
        ct_type = x[1]
    else:
        hostname = params

    # the method scans the json dictonary and detects all object "RESULT"
    # that have the hostname equals to the input and save in all_res only
    for cur_res in reportjson["all"]:

        if "RESULT" in cur_res:
            cur_node = cur_res["hostname"]
            if cur_node == hostname:
                loc_res = cur_res
                node_name = cur_res["id"] + " @ " + cur_res["hostname"]
                all_res[node_name] = loc_res

    # print all result and checktest (specific or all) of hostname in input
    output = ""
    output += f"\n--------------- Node with hostname {hostname}"

    if checktest_:
        output += f" and checktest {ct_type}"

    for x in all_res:
        t = all_res[x]
        outresult = f"\nId: {x} - Date: {t['date']} - Result: {t['RESULT']}\n"
        outtest = ""
        for p in t["PARTIAL"]:
            # print(type(p))
            if not checktest_ or list(p.keys())[0] == ct_type:
                outtest += f"\t{list(p.keys())[0]}\n"
                for s, sv in sorted(utils.get_iter_object_from_dictionary(list(p.values())[0])):
                    outtest += f"\t\t{s} : {sv}\n"

        if len(outtest) > 0:
            output += outresult + outtest

    return output


####--------------------------------------------------------------------------------------------------------------

def master(reportjson, params, logger):
    """
     report master:n - print last n master_submission [if n=0 --> all, def n = 1] 
    """
    output = ""
    all_master = []

    # the method scans the json dictonary and detects all object "master_submission"
    for cur in reportjson["all"]:
        if "master_submission" in cur:
            all_master.append(cur["master_submission"])

    # parameter is optional, if not specified is set to 1, if 0 equals to all
    if params is None:
        params = 1
    else:
        params = int(params)

    all_ = True
    if params != 0:
        all_ = False

    # sort the master_submission list by descendent date
    master_sorted = sorted(all_master, key=lambda i: i['date'], reverse=True)

    count = 0

    # print a determinated number of master_submission (see parameter) ordered by descendent date
    for x in master_sorted:
        output += f"\nId: {x['id']} - Date: {x['date']}\n\tarch: {x['arch']}\n\tcheck: {x['check']}\n\thpc:\n"
        hpcs = x["hpc"].split(",")

        for hpc in hpcs:
            output += f"\t\t{hpc}\n"
        output += "\n"
        count += 1
        if not all_ and count >= params:
            break

    return output


####--------------------------------------------------------------------------------------------------------------

def checktest(reportjson, params, logger):
    """
    report checktest:checktest - return all partial of a specific checktest (id,hostname,checktest - (linpack or
    Stream, ..)) report checktest:checktest#id - return all partial of a specific checktest (linpack or Stream,
    ..) selected by id(hostname,checktest)
    """

    if params is None:
        return "ERROR - report checktest - expected checktest or checktest#id"
    all_res = {}

    only_one_id = False
    spec_id = ""

    # check if there is only checktest parameter or also id and save the values in var
    if "#" in params:
        x = params.split("#")
        print(x)
        ct_type = str(x[0])
        only_one_id = True
        spec_id = x[1]
    else:
        ct_type = params

    # the method scans the json dictonary and detects all "PARTIAL" object selected by specific checktest (in input)
    # and save this in all_res. If is specified also the id, save only partial with this id
    for cur_res in reportjson["all"]:
        if "PARTIAL" in cur_res:
            partials = cur_res["PARTIAL"]
            for cur_p in partials:
                if ct_type in cur_p:
                    node_name = cur_res["id"] + "_" + cur_res["hostname"]
                    if not only_one_id or (cur_res["id"] == spec_id):
                        loc_res = cur_res
                        all_res[node_name] = loc_res

    # print all partial of specific checktest (and eventually specific id)
    output = ""
    output += "\n--------------- Partial for checkTest " + ct_type

    if only_one_id:
        output += " and ID " + spec_id

    for x in all_res:
        t = all_res[x]
        outresult = f"\nId: {t['id']} - hostname {t['hostname']} - Date: {t['date']}\n"
        outtest = ""

        for p in t["PARTIAL"]:
            if list(p.keys())[0] == ct_type:
                for s, sv in sorted(utils.get_iter_object_from_dictionary(list(p.values())[0])):
                    outtest += f"\t\t{s} : {sv}\n"
                outtest += "\n"

        if len(outtest) > 0:
            output += outresult + outtest

    return output


####--------------------------------------------------------------------------------------------------------------

def main(check_core):
    """
    - ID
        report id:<id> - return all results with specific ID and, in case of master_submission, the list of nodes
        without result;
        report id:<id>#<hostname> - return one specific result of hostname selected by ID;

    - Node
        report node:<hostname> - return all checktests and results selected by hostname;
        report node:<hostname>#<checktest> - return a specific (LINPACK or STREAM, ...) checktest and results selected
        by hostname;

    - Checktest
        report checktest:<checktest> - return all partial of a specific checktest (id,hostname,checktest -
        (LINPACK or STREAM, ...));
        report checktest:<checktest>#<id> - return all partial of a specific checktest (LINPACK or STREAM, ...)
        selected by id(hostname,checktest);

    - Master
        report master:<n> - print last <n> master_submission [if n==0 --> all, def n = 1].
    """

    # define logger
    logger = logging.getLogger(check_core.setting["logger_name"])
    logger.debug("Start REPORT")

    # The structure of flag Report is optionName:parameter[#optionalParameter]
    report_set = check_core.setting["report"]
    x = report_set.split(":")
    option_name = x[0]
    parameters = None
    if len(x) > 1:
        parameters = x[1]

    logger.debug("OPTION: " + option_name + " - Parameters: " + str(parameters))

    # read the file defined in resultfile parameter and convert it in a json dictionary
    rep_jsonfile = check_core.setting["resultfile"]
    data = []
    with open(rep_jsonfile) as f:
        for line in f:
            data.append(json.loads(line))
    if not data:
        logger.critical("the file " + rep_jsonfile + " is empty")
        return

    json_report = dict()
    json_report["all"] = data

    if json_report == -999:
        logger.debug("ERROR - void file " + rep_jsonfile)
    else:
        # if json dictionary is not empty, the function calls a specific method according to the optionName
        if "id" in option_name:
            logger.critical(id(json_report, parameters, logger))
        elif "node" in option_name:
            logger.critical(node(json_report, parameters, logger))
        elif "checktest" in option_name:
            logger.critical(checktest(json_report, parameters, logger))
        elif "master" in option_name:
            logger.critical(master(json_report, parameters, logger))
        else:
            logger.critical("Invalid setting for flag Report " + report_set)

    logger.debug("End REPORT")

####--------------------------------------------------------------------------------------------------------------
