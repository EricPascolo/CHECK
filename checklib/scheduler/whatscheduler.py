
####--------------------------------------------------------------------------------------------------------------

def check_installed_scheduler(setting):
    
    ''' This function select scheduler interface, at the momemt the scheduler is selected by parameter  '''
    
    if setting["cluster_scheduler"] == "PBS":
        from checklib.scheduler import pbs
        scheduler_object = pbs.pbs()

    if setting["cluster_scheduler"] == "Slurm":
        from checklib.scheduler import slurm
        scheduler_object = slurm.slurm()
    
    if setting["cluster_scheduler"] == "ssh":
        from checklib.scheduler import ssh
        scheduler_object = ssh.ssh()

    return scheduler_object

####--------------------------------------------------------------------------------------------------------------