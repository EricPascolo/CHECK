from checklib.scheduler.scheduler_template import scheduler

class ssh(scheduler):
    
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

        submission_string = "ssh"
        submission_string = submission_string +" "+arch_setting["hostname"]+" nohup "
        

        return submission_string

####--------------------------------------------------------------------------------------------------------------


