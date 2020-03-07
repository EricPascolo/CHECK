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

        submission_string = "sbatch"

        #automatic select number of nodes: explicit in setting or number of element of hostlist
        if arch_setting["number_of_nodes"] != "":
            submission_string = submission_string +" -N "+arch_setting["number_of_nodes"]
        else:
            submission_string = submission_string +" -N "+str(len(arch_setting["hostname"]))

        #automatic select number of node resources: explicit in setting or exclusive(all node taken)
        if "exclusive" in arch_setting:
            submission_string = submission_string +" --exclusive "
        else:
            submission_string = submission_string +" -n "+arch_setting["ncpus"]
            submission_string = submission_string +" --mem="+arch_setting["memory"]
        
        submission_string = submission_string +" --nodelist "+utils.list_to_String(arch_setting["hostname"],',')

        submission_string = submission_string +" -t 0-"+arch_setting["walltime"]
        submission_string = submission_string +" --partition "+arch_setting["queue"]
        submission_string = submission_string +" --job-name "+arch_setting["jobname"]
        submission_string = submission_string +" -o "+arch_setting["jobcollectiongpath"]+"/"+arch_setting["jobname"]
        submission_string = submission_string +" --account="+arch_setting["account"]
        submission_string = submission_string +" --wrap "

        return submission_string

####--------------------------------------------------------------------------------------------------------------


