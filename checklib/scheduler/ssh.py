from checklib.scheduler.scheduler_template import scheduler
from checklib.common import utils

class ssh(scheduler):
    
    '''  SSH check interface

            Scheduler cmd        : "ssh" 
            Anchor to slave cmd  : " nohup... "

        This scheduler not allow user to submit to automatic router queue.
            
    '''   

####--------------------------------------------------------------------------------------------------------------
#     
    def __init__(self):
        self.name = "ssh"

####--------------------------------------------------------------------------------------------------------------

    def scheduler_string_generator(self,arch_setting):

        submission_string = "ssh"
        submission_string = submission_string +" "+str(utils.list_to_String(arch_setting["hostname"],','))
        
        return submission_string

####--------------------------------------------------------------------------------------------------------------

    def get_job_resources(self):
        '''
        Return job requested resources in a dictionary
        '''

        pass

####--------------------------------------------------------------------------------------------------------------