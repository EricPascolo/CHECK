import logging
from checklib.common import utils

####--------------------------------------------------------------------------------------------------------------

def check_installed_scheduler(setting):
    """ This function selects scheduler interface, at the moment the scheduler is selected by parameter  """

    logger = logging.getLogger(setting["logger_name"])

    scheduler_object = None
    
    if "ssh" in setting:
        from checklib.scheduler import ssh
        scheduler_object = ssh.ssh()
        logger.debug("SSH mode")
    
    elif setting["cluster_scheduler"] == "Slurm" or utils.is_tool("sbatch"):
        from checklib.scheduler import slurm
        scheduler_object = slurm.slurm()
        logger.debug("scheduler:SLURM")
    
    elif setting["cluster_scheduler"] == "PBS" or utils.is_tool("qsub"):
        from checklib.scheduler import pbs
        scheduler_object = pbs.pbs()
        logger.debug("scheduler:PBS")

    else:
        logger.critical("NO SCHEDULER FOUND")

    return scheduler_object

####--------------------------------------------------------------------------------------------------------------
