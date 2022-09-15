
class check_result:
    """
    Class that describe checktest results
    """

####--------------------------------------------------------------------------------------------------------------   
    
    def __init__(self, name=None, status=None):
        self._benchmark = " "
        self.measure = 0.0
        self.udm = " "
        self.status = "FAIL"

        if status == "FAIL":
            self._benchmark = name
            self.status = "FAIL"
            self.measure = -999.0
            self.udm = "empty"
        
        if status is not None:
            self.status = status

        if name is not None:
            self.name = name

    def __str__(self):
        return f"{self.measure} {self.udm} \t {self.status}"

####--------------------------------------------------------------------------------------------------------------

