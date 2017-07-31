#
# CHECK
#
# @authors : Eric Pascolo
#

import logging
from checklib.core import checkobj_result
check_results = []

####--------------------------------------------------------------------------------------------------------------

def main(check_core):
    
    logger = logging.getLogger(check_core.setting.logger_name)
    logger.debug("Star slave")
    
    for cs in check_core.checktests:
        logger.debug("--------------- CheckTest : "+cs.get_name())
        cs.preproc()
        cs.run()
        cs.postproc()
        check_results.append(cs.comparison())

    for cr in check_results:
        logger.critical( str(cr.measure)+" "+cr.udm+" "+cr.check_status_dictionary[cr.status] )

####--------------------------------------------------------------------------------------------------------------
    