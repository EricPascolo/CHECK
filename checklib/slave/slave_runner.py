#
# CHECK
#
# @authors : Eric Pascolo
#

import traceback
import logging
import subprocess
import json
from datetime import datetime
from checklib.core import checkobj_result
from checklib.slave import multibenchmark
from checklib.common import utils
from checklib.scheduler import whatscheduler


####--------------------------------------------------------------------------------------------------------------

def installator(check_core):

    """
    CHECK's installator function, provide the launch of installtion function to all checktest selected.
    """
    logger = logging.getLogger(check_core.setting["logger_name"])

    for cs in check_core.checktests:

        logger.debug("--------------- CheckTest installation: "+cs.get_name())
        try:
            cs.install(check_core.setting["install"])
        except:
            logger.critical("Installation FAIL")
            #traceback.print_exc()

####--------------------------------------------------------------------------------------------------------------

def worker(check_core):

    """
    CHECK's worker function, this main launch all checkstest and after collect the resutls for single node
    and provide to call Multibenchmark node analysis.
    """

    logger = logging.getLogger(check_core.setting["logger_name"])
    # checktest result collection list
    #check_results = []

    # loop for check test launch, each benchmark will be completed in 4 step, launched separatelly
    for cs in check_core.checktests:
        logger.debug("--------------- CheckTest : "+cs.get_name())
        try:
            cs.preproc()
            cs.run()
            cs.postproc()
            cs.comparison()
            #check_results.append(cs.result)
        except:
            #check_results.append(checkobj_result.check_result(cs.get_name(),"FAIL"))
            traceback.print_exc()

    #get scheduler env
    resources = whatscheduler.check_installed_scheduler(check_core.setting).get_job_resources()
    
    #  get name of the node 
    nameofnode = utils.get_name_of_nodes(resources) #platform.node()

    # multibenchmark analyis call
    nodemark = multibenchmark.analisys(check_core)

    # log partial result of single benchmark
    res_file_json = {"id":check_core.setting["id"],"hostname":str(nameofnode)}
    if "master_id" in check_core.setting:
        res_file_json.update({"slave_mode":True})

    res_partial_list = []
    #partial log on logger and json file
    for cs in check_core.checktests:
        logger.info(str(nameofnode)+" - " \
                        +str(cs.get_name()) + " @ "\
                        +cs.target_arch \
                        +" --> " \
                        +str(cs.result.measure)+" " \
                        +cs.result.udm+" " \
                        +cs.result.status )

        res_partial_list.append({cs.get_name():{"arch":cs.target_arch, \
                                         "value":str(cs.result.measure), \
                                         "unit":cs.result.udm, \
                                         "status":cs.result.status}})

    # log multibenchmark analysis result
    logger.critical(str(nameofnode) +"  "+ nodemark)
    res_file_json.update({"PARTIAL":res_partial_list})
    res_file_json.update({"RESULT":nodemark})
    res_file_json.update({"date":str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))})
    
    #write result dictionary on check_result file
    out_file = open(check_core.setting["resultfile"],"a+")
    json.dump(res_file_json,out_file,sort_keys=True)
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
