#
# CHECK
#
# @authors : Eric Pascolo
#

import argparse

####--------------------------------------------------------------------------------------------------------------

def cl_parser():
    """
    Parsing command line pars with argparse module
    """
    
    parser = argparse.ArgumentParser(description = '''
    Python check suite to HPC Cluster''',
    formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(   '--master', 
                            action = 'store_true' ,
                            required = False,
                            help = 'Master/slave flag')

    parser.add_argument(   '--daemon', 
                                type = str,
                                required = False,
                                choices=['start', 'submit', 'status','kill'],
                                help = 'Daemon command')
                                
    parser.add_argument(   '--check', '-c',
                                type = str,
                                nargs='+',
                                required = False,
                                default = "-999",
                                help = 'List of check')
    
    parser.add_argument(   '--hpc', 
                                type = str,
                                required =False,
                                default = "-999",
                                help = 'Cluster hostfile')                               

    parser.add_argument(   '--configuration', 
                                type = str,
                                required = False,
                                
                                help = 'Input file')

    parser.add_argument(   '--analysis', 
                                type = str,
                                required = False,
                                default = "-999",
                                help = 'kind of analysis')
   
    parser.add_argument(   '--log', 
                                type = str,
                                required = False,
                                help = 'Input file')
    
    parser.add_argument(   '--logfile', 
                                type = str,
                                required = False,
                                help = 'Input file')

    
    
    return parser.parse_args()

####--------------------------------------------------------------------------------------------------------------

def cl_convert_to_dict(args):
    """
    Convert args object in dictionary
    """
    return vars(args)

####--------------------------------------------------------------------------------------------------------------