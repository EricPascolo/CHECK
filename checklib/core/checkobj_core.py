#
# CHECK
#
# @authors : Eric Pascolo
#

import logging
import os
import sys
import imp
from checklib.inout import file_reader
from checklib.inout import checklog
from checklib.common import utils
from operator import concat
class check_core:
    '''
    This object contain all setting that the software 
    '''

    loggername = " "
    loglevel = " "
    logtype = " "

    check_test_directory = " "
    check_tests_list = " "
    execution = " "
    hpc_cluster_list = " "

####--------------------------------------------------------------------------------------------------------------

    def __init__(self,cl_arg):
        
        check_file = os.path.realpath(os.path.expanduser(__file__))
        check_prefix = os.path.dirname(os.path.dirname(os.path.dirname(check_file)))
       
        ## set setting file path
        check_setting_path = " "
        check_setting_path_standard = check_prefix+"/etc"+"/check_setting.json"
        check_setting_path_default  = check_prefix+"/etc/default"+"/check_setting.json"
        
        ## check if you create a personal setting file
        if os.path.exists(check_setting_path_standard):
            check_setting_path = check_setting_path_standard
       
        ## check if setting file is in default location
        elif os.path.exists(check_setting_path_default):
            check_setting_path = check_setting_path_default
       
        ## setting file not found
        else:
            sys.exit("ERROR CHECK setting file not found")
        
        ## extract setting information from json file
        json_setting = file_reader.json_reader(check_setting_path)
        
        ## substitute in path ENV variable
        utils.resolve_env_path(json_setting)
        utils.resolve_env_path(cl_arg)

        ## enable log with cl or file setting
        try:
            self.loggername = checklog.checkloggin(json_setting["loglevel"],json_setting["logfile"],cl_arg["log"],cl_arg["logfile"],json_setting["logtype"])
        except KeyError:
            self.loggername = checklog.checkloggin(json_setting["loglevel"],json_setting["logfile"],cl_arg["log"],cl_arg["logfile"])
        
        
        logger = logging.getLogger(self.loggername)
        logger.debug(self.loggername)

        ## extract check setting and put it in core object
        self.extract_to_file(json_setting)

        ## extract cl setting and put it in core object
        self.extract_to_cl(cl_arg)

                
        #load checktest list module

####--------------------------------------------------------------------------------------------------------------    

    def extract_to_cl(self,cl):
        
        """ Extract all information from command line and put it in check core object """

        logger = logging.getLogger(self.loggername)

        # update cl setting with conf file setting if exist
        # the conf file setting override cl setting
        if cl["configuration"] is not None:

            try: 
                json_config_setting = {}
                json_config_setting = file_reader.json_reader(cl["configuration"])
                cl.update(json_config_setting)
                logger.info("merge cl with conf file")
            except:
                logger.critical("wrong merge cl with conf file")

        # load name of check test in list
        names_of_check_test = "".join(cl["check"]).split(",")
        logger.debug(names_of_check_test)
        
        self.checktests = self.load_checktest(names_of_check_test)

####--------------------------------------------------------------------------------------------------------------

    def extract_to_file(self,setting):
        
        logger = logging.getLogger(self.loggername)
        
        #check test repo path
        self.check_test_directory = setting["checktest_directory"]
        logger.debug("CHECKTEST DIR : "+self.check_test_directory)
        pass

####--------------------------------------------------------------------------------------------------------------

    def load_checktest(self,cklist):
        """ Given check list import matching checktest module """
        
        logger = logging.getLogger(self.loggername)

        ctarray = []
        
        for ct in cklist:

            #build check test directory path
            path_test_dir = self.check_test_directory+"/"+ct+"/checktest.py"

            #check if path exiist
            if os.path.exists(path_test_dir):

                logger.debug("CHECK TEST FOUND IN:"+path_test_dir)
                
                #build check test module name
                module_name = "checktest."+ct

                #load dynamicaly check test class
                dynamic_class = imp.load_source(module_name,path_test_dir)
                
                #get name of class to call
                method_to_call = getattr(dynamic_class, ct)
                
                #init check test dynamically 
                obj = method_to_call(self.loggername)
                
                #append obj test to list
                ctarray.append(obj)
            else:
                logger.critical("CHECK TEST NOT FOUND : "+ct)

        for ckt in ctarray:
            ckt.get_name()

        return ctarray

####--------------------------------------------------------------------------------------------------------------
