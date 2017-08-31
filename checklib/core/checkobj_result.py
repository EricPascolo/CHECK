
class check_result:
    """
    Class that describe checktest results
    """


    _benchmark = " "
    measure = 0.0
    udm = " "
    status = -9
    check_status_dictionary = ('down','warning','ok',"fail")
    
    def __init__(self,name=None,status=None):
        if status is "FAIL":
            self._benchmark = name
            self.status = 3
            self.measure = -999.0
            self.udm = "empty"
        

