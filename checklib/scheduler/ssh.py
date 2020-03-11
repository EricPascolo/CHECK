from checklib.scheduler.scheduler_template import scheduler

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
        submission_string = submission_string +" "+arch_setting["hostname"]+" nohup "
        

        return submission_string

####--------------------------------------------------------------------------------------------------------------

    def get_job_resources(self):
        '''
        Return job requested resources in a dictionary
        '''

        pass

####--------------------------------------------------------------------------------------------------------------