
def check_installed_scheduler():
    from checklib.scheduler import pbs
    scheduler_object = pbs.pbs()
    return scheduler_object