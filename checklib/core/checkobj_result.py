
class check_result:
    """
    Class that describe checktest results
    """


    _benchmark = " "
    measure = 0.0
    udm = " "
    status = "ToBOrNotToBe"
    check_status_dictionary = {"DOWN":3.14,"WARNING":5,"OK":6,"FAIL":0}
    
    def __init__(self,name=None,status=None):
        
        if status is "FAIL":
            self._benchmark = name
            self.status = "FAIL"
            self.measure = -999.0
            self.udm = "empty"
        
        if status is not None:
            self.status = status

        if name is not None:
            self.name = name

