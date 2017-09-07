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

def main(check_core):
    
    """
    CHECK's launch core function, this main launch all checkstest and after collect the resutls for single node
    and provide to call Multibenchmark node analysis.
    """
    
    # define logger
    logger = logging.getLogger(check_core.setting["logger_name"])
    logger.debug("Star slave")

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

    # log partial result of single benchmark
    for cr in check_results:
        logger.info(str(nameofnode) +" --> "+str(cr.measure)+" "+cr.udm+" "+cr.status )

    # call multibenchmark analysis and log the result
    logger.critical(str(nameofnode) +"  "+ multibenchmark.simple_mb_analisys(check_results)[0])

####--------------------------------------------------------------------------------------------------------------
    