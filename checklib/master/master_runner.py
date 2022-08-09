#
# CHECK
#
# @authors : Eric Pascolo
#

import os
import logging
import subprocess
import traceback
import json
import datetime
from subprocess import SubprocessError
from checklib.inout import file_reader
from checklib.common import utils
from checklib.scheduler import whatscheduler


####--------------------------------------------------------------------------------------------------------------

def check_collection_master_directory(checkcore, logger):
    """
    Check if master collection result directory exist, if not create it.
    if return FS error, the function set $HOME and collect dir
    """

    if not os.path.exists(checkcore.setting["check_master_collecting_path"]):
        logger.critical("CHECK MASTER COLLECTING PATH NOT EXIST")

        try:
            logger.critical("CHECK MASTER COLLECTING PATH CREATE")
            os.mkdir(checkcore.setting["check_master_collecting_path"])

        except PermissionError as pe:
            logger.critical("FS ERROR: check permission on check_master_collecting_path.")
            checkcore.setting["check_master_collecting_path"] = os.environ['HOME']

        except FileExistsError:
            pass  # ignore and continue

    logger.debug("check_master_collecting_path: " + checkcore.setting["check_master_collecting_path"])


####--------------------------------------------------------------------------------------------------------------

def select_checktest_on_architecture(arch, checkcore):
    """ Check if the checktest for the  architecture exists and create the string for the job's submission """

    string = ""

    for ct in checkcore.checktests:
        if "_" in arch:
            if ct["arch"] == arch or ct["arch"] == "__all__":
                string = string + ct["name"] + "@" + ct["arch"] + ","
        else:
            if ct["arch"].split("_")[0] == arch or ct["arch"] == "__all__":
                string = string + ct["name"] + "@" + ct["arch"] + ","

    if string.endswith(","):
        return string[:-1]
    else:
        return string


####--------------------------------------------------------------------------------------------------------------

def create_slave_cmd_string(arch, checkcore):
    """Compose slave command string with software name loglevel and checktest list"""

    ending_slash = True if checkcore.setting["check_remote_source_path"].endswith('/') else False
    remote_source_path = ''

    check_folder = checkcore.setting["check_remote_source_path"]

    if os.path.exists(check_folder) and os.path.isdir(check_folder):
        if ending_slash:
            remote_source_path = "source " + checkcore.setting["check_remote_source_path"] + \
                                 "bin/setup_check.sh; "
        else:
            remote_source_path = "source " + checkcore.setting["check_remote_source_path"] + \
                                 "/bin/setup_check.sh; "

    else:
        logger.critical('Could not find a folder named "CHECK" or "check" in path {}.'
                        .format(checkcore.setting["check_remote_source_path"]))
        exit(1)

    if not remote_source_path:
        logger.critical("Something went wrong while forming the command for the slave jobs. Interrupting.")
        exit(2)

    cmd_check_string = f"check " \
                       f"--loglevel {checkcore.setting['loglevel']} " \
                       f"--master_id {checkcore.setting['id']} " \
                       f"--check {select_checktest_on_architecture(arch, checkcore)} " \
                       f"--checktest_directory {checkcore.setting['checktest_directory']}"

    return remote_source_path + cmd_check_string


####--------------------------------------------------------------------------------------------------------------

