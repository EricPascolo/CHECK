import os
import regex


def resolve_env_path_dic(dictionary):
    for key, value in d.items():
        path = os.path.expandvars(value)
        if is_valid(path):
            value = path





def is_valid(path):
    valid = False
    prog = re.compile('^['"]?(?:/[^/\n]+)*['"]?$')
    valide = prog.match(path)
    return valid

             

