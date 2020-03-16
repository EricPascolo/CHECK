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

####--------------------------------------------------------------------------------------------------------------

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

####--------------------------------------------------------------------------------------------------------------    

def select_checktest_on_architercture(arch,checkcore):
    ''' Check if checktest for targer architecture exist and create string for job submission '''
    
    string = ""
    
    for ct in checkcore.checktests:
        
        if "_" in arch:
            if ct["arch"] == arch or ct["arch"]== "__all__":
                string =string+ ct["name"]+"@"+ct["arch"]+","
            
        else:
            if ct["arch"].split("_")[0]== arch or ct["arch"]== "__all__":
                string =string+ ct["name"]+"@"+ct["arch"]+","
    
    if string.endswith(","): 
        return string[:-1]
    else:
        return string

####--------------------------------------------------------------------------------------------------------------

def create_slave_cmd_string(arch,checkcore):
    '''Compose slave command string with software name logleve and checktest list'''

    remote_source_path = "source "+checkcore.setting["check_remote_source_path"]+"/check/bin/setup_check.sh; "


    cmd_check_string = "check"
    cmd_check_string = cmd_check_string + " --loglevel " + checkcore.setting["loglevel"]
    cmd_check_string = cmd_check_string + " --master_id " + checkcore.setting["id"]
    cmd_check_string = cmd_check_string + " --check " + select_checktest_on_architercture(arch,checkcore)
    if arch=='ssh':
        cmd_check_string = cmd_check_string +  "< /dev/null > /dev/null 2>&1 &"

    return remote_source_path + cmd_check_string

####--------------------------------------------------------------------------------------------------------------

def main(checkcore):
    '''
        Master core function, this function compose slave check command, set scheduler interface, hostlist
        and submit on each node in hostlist via scheduler the slave command.

        To know the scheduler parameter this function read the json architecture file in checktest directory.
        The hostlist is taken via command line or from config file.
        The scheduler interface is selected by check_installed_scheduler function and the submission line is composed in this way:

            scheduler_exe  scheduler_parameter check_slave_command

        The slave command for all scheduler is inlined in submission line.
    
    '''

    #enable logger
    logger = logging.getLogger(checkcore.setting["logger_name"])
    logger.debug("Start Master")
    
    #check collecting path and create subdir
    check_collectiong_master_directory(checkcore,logger)

    # load scheduler object
    scheduler = whatscheduler.check_installed_scheduler(checkcore.setting)
    arch_array = utils.split_hostline(checkcore.setting["hpc"])

    #load hpc cluster file
    hpc_map = {}
    if "hpc_cluster_map" in checkcore.setting:
        hpc_mapfile = checkcore.setting["hpc_cluster_map"]
    else:
        hpc_mapfile = checkcore.setting["checktest_directory"]+"/hpc/"+"map.hpc"
    
    if os.path.exists(hpc_mapfile):
        hpc_map = file_reader.hpc_map_file_reader(hpc_mapfile)
        logger.debug("Hpc_map_file: FOUND ")
        
    
    #loop on architecture
    for a in arch_array:

        #extract arch
        arch = a["arch"]
        arch_set = a["setting"]

        #if singleton is defined in cl, split group in single nodes
        if "singleton" in checkcore.setting:
            host_array = utils.extract_elements_from_dict_by_keylist(a["nodes"],hpc_map)
        else:
            host_array = a["nodes"]
        
        #load descriptor of architecture
        arch_jsonfile = checkcore.setting["checktest_directory"]+"/hpc/"+arch+".json"
        arch_setting = file_reader.json_reader(arch_jsonfile)[arch_set]

        for h in host_array:
            
            #select group of nodes or single hostname
            host_list = []
            if h in hpc_map:
                host_list = hpc_map[h]
            else:
                host_list.append(h)

            arch_setting["hostname"]=host_list
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
                
####--------------------------------------------------------------------------------------------------------------