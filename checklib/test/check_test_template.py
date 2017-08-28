#
# CHECK
#
# @authors : Eric Pascolo
#

import subprocess
import logging
import os
import regex
from checklib.core.checkobj_result import check_result 
from checklib.common.archive import *
class checktest():

    """ Checktest template class """

    #test description
    name = ""
    version = ""
    url = ""
    target_arch = ""
    test_vers = ""

    # check object
    result = None
    check_log = None
    check_core = None
    std_out = None
    std_err = None

    # test parameter
    exe = ""
    exe_argument = ""
    test_dir = {'bin_dir': 'bin', 'in_dir': 'in', 'out_dir': 'out','tmp_dir': 'tmp',}

################################################################################################ CHECK TETS METHOD


    def __init__(self,core,arch,vers):

        self.check_core = core 
        self.target_arch = arch
        self.test_vers = vers
        self.set_test_logger()
        self.check_path_builder()
        self.check_log.debug("CHECK TEST INIT : "+self.get_name())

####--------------------------------------------------------------------------------------------------------------

    def preproc(self):
        self.check_log.debug("call empty preproc")
        pass

####--------------------------------------------------------------------------------------------------------------

    def run(self):
        self.check_log.debug("call empty run")
        self.run_check_xx()
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
         

        for k in self.test_dir:
            if not os.path.isabs(self.test_dir[k]):
                    self.test_dir[k] = self.check_core.check_test_directory+"/"+self.get_name()+"/"+self.target_arch+"/"+self.test_dir[k]
                    self.check_log.debug(self.test_dir[k])

        #self.check_log.debug(self.exe)

        if not os.path.isabs(self.exe):
            self.exe = self.test_dir['bin_dir'] +"/"+ self.exe
            self.check_log.debug(self.exe)



####--------------------------------------------------------------------------------------------------------------


    def run_check_xx(self):

      self.check_log.debug(self.exe)
      string_to_execute = self.exe + self.exe_argument
      process = subprocess.Popen( self.exe, shell=False,cwd=self.test_dir["bin_dir"],stdout=subprocess.PIPE)
      self.std_out, self.std_err = process.communicate()

####--------------------------------------------------------------------------------------------------------------