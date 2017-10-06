from checklib.scheduler import scheduler

class pbs(scheduler):

    def __init__(self):
        name = "pbs"

    def scheduler_string_generator(self,number_of_nodes,ncpus,memory,hostname,walltime,queue,account):

        submission_string = "qsub"
        submission_string = submission_string +" -l select="+number_of_nodes
        submission_string = submission_string +":ncpus="+ncpus
        submission_string = submission_string +":mem="+memory
        submission_string = submission_string +":host="+hostname
        submission_string = submission_string +" -l walltime="+walltime
        submission_string = submission_string +" -q "+queue
        submission_string = submission_string +" -A "+account
        submission_string = submission_string +"-- /usr/bin/bash -c"

        return submission_string



