#
# CHECK
#
# @authors : Eric Pascolo
#


import os
import regex
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

    #regex to check path
    prog = regex.compile(regex_path)#(r"^(/)([^/\0]+(/)?)+$")
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
    prog = regex.compile(regex_splitsoftware)
    software_list = regex.split(regex_splitsoftware,software_string)

    software_hardware = ""
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

    reg_compiled = regex.compile(regex_parser_hostlist)
    result = reg_compiled.findall(line)

    architecture = []

    for r in result:
        nodes_splitted = "".join(r[5]).split(",")
        if r[3] is not '':
            architecture.append({"arch":r[2],"setting":r[3],"nodes":nodes_splitted})
        else:
            architecture.append({"arch":r[4],"setting":"default","nodes":nodes_splitted})
   
    return architecture
    
    

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