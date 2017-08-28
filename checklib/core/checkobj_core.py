#
# CHECK
#
# @authors : Eric Pascolo
#

import logging
import os
import sys
import importlib
from checklib.inout import file_reader
from checklib.inout import checklog
from checklib.common import utils
from operator import concat
from checklib.test.check_test_template import checktest


#################################################################################################### SETTING CLASS

class check_core_setting:
    '''
    Setting parameter of core
    '''

    logger_name = " "
    check_test_directory = " "

####################################################################################################### CORE CLASS

class check_core:
    '''
    This object contain all setting that the software 
    '''
    setting = None  # check core setting object 
    checktests = [] # list of checktest object

####--------------------------------------------------------------------------------------------------------------

    def __init__(self,cl_arg):
        
        self.setting = check_core_setting()
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
            self.setting.logger_name = checklog.checkloggin(json_setting["loglevel"],json_setting["logfile"],cl_arg["log"],cl_arg["logfile"],json_setting["logtype"])
        except KeyError:
            self.setting.logger_name = checklog.checkloggin(json_setting["loglevel"],json_setting["logfile"],cl_arg["log"],cl_arg["logfile"])
        
        
        logger = logging.getLogger(self.setting.logger_name)
        logger.debug(self.setting.logger_name)

        ## extract check setting and put it in core object
        self.extract_to_file(json_setting)

        ## extract cl setting and put it in core object
        self.extract_to_cl(cl_arg)

####--------------------------------------------------------------------------------------------------------------    

    def extract_to_cl(self,cl):
        
        """ Extract all information from command line and put it in check core object """

        logger = logging.getLogger(self.setting.logger_name)

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

        if not cl["check"] == "-999":
            # load name of check test in list
            names_of_check_test = "".join(cl["check"]).split(",")
            logger.debug(names_of_check_test)
            
            # load checktest object list
            self.checktests = self.load_checktest(names_of_check_test)
        else:
            logger.critical("Checktest list is empty")
####--------------------------------------------------------------------------------------------------------------

    def extract_to_file(self,setting):
        
        logger = logging.getLogger(self.setting.logger_name)
        
        #check test repo path
        self.setting.check_test_directory = setting["checktest_directory"]
        logger.debug("CHECKTEST DIR : "+self.setting.check_test_directory)
        pass

####--------------------------------------------------------------------------------------------------------------

    def load_checktest(self,cklist):
        """ Given check list import matching checktest module """

        logger = logging.getLogger(self.setting.logger_name)

        ctarray = []
        sys.path.append(self.setting.check_test_directory)

        for ct in cklist:

            #split check test name in name,version,architecture and build correct path
            ct_sfw,ct_arch,ct_vers,ct_num_par = utils.split_name_version(ct)
            logger.debug("CT split : "+ct+" name "+ct_sfw+" arch "+ct_arch+" version "+ct_vers)

            if ct_arch != None:
                path_test_dir = self.setting.check_test_directory+"/"+ct_sfw+"/"+ct_arch
                module_name = ct_sfw+"."+ct_arch
            else:
                path_test_dir = self.setting.check_test_directory+"/"+ct_sfw
                module_name = ct_sfw

            logger.debug(path_test_dir + "---" + module_name)

            #build check test module init
            path_test_init = path_test_dir+"/__init__.py"

            #check if path exiist
            if os.path.exists(path_test_init):
                
                logger.debug("CHECK TEST FOUND IN:"+path_test_dir)
                #load dynamicaly check test class
                dynamic_class = importlib.import_module(module_name)
                
                #get name of class to call
                method_to_call = getattr(dynamic_class, ct_sfw)
                
                #init check test dynamically 
                obj = method_to_call(self.setting,ct_arch,ct_vers)
                
                #append obj test to list
                ctarray.append(obj)
            else:
                logger.critical("CHECK TEST NOT FOUND : "+ct)

        return ctarray

####--------------------------------------------------------------------------------------------------------------