def main(checkcore):
    """
        Master core function, this function compose slave check command, set scheduler interface, hostlist
        and submit on each node in hostlist via scheduler the slave command.

        To know the scheduler parameter this function read the json architecture file in checktest directory.
        The hostlist is taken via command line or from config file.
        The scheduler interface is selected by check_installed_scheduler function and the submission line is composed
        in this way:

            scheduler_exe  scheduler_parameter check_slave_command

        The slave command for all scheduler is inlined in submission line.
        Can you request a job without hostlist in this way:

        arch#def:'<"nnodes"=4;"exclusive"="yes";"wtime"=20;"queue"="system";"account"="cin_pos">'

    """

    # enable logger
    logger = logging.getLogger(checkcore.setting["logger_name"])
    logger.debug("Start Master")

    # check collecting path and create subdir
    check_collection_master_directory(checkcore, logger)

    # load scheduler object
    scheduler = whatscheduler.check_installed_scheduler(checkcore.setting)

    if not scheduler:
        logger.critical("Cannot start CHECK in master mode without a scheduler.")
        return

    if "hpc" not in checkcore.setting:
        logger.critical("To run CHECK in master mode a --hpc option is necessary, specifying architecture and nodes.")
        return

    arch_array = utils.split_hostline(checkcore.setting["hpc"])

    # load hpc cluster file
    hpc_map = dict()
    if "hpc_cluster_map" in checkcore.setting:
        hpc_mapfile = checkcore.setting["hpc_cluster_map"]
    else:
        hpc_mapfile = checkcore.setting["checktest_directory"] + "/hpc/" + "map.hpc"

    if os.path.exists(hpc_mapfile):
        hpc_map = file_reader.hpc_map_file_reader(hpc_mapfile)
        logger.debug("Hpc_map_file: FOUND ")

    out_file = open(checkcore.setting["resultfile"], "a+")

    # loop on architecture
    for a in arch_array:

        # extract arch
        arch = a["arch"]
        arch_set = a["setting"]

        # if singleton is defined in cl, split group in single nodes
        if "singleton" in checkcore.setting:
            host_array = utils.extract_elements_from_dict_by_keylist(a["nodes"], hpc_map)
        else:
            host_array = a["nodes"]

        # load descriptor of architecture
        arch_jsonfile = checkcore.setting["checktest_directory"] + "/hpc/" + arch + ".json"
        arch_setting_global = file_reader.json_reader(arch_jsonfile)[arch_set]

        submission_errors = 0
        submission_error_nodes = list()

        for h in host_array:

            # local arch setting for each job
            arch_setting = arch_setting_global.copy()

            # request job without nodelist
            if "<" in h:
                new_set_dict = utils.convert_request_to_json(h)
                arch_setting.update(new_set_dict)
                del arch_setting["hostname"]
                arch_setting["jobname"] = "check_" + checkcore.setting["id"][:6]

            # node or group of nodes, separated by comma
            else:
                host_list = []
                # groups of nodes
                if h in hpc_map:
                    host_list = hpc_map[h]
                # single nodes
                else:
                    host_list.append(h)
                arch_setting["hostname"] = host_list
                arch_setting["jobname"] = "check_" + h

            # set up path for job output file
            arch_setting["jobcollectionpath"] = checkcore.setting["check_master_collecting_path"]

            # wtime(min) -> walltime(hh:mm:ss)
            if "wtime" in arch_setting:
                arch_setting["walltime"] = str(datetime.timedelta(minutes=arch_setting["wtime"]))

            # get scheduler string
            scheduler_string = scheduler.scheduler_string_generator(arch_setting)

            # get slave string
            slave_string = create_slave_cmd_string(arch, checkcore)

            # create submit string, different for scheduler and ssh
            if "ssh" in checkcore.setting:
                slave_submit_string = scheduler_string + " \"(" + slave_string + " )&>/dev/null & \""
            else:
                slave_submit_string = scheduler_string + "\"" + slave_string + "\""

            logger.info(slave_submit_string)

            # submit via scheduler
            try:
                completed_process = subprocess.run(slave_submit_string, shell=True,
                                                   cwd=checkcore.setting["check_master_collecting_path"],
                                                   executable='/bin/bash', env=os.environ, capture_output=True,
                                                   universal_newlines=True)

                if completed_process.stdout:
                    logger.info(completed_process.stdout)

                if completed_process.stderr and "error" in completed_process.stderr.lower():
                    submission_errors += 1
                    submission_error_nodes.append(h)

                    if type(h) is list:
                        logger.critical("Submission Error on nodes {}: {}".format(
                            ", ".join(h).rstrip(", "), completed_process.stderr.rstrip('\n')))

                    else:
                        logger.critical("Submission Error on node {}: {}".format(
                            h, completed_process.stderr.rstrip('\n')))

            # SubprocessError is the superclass exception for every other exception from the subprocess library
            except SubprocessError:
                logger.critical("SUBMISSION ERROR")
                traceback.print_exc()

        total_nodes = set(host_array)
        error_nodes = set(submission_error_nodes)
        working_nodes = list(total_nodes - error_nodes)

        if submission_errors != 0:
            logger.critical("{} submission errors. Jobs weren't scheduled on {}".format(
                submission_errors, ", ".join(error_nodes).rstrip(", ")))

        json.dump({"master_submission": {"id": checkcore.setting["id"],
                                         "check": str(select_checktest_on_architecture(arch, checkcore)),
                                         "arch": arch + "#" + arch_set,
                                         "date": str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
                                         "hpc": utils.list_to_String(
                                             working_nodes if working_nodes else ["None"], ",")}},
                  out_file, sort_keys=True)

        out_file.write("\n")

    # close last result in checkresult file
    out_file.close()
    ####--------------------------------------------------------------------------------------------------------------
