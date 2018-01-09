
def check_installed_scheduler(setting):
    
    ''' This function select scheduler interface, at the momemt the scheduler is selected by parameter  '''
    
    if setting["cluster_scheduler"] == "PBS":
        from checklib.scheduler import pbs
        scheduler_object = pbs.pbs()

    if setting["cluster_scheduler"] == "Slurm":
        from checklib.scheduler import slurm
        scheduler_object = slurm.slurm()

    return scheduler_object