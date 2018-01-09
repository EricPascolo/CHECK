
class scheduler:
    
    '''   Virtual class that provide structure to scheduler interface '''
    
    def __init__(self):
        self.name = "generic"

    def scheduler_string_generator(self,arch_setting):
        
        ''' 
        
            Virtual function that generate scheduler interface string given architecture setting.
            The string is composed by:

                    scheduler_exe   scheduler_paramenter   scheduler_inline_anchor_to_slave_command 
            
        '''
        
        return "generic scheduler"



