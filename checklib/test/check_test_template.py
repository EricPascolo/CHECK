#
# CHECK
#
# @authors : Eric Pascolo
#

import subprocess
import logging
import os
import re
import sys
from checklib.core.checkobj_result import check_result 
from checklib.common.archive import *
from checklib.scheduler import whatscheduler

class checktest():

    """ Checktest template class """

 
################################################################################################ CHECK TETS METHOD


    def __init__(self,core,arch,vers):

        
        self.test_dir = {'bin_dir': 'bin', 'in_dir': 'in', 'out_dir': 'out','tmp_dir': 'tmp',}
        #test description
        self.name = ""
        self.version = ""
        self.url = ""
        self.target_arch = ""
        self.test_vers = ""

        # check object
        self.check_log = None
        self.check_core = None
        self.std_out = None
        self.std_err = None

        # test parameter
        self.exe_argument = ""
        self.check_core = core 
        self.target_arch = arch
        self.test_vers = vers
        self.set_test_logger()
        self.check_path_builder()
        self.check_log.debug("CHECK TEST INIT : "+self.get_name())

        # result object
        self.result = check_result()

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
        pass
        

####--------------------------------------------------------------------------------------------------------------

    def install(self,setting="default"):
        self.check_log.debug("call empty install")
        pass


################################################################################################## PROVIDED METHOD


    def get_name(self):
        return self.__class__.__name__

####--------------------------------------------------------------------------------------------------------------

    def set_test_logger(self):
        self.check_log =  logging.getLogger(self.check_core["logger_name"])

####--------------------------------------------------------------------------------------------------------------

    def check_path_builder(self):
         
        for k in self.test_dir:
            if self.target_arch =="__all__":
                if not os.path.isabs(self.test_dir[k]):
                       self.test_dir[k] = self.check_core["checktest_directory"]+"/"+self.get_name()+"/"+"/"+self.test_dir[k]
                       #self.check_log.debug(self.test_dir[k])
            else:
                if not os.path.isabs(self.test_dir[k]):
                       self.test_dir[k] = self.check_core["checktest_directory"]+"/"+self.get_name()+"/"+self.target_arch+"/"+self.test_dir[k]
                       #self.check_log.debug(self.test_dir[k])
        
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


    def get_allocated_resources(self):

        resources = {}
        scheduler = whatscheduler.check_installed_scheduler(self.check_core)
        resources = scheduler.get_job_resources()
        return resources


####--------------------------------------------------------------------------------------------------------------