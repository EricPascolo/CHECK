#
# CHECKS v 0.1
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






def argument():
    parser = argparse.ArgumentParser(description = '''
    Python check suite to HPC C
    ''',
    formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(   '--hpc_cluster', '-hpc',
                                type = str,
                                required =False,
                                help = ''' Input image'''
                                )
  
    parser.add_argument(   '--operation', '-op',
                                type = int,
                                required = False,
                                default = 0,
                                choices=[-1,0,1,2,3],
                                help = 'Number of operation')
  
    return parser.parse_args()




