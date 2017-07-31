#
# CHECK
#
# @authors : Eric Pascolo
#


import logging

def checkloggin(set_log,set_logfile,cl_log,cl_logfile,logtype="both"):
    
    ## set logleve, command line set have priority
    if cl_log is None:
        loglevel = logging.getLevelName(set_log)
    else:
        loglevel = logging.getLevelName(cl_log)
    
    ## set logfile, command line set have priority
    if cl_logfile is None:
        logfile = set_logfile
    else:
        logfile = cl_logfile

    # create logger with 'spam_application'
    logger_name = 'check_file_stream_log'
    logger = logging.getLogger(logger_name)
    logger.setLevel( loglevel  )
    # create file handler which logs even debug messages
    fh = logging.FileHandler(logfile)
    fh.setLevel(loglevel)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s (%(module)s %(funcName)s) : %(message)s')
    fh.setFormatter(formatter)
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
    