#
# CHECK
#
# @authors : Eric Pascolo and Giacomo Guiduzzi
#


# extract path of bin directory and after cut it to obtain CHECK package path
BINDIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd -P)
CHECK_PATH=${BINDIR%%bin}
# separates CHECK's path substituting slashes with whitespaces (// = global sostitution)
# this allows bash to interpret this string as an array, the round parenthesis are for that
# then it accesses the last element of the array which is the name of the folder that contains CHECK
# this is because the folder that contains CHECK could be named whatever the user wants
CHECK_FOLDER_NAME=(${CHECK_PATH//// })
CHECK_FOLDER_NAME=${CHECK_FOLDER_NAME[-1]}

export CHECK_HOME=$CHECK_PATH

export CHECK_IM_REMOTE=${CHECK_HOME%%$CHECK_FOLDER_NAME/}

# set bin path to system path and package path to python path
# search for CHECK's path in $PATH, add if not present
if [[ ":$PATH:" != *":$BINDIR:"* ]]; then
    export PATH=$BINDIR:$PATH
fi

if [[ -z $PYTHONPATH ]]; then
    export PYTHONPATH=$CHECK_PATH
else
    export PYTHONPATH=$CHECK_PATH:$PYTHONPATH
fi

alias pyccleandir="find . -name '*.pyc' -delete"
alias checkcleandir='cd $CHECK_HOME ; pyccleandir ; cd $OLDPWD'


