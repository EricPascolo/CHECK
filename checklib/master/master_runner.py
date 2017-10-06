#
# CHECK
#
# @authors : Eric Pascolo
#
from checklib.scheduler import whatscheduler
def create_slave_cmd_string:
    return "source /cinecalocal/usprod/check/bin/setup_check.sh; check --check linpack@bwd,stream@bwd --loglevel INFO"

import logging

def main(checkcore):

    #enable logger
    logger = logging.getLogger(checkcore.setting["logger_name"])
    logger.debug("Start Master")
    
    # load scheduler object
    scheduler = whatscheduler.check_installed_scheduler()

    #loop on hostname
    for h in hostlist:
        # get scheduler string
        scheduler_string = scheduler.string_generator(number_of_nodes,ncpus,memory,hostname,walltime,queue,account)

        #get slave string
        slave_string = create_slave_cmd_string()

        #create submit string
        slave_submit_string = scheduler_string + slave_string
        
        # submit via scheduler