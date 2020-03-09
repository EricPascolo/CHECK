#
# CHECK
#
# @authors : Eric Pascolo, Roberto Da Via
#

re_scientific_notation = '[\s=]+([+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+))$'
re_path = '^(/)([^/\0]+(/)?)+$'
re_splitsoftware = '[@#]'

# Details of re_parser_hostlist:
#'(([^:^#^\/.]{1,})|([^:^\/.]{1,})#([^:^\/.]{1,})):([^:^\/.]{1,})'
#
# - group0: architecture w/wo settings
#    - group1: architecture if no settings given, empty otherwise
#         ([^:^#^\/.]{1,}) -> explicitly exclude # symbol, to avoid 
#         an overlap between group1 and group 2&3
#    - group2: architecture if settings are given (# is present), 
#         empty otherwise
#         ([^:^\/.]{1,})
#    - group3: settings, if given, empty otherwise
#         ([^:^\/.]{1,})
# - group4: nodelist, group read after ':'
#         ([^:^\/.]{1,})
# Example line: 'mkl:r055c19s13,r033c01s05,r033c03s08/x86#info:r033c01s05'
# Expected output: [
#                    ('mkl', 'mkl', '', '', 'r055c19s13,r033c01s05,r033c03s08'), 
#                    ('x86#info', '', 'x86', 'info', 'r033c01s05')
#                  ]
#
re_parser_hostlist='(([^:^#^\/.]{1,})|([^:^\/.]{1,})#([^:^\/.]{1,})):([^:^\/.]{1,})'

