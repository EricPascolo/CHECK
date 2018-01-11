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

def create_arg_dict_from_string(a):
    
    """ Transform string in args dictionary in python callable object. 
        Not use eval() to avoid code error or hacking """
    
    logger = logging.getLogger("basic")
    
    for k,v in utils.get_iter_object_from_dictionary(a):
        
        if k == "required": 
          
            if v == "True": 
                a[k] = True
            else:
                a[k] = False


        if k == "type": 
            
            if v == "str":
                a[k] = str
            if v == "int":
                a[k] = int
            if v == "float":
                a[k] = float
            if v == "open":
                a[k] = open
               


####--------------------------------------------------------------------------------------------------------------

def cl_parser():
    """
    Parsing command line pars with argparse module, the cl argoument is dynamically loaded from configuration file,
    and after parser by a fuction that convert string in py callable object.
    """
    
    #get basic logger
    logger = logging.getLogger("basic")
    
    #get cl setting filepath
    check_setting_path = utils.get_setting_file_path("check_cl.json")
        
    # extract setting information from json file
    cl_setting = file_reader.json_reader(check_setting_path)
    
    #init parser 
    parser = argparse.ArgumentParser(description = ''' CHECK : Cluster Health and Environment ChecKing system''', formatter_class=argparse.RawTextHelpFormatter)

    # add parser argument from dictionary obtained to json file
    for arg in cl_setting["flag"]:
        # trasform string in object
        create_arg_dict_from_string(arg["param"])
        # add arg name and arg parameter dictionay
        parser.add_argument(arg["name"], **arg["param"])

    return parser.parse_args()

    
####--------------------------------------------------------------------------------------------------------------

def cl_convert_to_dict(args):
    """
    Convert args object in dictionary
    """
    
    convdict = utils.get_iter_object_from_dictionary(vars(args))
    newdict =   dict([(vkey, vdata) for vkey, vdata in convdict if(vdata) ])
    
    return newdict

####--------------------------------------------------------------------------------------------------------------