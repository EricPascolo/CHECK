#
# CHECK
#
# @authors : Eric Pascolo, Roberto Da Via'
#

import traceback
import logging
import os
import sys
import importlib
import subprocess
from checklib.inout import file_reader
from checklib.inout import checklog
from checklib.common import utils
from operator import concat
from checklib.test.check_test_template import checktest

####################################################################################################### CORE CLASS

class check_core:
    '''
    This object contain all setting that the software
    '''
    setting = {}  # check core setting object
    checktests = [] # list of checktest object


####--------------------------------------------------------------------------------------------------------------

    def __init__(self,cl_arg,run_id):
        
        #set run id
        self.setting.update({"id":run_id})

        #set an empty module instance
        self.module = None
        self.setting["module"] = self.module

        # set setting file path
        check_setting_path = utils.get_setting_file_path("check_setting.json")

        ## extract setting information from json file
        json_setting = []
        for p in check_setting_path:
            json_setting.append(file_reader.json_reader(p))

        ## extract check setting and put it in core object
        self.extract_merge_setting(cl_arg,json_setting)
         
        ## enable log with user setting
        try:
            lgnm = checklog.checkloggin(run_id,self.setting["loglevel"], \
                             self.setting["logfile"],self.setting["logtype"])
            self.setting.update({"logger_name":lgnm})
        except KeyError:
            pass
        
        #set logger for this subroutine
        logger = logging.getLogger(self.setting["logger_name"])
        logger.debug(self.setting["logger_name"])
        
        # ssh enable master singleton mode
        if "ssh" in self.setting:
            if "master" not in self.setting:
                self.setting["master"] = True
            if "singleton" not in self.setting:
                self.setting["singleton"] = True

        if "checkparameters" in self.setting:
            self.printparameters()
        
        if "checklist" in self.setting:
            self.printchecklist()
            return

        elif not self.setting["check"] == "-999":
            # load name of check test in list
            names_of_check_test = "".join(self.setting["check"]).split(",")
            logger.debug(names_of_check_test)

            if "master" in self.setting:
                #check existence of checktest
                self.checktests = self.checktests_existence(names_of_check_test)
            else:
                # load checktest object list
                self.checktests = self.load_checktest(names_of_check_test)

        else:
            logger.critical("Checktest list is empty")
        
####--------------------------------------------------------------------------------------------------------------

    def set_module_function(self, module):
        '''
        Set the module function as check_core method. The function is used to load
        software modules from hpc environment 
        '''
        self.module = module
        self.setting["module"] = self.module

####--------------------------------------------------------------------------------------------------------------

    def extract_merge_setting(self,cl,json_basic):

        '''
        Extract and merge  all setting information from command line, json conf file and json
        basic conf file. The priority order is:
            - configuration file passed by cl flag
            - other parameter setting in cl
            - check_setting.json in etc/
            - check_setting.json in etc/default
        The merged dictionary update the global setting dict in class
        '''
        #dict where to merge setting
        json_setting ={}

        # merge json file setting
        for j in json_basic:
            utils.resolve_env_path(j)
            json_setting.update(j)

        #merge cl file setting
        utils.resolve_env_path(cl)
        json_setting.update(cl)

        #if present read and merge configuration file setting
        if "configuration" in cl:
                json_config_setting = {}
                json_config_setting = file_reader.json_reader(cl["configuration"])
                utils.resolve_env_path(json_config_setting)
                json_setting.update(json_config_setting)
 
        #update global setting with merged dict
        self.setting.update(json_setting)


####--------------------------------------------------------------------------------------------------------------

    def checktests_existence(self,cklist):
        """ Given check list check if checktest exist or not """

        logger = logging.getLogger(self.setting["logger_name"])

        ctarray = []
        sys.path.append(self.setting["checktest_directory"])

        for ct in cklist:

            #split check test name in name,version,architecture and build correct path
            ct_sfw,ct_arch,ct_vers,ct_num_par = utils.split_name_version(ct)
            logger.debug("CT split : "+ct+" name "+ct_sfw+" arch "+ct_arch+" version "+ct_vers)

            if ct_arch != "__all__":
                path_test_dir = self.setting["checktest_directory"]+"/"+ct_sfw+"/"+ct_arch
                module_name = ct_sfw+"."+ct_arch
            else:
                path_test_dir = self.setting["checktest_directory"]+"/"+ct_sfw
                module_name = ct_sfw


            logger.debug(path_test_dir + "---" + module_name)

            #build check test module init
            path_test_init = path_test_dir+"/__init__.py"

            #check if path exiist
            if os.path.exists(path_test_init):

                ctarray.append({"name":ct_sfw,"arch":ct_arch})

            else:
                logger.critical("CHECK TEST NOT FOUND : "+ct)

        return ctarray

