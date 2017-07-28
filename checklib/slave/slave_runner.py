#
# CHECK
#
# @authors : Eric Pascolo
#

import logging
from checklib.core import checkobj_result
check_results = []

####--------------------------------------------------------------------------------------------------------------

def main(checkcore):
    
    logger = logging.getLogger(checkcore.loggername)
    logger.debug("Star slave")
    
    for cs in checkcore.checktests:
        logger.debug("--------------- CheckTest : "+cs.get_name())
        cs.preproc()
        cs.run()
        cs.postproc()
        check_results.append(cs.comparison())

    for cr in check_results:
        logger.info( str(cr.measure)+" "+cr.udm+" "+cr.check_status_dictionary[cr.status] )

####--------------------------------------------------------------------------------------------------------------
    