from checklib.scheduler.scheduler_template import scheduler
from checklib.common import utils
import os

class pbs(scheduler):

    """  PBS Pro check interface

            Scheduler cmd        : "qsub" 
            Anchor to slave cmd  : " -- /usr/bin/bash -c "

        This scheduler allow user to submit to automatic router queue, so the interfece accept the __noqueue__ parameter.
            
    """
####--------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()
        self.name = "pbs"

####--------------------------------------------------------------------------------------------------------------

    def scheduler_string_generator(self, arch_setting):

        submission_string = "qsub"
        if arch_setting["nnodes"] != "":
            submission_string = submission_string +" -l select="+str(arch_setting["nnodes"])
        else:
            submission_string = submission_string +" -l select="+str(len(arch_setting["hostname"]))

        submission_string = submission_string +":ncpus="+str(arch_setting["ncpus"])
        submission_string = submission_string +":mem="+str(arch_setting["memory"])

        if "hostname" in arch_setting:
            submission_string = submission_string +":host="+utils.list_to_String(arch_setting["hostname"],',')

        submission_string = submission_string +" -l walltime="+arch_setting["walltime"]
        if  arch_setting["queue"] != "__noqueue__":
            submission_string = submission_string +" -q "+arch_setting["queue"]
        submission_string = submission_string +" -N "+arch_setting["jobname"]
        submission_string = submission_string +" -j oe "
        submission_string = submission_string +" -A "+arch_setting["account"]
        submission_string = submission_string +" -- /usr/bin/bash -c "

        return submission_string

####--------------------------------------------------------------------------------------------------------------

    def get_job_resources(self):
        '''
        Take job requested resources from env variables
        '''
        resources = {}
        resources.update({"JOB_ID":os.path.expandvars("$PBS_JOBID")})
        resources.update({"JOB_NAME":os.path.expandvars("$PBS_JOBNAME")})
        resources.update({"NODE_FILE":os.path.expandvars("$PBS_NODEFILE")})
        resources.update({"NODENAME":os.path.expandvars("$PBS_O_HOST")})
        
        return resources