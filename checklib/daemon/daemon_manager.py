#
# CHECK
#
# @authors : Eric Pascolo
#

import logging


class deamon_manager:

####--------------------------------------------------------------------------------------------------------------

    def __init__(self,checkcore):
        self.logger = logging.getLogger(checkcore.logger_name)
        self.logger.debug("init deamon")
        
####--------------------------------------------------------------------------------------------------------------

    def command(self,cl_args):
        if cl_args["daemon"] == "start":
            self.start()
        elif cl_args["daemon"] == "submit":
            self.submit()
        elif cl_args["daemon"] == "status":
            self.status()
        elif cl_args["daemon"] == "kill":
            self.kill()

####--------------------------------------------------------------------------------------------------------------

    def start(self):
        self.logger.debug("deamon star")
        pass

####--------------------------------------------------------------------------------------------------------------
    
    def submit(self):
        self.logger.debug("deamon submit")
        pass

####--------------------------------------------------------------------------------------------------------------

    def status(self):
        self.logger.debug("deamon status")
        pass

####--------------------------------------------------------------------------------------------------------------

    def kill(self):
        self.logger.debug("deamon kill")
        pass

####--------------------------------------------------------------------------------------------------------------