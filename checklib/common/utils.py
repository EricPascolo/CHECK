#
# CHECK
#
# @authors : Eric Pascolo
#


import os
import re
import sys
from checklib.common.archive import *

####--------------------------------------------------------------------------------------------------------------

def resolve_env_path(dictionary):
    '''Given dictionary substitute into path env var'''
    for key, value in dictionary.items():

        try:
            path = os.path.expandvars(value)
            if is_valid(path):
                dictionary[key] = path
        except:
            pass

####--------------------------------------------------------------------------------------------------------------

def is_valid(path):
    '''Check if path is linux path'''

    #re to check path
    prog = re.compile(re_path)#(r"^(/)([^/\0]+(/)?)+$")
    valid = prog.match(path)
    if valid is None:
        return False
    else:
        return True

####--------------------------------------------------------------------------------------------------------------

def split_name_version(software_string):
    '''
    Given the software split name version and architecture
    Use @ symbol to architecture and # symbol for the version   
    '''
    prog = re.compile(re_splitsoftware)
    software_list = re.split(re_splitsoftware,software_string)

    software_hardware = "__all__"
    software_version  = ""
    software_name = software_list[0]
    num_parameter = len(software_list)
    
    if num_parameter >= 2:
        software_hardware = software_list[1]
    if num_parameter == 3:
        software_version  = software_list[2]
    
    return software_name,software_hardware,software_version,num_parameter

####--------------------------------------------------------------------------------------------------------------

def split_hostline(line):
    '''
    Split hostline with this two syntax:

        - arch#recipes:nodelist/
        - arch:nodelist/
    
    The pattern can be repeated with / as separator

    '''

    # find the pattern that mathc with re
    print(line)
    reg_compiled = re.compile(re_parser_hostlist)
    result = reg_compiled.findall(line)
    print(result[:])
    architecture = []

    for r in result:

        #check if node is env var and substitute it
        if "$" in r[1]:
            r[1] = os.path.expandvars(r[1])
        #split nodelist 
        nodes_splitted = "".join(r[1]).split(",")
        
        #check if submission recipes is default or other
        #if r[3] is not '':
        #    architecture.append({"arch":r[2],"setting":r[3],"nodes":nodes_splitted})
        #else:
        architecture.append({"arch":r[0],"setting":"default","nodes":nodes_splitted})
   
    return architecture
    
    

####--------------------------------------------------------------------------------------------------------------

def list_to_String(slist,separator):
    '''
    Return string from list symbol separeted and remove newline
    '''

    return remove_newline_in(separator.join(slist)) 


####--------------------------------------------------------------------------------------------------------------

def remove_newline_in(stringline):
    '''
    remove newline at the end of the string
    '''
    if stringline.endswith("\r\n"): 
        return stringline[:-2]
    if stringline.endswith("\n"): 
        return stringline[:-1]
    else :
        return stringline


####--------------------------------------------------------------------------------------------------------------        

def get_setting_file_path(filename):

    """ Return setting file given its name, the search path is in oreder etc and etc/default """

    check_file = os.path.realpath(os.path.expanduser(__file__))
    check_prefix = os.path.dirname(os.path.dirname(os.path.dirname(check_file)))
    
    ## set setting file path
    check_setting_path = " "
    check_setting_path_standard = check_prefix+"/etc/"+filename
    check_setting_path_default  = check_prefix+"/etc/default/"+filename
    
    ## check if you create a personal setting file
    if os.path.exists(check_setting_path_standard):
        check_setting_path = check_setting_path_standard
    
    ## check if setting file is in default location
    elif os.path.exists(check_setting_path_default):
        check_setting_path = check_setting_path_default
    
    ## setting file not found
    else:
        sys.exit("ERROR CHECK setting file not found:"+filename)

    return check_setting_path

####--------------------------------------------------------------------------------------------------------------  

def get_iter_object_from_dictionary(d):
    """ Return different iter object of dictionary, the objects depends to python version"""

    if sys.version_info[:2] < (3,0):
        return d.iteritems()
    else:
        return d.items()

####--------------------------------------------------------------------------------------------------------------
