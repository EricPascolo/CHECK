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
    
####--------------------------------------------------------------------------------------------------------------