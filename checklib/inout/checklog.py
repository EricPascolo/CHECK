#
# CHECK
#
# @authors : Eric Pascolo
#


import logging

logger_name = 'basic'
logger = logging.getLogger(logger_name)
logger.setLevel("INFO")
ch = logging.StreamHandler()
logger.addHandler(ch)

####--------------------------------------------------------------------------------------------------------------


def checkloggin(run_id, loglevel, logfile, logtype="both"):
    global logger_name, logger, ch

    if logfile != "__nofile__" and logtype == "cl":
        logtype = "both"
    # create logger with 'spam_application'
    logger_name = 'check_file_stream_log'
    logger = logging.getLogger(logger_name)
    logger.setLevel(loglevel)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(str(run_id)+' %(asctime)s [%(levelname)s] (%(funcName)s) : %(message)s', "%H:%M")

    # create file handler which logs even debug messages
    if logfile != "__nofile__":
        fh = logging.FileHandler(logfile)
        fh.setLevel(loglevel)
        fh.setFormatter(formatter)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    ch.setFormatter(formatter)
    # add the handlers to the logger

    if logtype == "both":
        logger.addHandler(ch)

        if logfile != "__nofile__":
            logger.addHandler(fh)
        else:
            logger.critical("ERROR NO LOGGER FILE SET")

    elif logtype == "file":
        if logfile != "__nofile__":
            logger.addHandler(fh)
        else:
            print("ERROR NO LOGGER FILE SET")
    else:
        logger.addHandler(ch)   # cl is default
        if logtype not in ["both", "cl", "file"]:
            logger.critical("ERROR WRONG LOG TYPE: cl is set by default")

    logger.info("Logger type: " + logtype)

    return logger_name

####--------------------------------------------------------------------------------------------------------------
