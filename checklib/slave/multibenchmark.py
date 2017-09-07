
from checklib.core.checkobj_result import check_result

def simple_mb_analisys(result_array):
    """
    Simpler multibenchmark analyssis, the node result is computed using this schema:

    - OK : if all result are OK
    - WARNING : if some results are warning
    - DEEP WARNING : if all results are warning
    - DOWN : if some results are DOWN
    - FAIL : if some benchmatk was not executed

    """
    final_mark = 1

    for m in result_array:
        partial = float(check_result.check_status_dictionary[m.status])
        final_mark = partial * final_mark

    if final_mark == 0:
        mark = "FAIL"
    elif final_mark%1 != 0:
        mark = "DOWN"
    elif final_mark == check_result.check_status_dictionary["OK"]**len(result_array):
        mark = "OK"
    elif 1 < final_mark < check_result.check_status_dictionary["OK"]**len(result_array):
        if (final_mark % 2 == 0): #even 
            mark = "WARNING"
        else: 
            mark = "DEEP WARNING"


    return mark,final_mark