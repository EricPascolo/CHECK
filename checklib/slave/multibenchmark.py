#
# CHECK
#
# @authors : Eric Pascolo
#

import logging

####--------------------------------------------------------------------------------------------------------------

def simple_mb_analisys(result_array):
    """
    Simpler multibenchmark analyssis, the node result is computed using this schema:

    - OK : if all result are OK
    - WARNING : if some results are warning
    - DEEP WARNING : if all results are warning
    - DOWN : if some results are DOWN
    - FAIL : if some benchmatk was not executed

    """
    
    check_status_dictionary = {"DOWN":3.14,"WARNING":5,"OK":6,"FAIL":0}

    final_mark = 1

    for m in result_array:
        partial = float(check_status_dictionary[m.status])
        final_mark = partial * final_mark

    if final_mark == 0:
        mark = "FAIL"
    elif final_mark%1 != 0:
        mark = "DOWN"
    elif final_mark == check_status_dictionary["OK"]**len(result_array):
        mark = "OK"
    elif 1 < final_mark < check_status_dictionary["OK"]**len(result_array):
        if (final_mark % 2 == 0): #even 
            mark = "WARNING"
        else: 
            mark = "DEEP WARNING"

    return mark

####--------------------------------------------------------------------------------------------------------------

def  analisys(check_core,check_result_array):

    logger = logging.getLogger(check_core.setting["logger_name"])
    
    mark = "empty"
    
    if "analysis" not in check_core.setting:
        mark = simple_mb_analisys(check_result_array)

    elif  check_core.setting["analysis"] == "simple":
        mark = simple_mb_analisys(check_result_array)
    else:
        logger.info("NOT MULTIBENCHMARK ANALYSIS FOUND")

    return mark

####--------------------------------------------------------------------------------------------------------------