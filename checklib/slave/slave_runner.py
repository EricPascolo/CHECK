#
# CHECK
#
# @authors : Eric Pascolo
#

import logging
import os
from checklib.core import checkobj_result
check_results = []

####--------------------------------------------------------------------------------------------------------------

def main(check_core):
    
    logger = logging.getLogger(check_core.setting.logger_name)
    logger.debug("Star slave")
    
    for cs in check_core.checktests:
        logger.debug("--------------- CheckTest : "+cs.get_name())
        try: 
            cs.preproc()
            cs.run()
            cs.postproc()
            check_results.append(cs.comparison())
        except:
            check_results.append(checkobj_result.check_result(cs.get_name(),"FAIL"))

    for cr in check_results:
        logger.critical(os.getenv("HOSTNAME") +" -->"+ str(cr.measure)+" "+cr.udm+" "+cr.check_status_dictionary[cr.status] )

####--------------------------------------------------------------------------------------------------------------
    