#
# CHECKS v 0.1
#
# @authors : Eric Pascolo
#
# Copyright (C) 2017 B.U HPC - CINECA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
    loggername = 'check_file_stream_log'
    logger = logging.getLogger(loggername)
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
    
    logger.info("Enable logger name:"+loggername+" type:"+logtype)

    return loggername
    