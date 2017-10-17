#
# CHECK
#
# @authors : Eric Pascolo
#

import os
import logging
import subprocess
import traceback
from checklib.inout import file_reader
from checklib.common import utils
from checklib.scheduler import whatscheduler



def check_collectiong_master_directory(checkcore,logger):
    ''' Check if master collection result directory exist, if not create it.
    if return FS error, the function set $HOME ad collect dir    '''

    if not os.path.exists(checkcore.setting["check_master_collecting_path"]):       
        logger.critical("CHECK MASTER COLLECTING PATH NOT EXIST")
        try:
            os.mkdir(checkcore.setting["check_master_collecting_path"])
            logger.critical("CHECK MASTER COLLECTING PATH CREATE")
        except:
            logger.critical("FS ERROR: check permission on check_master_collecting_path")
            checkcore.setting["check_master_collecting_path"]=os.environ['HOME']


    logger.debug("check_master_collecting_path : "+checkcore.setting["check_master_collecting_path"])
    

def select_checktest_on_architercture(arch,checkcore):
    
    string = ""
    
    for ct in checkcore.checktests:
        if ct["arch"].split("_")[0]== arch or ct["arch"]== "__all__":
            string =string+ ct["name"]+"@"+ct["arch"]+","
    
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
    
    #check collecting path and create subdir
    check_collectiong_master_directory(checkcore,logger)

    # load scheduler object
    scheduler = whatscheduler.check_installed_scheduler()
    arch_array = utils.split_hostline(checkcore.setting["hostlist"])
    
    
    #loop on architecture
    for a in arch_array:

        #extract arch
        arch = a["arch"]
        arch_set = a["setting"]
        host_array = a["nodes"]
        
        #load descriptor of architecture
        arch_jsonfile = checkcore.setting["check_test_directory"]+"/architecture/"+arch+".json"
        arch_setting = file_reader.json_reader(arch_jsonfile)[arch_set]
        
        for h in host_array:
            
            arch_setting["hostname"]=h
            arch_setting["jobname"]= "check_"+h
            arch_setting["jobcollectiongpath"] = checkcore.setting["check_master_collecting_path"]
            #get scheduler string
            scheduler_string = scheduler.scheduler_string_generator(arch_setting)

            #get slave string
            slave_string = create_slave_cmd_string(arch,checkcore)

            #create submit string
            slave_submit_string = scheduler_string + "\"" + slave_string + "\""
            logger.info(slave_submit_string)

            #submit via scheduler
            try:
                process = subprocess.call( slave_submit_string, shell=True,cwd=checkcore.setting["check_master_collecting_path"],executable='/bin/bash',env=os.environ)
         
            except:
                logger.critical("SUBMISSION ERROR")
                traceback.print_exc()
                