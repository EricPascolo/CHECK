import os
import regex


def resolve_env_path(dictionary):
    for key, value in dictionary.items():

        try:
            path = os.path.expandvars(value)
            if is_valid(path):
                dictionary[key] = path
        except:
            pass

def is_valid(path):
    
    prog = regex.compile(r"^(/)([^/\0]+(/)?)+$")
    valid = prog.match(path)
    if valid is None:
        return False
    else:
        return True

             

