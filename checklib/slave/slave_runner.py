#
# CHECK
#
# @authors : Eric Pascolo
#

import traceback
import logging
import subprocess
import json
from checklib.core import checkobj_result
from checklib.slave import multibenchmark
from checklib.common import utils


####--------------------------------------------------------------------------------------------------------------

def installator(check_core):

    """
    CHECK's installator function, provide the launch of installtion function to all checktest selected.
    """
    logger = logging.getLogger(check_core.setting["logger_name"])

    for cs in check_core.checktests:

        logger.debug("--------------- CheckTest installation: "+cs.get_name())
        try:
            cs.install()
        except:
            logger.CRITICAL("Installation FAIL")
            traceback.print_exc()

####--------------------------------------------------------------------------------------------------------------

def worker(check_core):

    """
    CHECK's worker function, this main launch all checkstest and after collect the resutls for single node
    and provide to call Multibenchmark node analysis.
    """

    logger = logging.getLogger(check_core.setting["logger_name"])
    # checktest result collection list
    check_results = []

    # loop for check test launch, each benchmark will be completed in 4 step, launched separatelly
    for cs in check_core.checktests:
        logger.debug("--------------- CheckTest : "+cs.get_name())
        try:
            cs.preproc()
            cs.run()
            cs.postproc()
            check_results.append(cs.comparison())
        except:
            check_results.append(checkobj_result.check_result(cs.get_name(),"FAIL"))
            traceback.print_exc()

    # try to get name of the node through hostname command
    try:
        p = subprocess.Popen("hostname",stdout=subprocess.PIPE, stderr=None)
        out,err = p.communicate()
        nameofnode = utils.remove_newline_in(out)
    except:
        nameofnode = "NOTDEFINED"
        logger.critical("WARNING : impossible to get hostname")

    # multibenchmark analyis call
    nodemark = multibenchmark.analisys(check_core,check_results)

    # log partial result of single benchmark
    res_file_json = {"id":check_core.setting["id"],"hostname":str(nameofnode)}
    if "master_id" in check_core.setting:
        res_file_json.update({"slave_mode":True})

    #partial log on logger and json file
    for cr in check_results:
        logger.info( cr._benchmark + " @ "+str(nameofnode)+" --> "+ \
                                        str(cr.measure)+" "+cr.udm+" "+cr.status )
        res_file_json.update({cr._benchmark:{"check":cr._benchmark,
                                         "value":str(cr.measure),
                                         "udm":cr.udm,
                                         "status":cr.status}})

    # log multibenchmark analysis result
    logger.critical(str(nameofnode) +"  "+ nodemark)
    res_file_json.update({"RESULT":nodemark})
    
    #write result dictionary on check_result file
    out_file = open(check_core.setting["resultfile"],"a+")
    json.dump(res_file_json,out_file,indent=2)
    out_file.write("\n")
    out_file.close()

####--------------------------------------------------------------------------------------------------------------

def main(check_core):

    """
    CHECK's launch core function, select if launch benchmark or installation
    """

    # define logger
    logger = logging.getLogger(check_core.setting["logger_name"])
    logger.debug("Star slave")

    #choose if install or launch checktest
    if "install" in check_core.setting:

        installator(check_core)

    else:

        worker(check_core)

####--------------------------------------------------------------------------------------------------------------
