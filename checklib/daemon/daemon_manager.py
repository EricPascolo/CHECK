import logging


class deamon_manager:

    def __init__(self,setting):
        logger = logging.getLogger(setting.loggername)
        logger.debug("init deamon")
        pass