#
# CHECK
#
# @authors : Eric Pascolo, Roberto Da Via
#

re_scientific_notation = '[\s=]+([+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+))$'
re_path = '^(/)([^/\0]+(/)?)+$'
re_splitsoftware = '[@#]'
re_parser_hostlist='(([^\/^:\d]{1,})#([^:\d]{1,}))|([^:.]{1,}):([^:.]{1,})([\/]|\n)'
