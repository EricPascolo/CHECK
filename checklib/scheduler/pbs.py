from checklib.scheduler.scheduler_template import scheduler

class pbs(scheduler):

    def __init__(self):
        self.name = "pbs"

    def scheduler_string_generator(self,arch_setting):

        submission_string = "qsub"
        submission_string = submission_string +" -l select="+arch_setting["number_of_nodes"]
        submission_string = submission_string +":ncpus="+arch_setting["ncpus"]
        submission_string = submission_string +":mem="+arch_setting["memory"]
        submission_string = submission_string +":host="+arch_setting["hostname"]
        submission_string = submission_string +" -l walltime="+arch_setting["walltime"]
        submission_string = submission_string +" -q "+arch_setting["queue"]
        submission_string = submission_string +" -A "+arch_setting["account"]
        submission_string = submission_string +" -- /usr/bin/bash -c "

        return submission_string



