#
# CHECK
#
# @authors : Eric Pascolo
#

import sys
import json
import os

"""
Python module that contain read file methods
"""

####--------------------------------------------------------------------------------------------------------------

def json_reader(filepath):
    """
    Checking existence of json file and read it
    """
    filecontained = "-999"
    try:
        if os.path.isfile(filepath) :
            filecontained = json.loads(open(filepath).read())
        else :
            sys.exit()

    except:
        sys.exit("ERROR JSON file not readable "+filepath)

    return filecontained

####--------------------------------------------------------------------------------------------------------------

def hpc_map_file_reader(hpcmap_file):
    """
    Read a file that contains hpc map
    Each row is composed by:

        -name of the row
        -array of string, comma separated
    
    The output is a dictionary of string array, the key is name of the row

    """

    hpcmap = {}

    hpc_groups = generic_file_reader(hpcmap_file)

    for group in hpc_groups:
        group_name, group_array = group.split(" ")
        group_nodes = group_array.split(",")
        hpcmap.update({group_name: group_nodes}) 

    return hpcmap

####--------------------------------------------------------------------------------------------------------------

def generic_file_reader(filename):
    """
        Read a generic ascii file and return an array of string (1 per row)
    """
    rows_from_file = []
    if os.path.isfile(filename):
        file_toread = open(filename, 'r')
        rows_from_file = file_toread.readlines()
        file_toread.close()
    else:
        print("ERROR file dosn't exist:"+filename)

    return rows_from_file

####--------------------------------------------------------------------------------------------------------------