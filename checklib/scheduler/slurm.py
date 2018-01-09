from checklib.scheduler.scheduler_template import scheduler

class slurm(scheduler):

    def __init__(self):
        self.name = "slurm"

    def scheduler_string_generator(self,arch_setting):

        submission_string = "sbatch"
        submission_string = submission_string +" -N "+arch_setting["number_of_nodes"]
        submission_string = submission_string +" -n "+arch_setting["ncpus"]
        submission_string = submission_string +" --mem="+arch_setting["memory"]
        submission_string = submission_string +" --nodelist "+arch_setting["hostname"]
        submission_string = submission_string +" -t 0-"+arch_setting["walltime"]
        if  arch_setting["queue"] != "__noqueue__":
            submission_string = submission_string +" --partition "+arch_setting["queue"]
        submission_string = submission_string +" --job-name "+arch_setting["jobname"]
        submission_string = submission_string +" -o "+arch_setting["jobcollectiongpath"]+"/"+arch_setting["jobname"]
        submission_string = submission_string +" --account="+arch_setting["account"]
        submission_string = submission_string +" --wrap "

        return submission_string



