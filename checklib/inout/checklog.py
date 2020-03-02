#
# CHECK
#
# @authors : Eric Pascolo
#


import logging

logger_name = 'basic'
logger = logging.getLogger(logger_name)
logger.setLevel( "INFO"  )
ch = logging.StreamHandler()
logger.addHandler(ch)

####--------------------------------------------------------------------------------------------------------------

def checkloggin(loglevel,logfile,logtype="both"):

    if logfile != "__nofile__" and logtype == "cl":
        logtype="both"
    # create logger with 'spam_application'
    logger_name = 'check_file_stream_log'
    logger = logging.getLogger(logger_name)
    logger.setLevel( loglevel  )
    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s (%(module)s %(funcName)s) : %(message)s')

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
        logger.addHandler(fh)
        logger.addHandler(ch)
    if logtype == "cl":
        logger.addHandler(ch)
    if logtype == "file":
        logger.addHandler(fh)

    logger.info("Enable logger name:"+logger_name+" type:"+logtype)

    return logger_name

####--------------------------------------------------------------------------------------------------------------
