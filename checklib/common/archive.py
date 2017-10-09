#
# CHECK
#
# @authors : Eric Pascolo
#

regex_scientific_notation = '[\s=]+([+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+))$'
regex_path = '^(/)([^/\0]+(/)?)+$'
regex_splitsoftware = '[@#]'
regex_parser_hostlist='((([^\/^:\d]{1,})#([^:\d]{1,}))|([^:.]{1,})):([^:.]{1,})\/'