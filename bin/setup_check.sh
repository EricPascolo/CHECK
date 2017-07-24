#
# CHECK
#
# @authors : Eric Pascolo
#


# extract path of bin directory and after cut it to obtain CHECK package path
BINDIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd -P)
CHECK_PATH=${BINDIR%%bin}

export CHECK_HOME=$CHECK_PATH
#set bin path to system path and package path to python path
export PATH=$BINDIR:$PATH
export PYTHONPATH=$CHECK_PATH:$PWD
alias checkcleandir='cd $CHECK_HOME ; find . -name '*.pyc' -delete'