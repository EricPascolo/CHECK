#
# CHECK
#
# @authors : Eric Pascolo
#

import logging
from checklib.inout import file_reader
from checklib.common import utils
from checklib.scheduler import whatscheduler

def select_checktest_on_architercture(arch,checkcore):
    
    string = ""
    for ct in checkcore.checktests:
        if ct["arch"]== arch:
            string =string+ ct["name"]+""+ct["arch"]+","
    
    if string.endswith(","): 
        return string[:-1]
    else:
        return string


def create_slave_cmd_string(arch,checkcore):

    remote_source_path = "source "+checkcore.setting["check_remote_source_path"]+"/check/bin/setup_check.sh; "


    cmd_check_string = "check"
    cmd_check_string = cmd_check_string + " --loglevel " + checkcore.setting["loglevel"]
    cmd_check_string = cmd_check_string + " --check " + select_checktest_on_architercture(arch,checkcore)

    return remote_source_path + cmd_check_string


def main(checkcore):

    #enable logger
    logger = logging.getLogger(checkcore.setting["logger_name"])
    logger.debug("Start Master")
    

    # load scheduler object
    scheduler = whatscheduler.check_installed_scheduler()
    arch_array = utils.split_hostline(checkcore.setting["hostlist"])
    
    
    #loop on architecture
    for a in arch_array:

        #extract arch
        arch = a["arch"]
        arch_set = a["setting"]
        host_array = a["nodes"]
        
        #load descriptor class
        arch_jsonfile = checkcore.setting["check_test_directory"]+"/architecture/"+arch+".json"
        arch_setting = file_reader.json_reader(arch_jsonfile)[arch_set]
        
        for h in host_array:
            
            arch_setting["hostname"]=h
            scheduler_string = scheduler.scheduler_string_generator(arch_setting)
            
            #get scheduler string

            #get slave string
            slave_string = create_slave_cmd_string(arch,checkcore)

            #create submit string
            slave_submit_string = scheduler_string + "\"" + slave_string + "\""
            logger.debug(slave_submit_string)

            #submit via scheduler