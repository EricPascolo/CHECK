#
# CHECK
#
# @authors : Eric Pascolo
#

import traceback
import logging
import subprocess
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

    #open last result in checkresult file

    out_file = open(check_core.setting["resultfile"],"a+")

    # log partial result of single benchmark
    for cr in check_results:
        logger.info(" @ "+str(nameofnode)+" --> "+ \
                                        str(cr.measure)+" "+cr.udm+" "+cr.status )
        out_file.write(check_core.setting["id"]+" @ "+str(nameofnode) +" [PARTIAL] "+str(cr.measure)+" "+cr.udm+" "+cr.status+"\n")

    # log multibenchmark analysis result
    logger.critical(str(nameofnode) +"  "+ nodemark)
    out_file.write(check_core.setting["id"]+" @ "+str(nameofnode)+" [RESULT] "+ nodemark+"\n")


    #close last result in checkresult file
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
