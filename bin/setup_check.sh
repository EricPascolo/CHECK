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



# extract path of bin directory and after cut it to obtain CHECK package path
BINDIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd -P)
CHECK_PATH=${BINDIR%%bin}

export CHECK_HOME=$CHECK_PATH
#set bin path to system path and package path to python path
export PATH=$BINDIR:$PATH
export PYTHONPATH=$CHECK_PATH:$PWD
alias checkcleandir='cd $CHECK_HOME ; find . -name '*.pyc' -delete'