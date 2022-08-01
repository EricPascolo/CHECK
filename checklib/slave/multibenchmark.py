#
# CHECK
#
# @authors : Eric Pascolo
#

import logging

####--------------------------------------------------------------------------------------------------------------


def simple_mb_analisys(checktests):
    """
    Simpler multibenchmark analyssis, the node result is computed using this schema:

    - OK : if all result are OK
    - WARNING : if some results are warning
    - DEEP WARNING : if all results are warning
    - DOWN : if some results are DOWN
    - FAIL : if some benchmatk was not executed

    """
    
    check_status_dictionary = {"DOWN": 3.14, "WARNING": 5, "OK": 6, "FAIL": 0}

    final_mark = 1

    for checktest in checktests:
        if type(checktest.result) is list:
            for result in checktest.result:
                partial = float(check_status_dictionary[result.status])
                final_mark = partial * final_mark

        else:
            partial = float(check_status_dictionary[checktest.result.status])
            final_mark = partial * final_mark

    if final_mark == 0:
        return "FAIL"
    elif final_mark % 1 != 0:
        return "DOWN"
    elif final_mark == check_status_dictionary["OK"] ** len(checktests):
        return "OK"
    elif 1 < final_mark < check_status_dictionary["OK"] ** len(checktests):
        if (final_mark % 2) == 0:  # even
            return "WARNING"
        else:
            return "DEEP WARNING"

####--------------------------------------------------------------------------------------------------------------


def analysis(check_core):

    logger = logging.getLogger(check_core.setting["logger_name"])
    
    mark = "empty"

    analysis_setting = check_core.setting.get('analysis', None)
    
    if not analysis_setting or analysis_setting == 'simple':
        mark = simple_mb_analisys(check_core.checktests)

    else:
        logger.info("MULTIBENCHMARK ANALYSIS NOT FOUND")

    return mark

####--------------------------------------------------------------------------------------------------------------