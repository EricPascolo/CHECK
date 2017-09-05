#
# CHECK
#
# @authors : Eric Pascolo
#

import traceback
import logging
import os
from checklib.core import checkobj_result
from checklib.slave import multibenchmark

####--------------------------------------------------------------------------------------------------------------

def main(check_core):
    
    logger = logging.getLogger(check_core.setting.logger_name)
    logger.debug("Star slave")
    check_results = []
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


   
    for cr in check_results:
        logger.info(str(os.getenv("HOSTNAME")) +" --> "+str(cr.measure)+" "+cr.udm+" "+cr.status )

    logger.critical(str(os.getenv("HOSTNAME")) +"  "+ multibenchmark.simple_mb_analisys(check_results)[0])

####--------------------------------------------------------------------------------------------------------------
    