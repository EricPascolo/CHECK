
#
# CHECKS v 0.1
#
# @authors : Eric Pascolo
#
# Copyright (C) 2017 B.U HPC - CINECA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import argparse

def cl_parser():
    parser = argparse.ArgumentParser(description = '''
    Python check suite to HPC Cluster
    ''',
    formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(   '--master', '-m',
                            type = str,
                            required = False,
                            default = "./conf.json",
                            help = 'Master/slave flag')

    parser.add_argument(   '--hpc', '-h',
                                type = str,
                                required =False,
                                help = ''' Cluster hostfile'''
                                )
  
    parser.add_argument(   '--check', '-c',
                                type = int,
                                required = False,
                                default = 0,
                                help = 'List of check')

    parser.add_argument(   '--configuration', '-c',
                                type = int,
                                required = False,
                                default = 0,
                                help = 'Input file')
  
    return parser.parse_args()