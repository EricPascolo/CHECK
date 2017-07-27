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
        logger.debug("CheckTest : "+checkcore.checktest.name)
        cs.preproc()
        cs.run()
        cs.postproc()
        cs.result = cs.comparison()

####--------------------------------------------------------------------------------------------------------------
    