import os
from checklib.scheduler.scheduler_template import scheduler
from checklib.common import utils

class slurm(scheduler):
    
    '''  Slurm check interface

            Scheduler cmd        : "sbatch" 
            Anchor to slave cmd  : " --wrap "

        This scheduler not allow user to submit to automatic router queue.
            
    '''   

####--------------------------------------------------------------------------------------------------------------
#     
    def __init__(self):
        self.name = "slurm"

####--------------------------------------------------------------------------------------------------------------

    def scheduler_string_generator(self,arch_setting):
        '''
        arch_setting object:
            - nnodes
            - ncpus
            - memory
            - exclusive
            - hostname
            - walltime
            - queue
            - jobname
            - account

        '''
        submission_string = "sbatch"

        #automatic select number of nodes: explicit in setting or number of element of hostlist
        if arch_setting["nnodes"] != "":
            submission_string = submission_string +" -N "+str(arch_setting["nnodes"])
        else:
            submission_string = submission_string +" -N "+str(len(arch_setting["hostname"]))

        #automatic select number of node resources: explicit in setting or exclusive(all node taken)
        if "exclusive" in arch_setting:
            submission_string = submission_string +" --exclusive "
        else:
            submission_string = submission_string +" -n "+arch_setting["ncpus"]
            submission_string = submission_string +" --mem="+arch_setting["memory"]
        
        if "hostname" in arch_setting:
            submission_string = submission_string +" --nodelist "+utils.list_to_String(arch_setting["hostname"],',')

        submission_string = submission_string +" -t 0-"+arch_setting["walltime"]
        submission_string = submission_string +" --partition "+arch_setting["queue"]
        submission_string = submission_string +" --job-name "+arch_setting["jobname"]
        submission_string = submission_string +" -o "+arch_setting["jobcollectiongpath"]+"/"+arch_setting["jobname"]
        submission_string = submission_string +" --account="+arch_setting["account"]
        submission_string = submission_string +" --wrap "

        return submission_string

####--------------------------------------------------------------------------------------------------------------
    def get_job_resources(self):
        '''
        Take job requested resources from env variables
        '''
        resources = {}
        resources.update({"JOB_CPUS_PER_NODE":os.path.expandvars("$SLURM_JOB_CPUS_PER_NODE")})
        resources.update({"CPUS_ON_NODE":os.path.expandvars("$SLURM_CPUS_ON_NODE")})
        resources.update({"CPUS_PER_TASK":os.path.expandvars("$SLURM_CPUS_PER_TASK")})
        resources.update({"GPUS":os.path.expandvars("$SLURM_GPUS")})
        resources.update({"JOB_ID":os.path.expandvars("$SLURM_JOB_ID")})
        resources.update({"JOB_NAME":os.path.expandvars("$SLURM_JOB_NAME")})
        resources.update({"NTASKS_PER_NODE":os.path.expandvars("$SLURM_NTASKS_PER_NODE")})
        resources.update({"NODENAME":os.path.expandvars("$SLURMD_NODENAME")})
        resources.update({"GPUS_PER_NODE":os.path.expandvars("$SLURM_GPUS_PER_NODE")})
        resources.update({"GPUS_PER_TASK":os.path.expandvars("$SLURM_GPUS_PER_TASK")})
        return resources


####--------------------------------------------------------------------------------------------------------------
