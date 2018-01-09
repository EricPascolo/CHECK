#
# CHECK
#
# @authors : Eric Pascolo
#

import logging
import argparse
import sys
from checklib.common import utils
from checklib.inout import file_reader

####--------------------------------------------------------------------------------------------------------------

def cl_parser():
    """
    Parsing command line pars with argparse module
    """
    
    #get basic logger
    logger = logging.getLogger("basic")
    
    #get cl setting filepath
    check_setting_path = utils.get_setting_file_path("check_cl.json")
        
    # extract setting information from json file
    cl_setting = file_reader.json_reader(check_setting_path)
    
    parser = argparse.ArgumentParser(description = ''' CHECK : Cluster Health and Environment ChecKing system''', formatter_class=argparse.RawTextHelpFormatter)
    
    for arg in cl_setting["flag"]:
        logger.critical(arg)
        parser.add_argument(arg["name"], **arg["param"])

    return parser.parse_args()



    # parser.add_argument(   '--master', 
    #                         action = 'store_true' ,
    #                         required = False,
    #                         help = 'Master/slave flag')
                                
    # parser.add_argument(   '--check', '-ct',
    #                             type = str,
    #                             nargs='+',
    #                             required = False,
    #                             default = "-999",
    #                             help = 'List of check')                            
    
    # parser.add_argument(   '--checkparameters', 
    #                         action = 'store_true' ,
    #                         required = False,
    #                         help = 'Print check setting parameter')
    
    # parser.add_argument(   '--checklist', 
    #                         action = 'store_true' ,
    #                         required = False,
    #                         help = 'Print checktest list')

    # parser.add_argument(   '--configuration', 
    #                             type = str,
    #                             required = False,
    #                             help = 'Input file')

    # parser.add_argument(   '--cluster_scheduler', 
    #                             type = str,
    #                             required = False,
    #                             help = 'Name of scheduler')

    # parser.add_argument(   '--install', 
    #                         action = 'store_true' ,
    #                         required = False,
    #                         help = 'Install checktest')

    # parser.add_argument(   '--analysis', 
    #                             type = str,
    #                             required = False,
    #                             help = 'kind of analysis')
   
    # parser.add_argument(   '--loglevel', 
    #                             type = str,
    #                             required = False,
    #                             help = 'Log level')
    
    # parser.add_argument(   '--logfile', 
    #                             type = str,
    #                             required = False,
    #                             help = 'Log file')

    # parser.add_argument(   '--logtype', 
    #                             type = str,
    #                             required = False,
    #                             help = 'Log type')
   
    # parser.add_argument(   '--hostlist', '-hpc', 
    #                             type = str,
    #                             required = False,
    #                             help = 'List of Hostname to Master submission')

    # parser.add_argument(   '--checktest_directory', '-checkTD', 
    #                             type = str,
    #                             required = False,
    #                             help = 'check test directory')
    

    # parser.add_argument(   '--check_remote_source_path', '-checkRSP', 
    #                             type = str,
    #                             required = False,
    #                             help = 'Remote CHECK directory path')
    
    # parser.add_argument(   '--check_master_collecting_path', '-checkMCP', 
    #                             type = str,
    #                             required = False,
    #                             help = 'Directory path where collect scheduler job results')

    
####--------------------------------------------------------------------------------------------------------------

def cl_convert_to_dict(args):
    """
    Convert args object in dictionary
    """

    convdict = vars(args)
    if sys.version_info[:2] < (3,0):
        newdict =   dict([(vkey, vdata) for vkey, vdata in convdict.iteritems() if(vdata) ])
    else:
        newdict =   dict([(vkey, vdata) for vkey, vdata in convdict.items() if(vdata) ])

    return newdict

####--------------------------------------------------------------------------------------------------------------