####--------------------------------------------------------------------------------------------------------------

    def load_checktest(self,cklist):
        """ Return checktest py object given checktest list from CL"""

        logger = logging.getLogger(self.setting["logger_name"])

        ctarray = []
        sys.path.append(self.setting["checktest_directory"])

        for ct in cklist:

            #split check test name in name,version,architecture and build correct path
            ct_sfw,ct_arch,ct_vers,ct_num_par = utils.split_name_version(ct)
            logger.debug("CT split : "+ct+" name "+ct_sfw+" arch "+ct_arch+" version "+ct_vers)


            if ct_arch != "__all__":
                path_test_dir = self.setting["checktest_directory"]+"/"+ct_sfw+"/"+ct_arch
                module_name = ct_sfw+"."+ct_arch
            else:
                path_test_dir = self.setting["checktest_directory"]+"/"+ct_sfw
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

    def printchecklist(self):
        """ Print CHECKTEST installed and archicetures lists"""

        logger = logging.getLogger(self.setting["logger_name"])

        checklist_string = " "

        sys.path.append(self.setting["checktest_directory"])
        subdir = os.listdir(self.setting["checktest_directory"])
        
        #architectures string composer
        if "hpc" in subdir:
            subdir.remove('hpc')
            checklist_string = "\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ARCHITECTURES AVAILABLE:\n\n"
            arch_dir = self.setting["checktest_directory"]+"/hpc/"
            arch_list = os.listdir(arch_dir)
            
            
            for a in sorted(arch_list):
                if a.endswith('.json'):
                    checklist_string = checklist_string+ "================================================ARCH "+a[:-5]+"\n"

                    try:
                        jfile = file_reader.json_reader(arch_dir+a)
                        jread = jfile.keys()
                        
                        #print help string if exist as field "help" in json
                        if 'help' in jread:
                            jread.remove('help')
                            checklist_string = checklist_string+ jfile['help'] +"\n\n"
                        
                        checklist_string = checklist_string + "----- SETTING: "
                        for jk in sorted(jread):
                            checklist_string = checklist_string +jk+","
                        checklist_string = checklist_string[:-1] + "\n\n"
                    except:
                        pass
       
        #checktests string composer
        checklist_string = checklist_string+"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! CHECKTEST AVAILABLE:\n\n"

        # check checktest available
        for dr in sorted(subdir):
            help_path = ""
            dr_path = self.setting["checktest_directory"]+dr+"/"
            
            # check if dir have python package structure
            if os.path.exists(dr_path+"__init__.py"):
                sdr = os.listdir(dr_path)
                
                # case 1) checktest/test/__init__.py               
                if os.path.exists(dr_path+"/__init__.py") and os.path.exists(dr_path+"/help.md"):
                    checklist_string = checklist_string+"================================================ "+dr+"\n"
                    checklist_string = checklist_string+file_reader.filetostring(dr_path+"/help.md")
                
                # case 2) checktest/test/arch/__init__.py    
                else:
                    for d in sorted(sdr):
                        if os.path.exists(dr_path+d+"/__init__.py"):
                            checklist_string = checklist_string+"================================================ "+dr+"@"+d+"\n"
                            checklist_string = checklist_string+file_reader.filetostring(dr_path+d+"/help.md")
                                
                checklist_string = checklist_string + "\n\n"

        logger.critical(checklist_string)

####--------------------------------------------------------------------------------------------------------------

    def printparameters(self):
        """ print all parameters contained in check setting """

        logger = logging.getLogger(self.setting["logger_name"])
        checkparameter_string = "\n"


        for s, sv in sorted(utils.get_iter_object_from_dictionary(self.setting)):
             checkparameter_string = checkparameter_string+"-- "+s +" : "+str(sv)+"\n"

        logger.critical(checkparameter_string)
####--------------------------------------------------------------------------------------------------------------
