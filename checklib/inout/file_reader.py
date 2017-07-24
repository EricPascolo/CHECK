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
