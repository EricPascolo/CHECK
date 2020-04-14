#
# CHECK
#
# @authors : Eric Pascolo
#


# extract path of bin directory and after cut it to obtain CHECK package path
BINDIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd -P)
CHECK_PATH=${BINDIR%%bin}

export CHECK_HOME=$CHECK_PATH
export CHECK_IM_REMOTE=${CHECK_HOME%%check/}
#set bin path to system path and package path to python path
export PATH=$BINDIR:$PATH
export PYTHONPATH=$CHECK_PATH:$PYTHONPATH
alias pyccleandir="find . -name '*.pyc' -delete"
alias checkcleandir='cd $CHECK_HOME ; pyccleandir ; cd $OLDPWD'
