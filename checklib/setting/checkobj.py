#
# CHECK
#
# @authors : Eric Pascolo
#

import logging
import os
import sys
from checklib.inout import file_reader
from checklib.inout import checklog
from checklib.common import utils

class check_setting:
    '''
    This object contain all setting that the software 
    '''

    loggername = " "



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