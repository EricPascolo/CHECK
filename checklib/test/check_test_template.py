#
# CHECK
#
# @authors : Eric Pascolo
#

import logging
from checklib.core.checkobj_result import check_result 

class checktest():

    """ Checktest template class """

    #test description
    name = ""
    version = ""
    url = ""
    
    # check object
    check_log = None
    check_core = None
    
    # test parameter
    exucutable = ""
    test_dir =   ""
    bin_dir =    ""
    in_dir =     ""
    out_dir =    ""
    tmp_dir =    ""


################################################################################################ CHECK TETS METHOD


    def __init__(self,core):

        self.check_core = core 
        self.set_test_logger()
        self.check_log.debug("CHECK TEST INIT : "+self.get_name())

####--------------------------------------------------------------------------------------------------------------

    def preproc(self):
        self.check_log.debug("call empty preproc")
        pass

####--------------------------------------------------------------------------------------------------------------

    def run(self):
        self.check_log.debug("call empty run")
        pass

####--------------------------------------------------------------------------------------------------------------

    def postproc(self):
        self.check_log.debug("call empty postproc")
        pass

####--------------------------------------------------------------------------------------------------------------

    def comparison(self):
        result = check_result()
        
        return result

####--------------------------------------------------------------------------------------------------------------

    def install(self):
        self.check_log.debug("call empty install")
        pass



################################################################################################## PROVIDED METHOD


    def get_name(self):
        return self.__class__.__name__

####--------------------------------------------------------------------------------------------------------------

    def set_test_logger(self):
        self.check_log =  logging.getLogger(self.check_core.logger_name)

####--------------------------------------------------------------------------------------------------------------

    def check_path_builder(self):
        self.check_log =  logging.getLogger(self.check_core.logger_name)
        if 

####--------------------------------------------------------------------------------------------------------------