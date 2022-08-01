#
# CHECK
#
# @authors : Eric Pascolo
#


# extract path of bin directory and after cut it to obtain CHECK package path
BINDIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd -P)
CHECK_PATH=${BINDIR%%bin}
export CHECK_HOME=$CHECK_PATH

CHECK_FOLDER_EXISTS=false

if [[ ${CHECK_HOME} == *"check"* ]];
then
        export CHECK_IM_REMOTE=${CHECK_HOME%%check/}
        CHECK_FOLDER_EXISTS=true

elif [[ ${CHECK_HOME} == *"CHECK"* ]];
then
        export CHECK_IM_REMOTE=${CHECK_HOME%%CHECK/}
        CHECK_FOLDER_EXISTS=true
else
        echo "Could not find CHECK install folder."
fi

if $CHECK_FOLDER_EXISTS;
then
        # set bin path to system path and package path to python path
        export PATH=$BINDIR:$PATH
        export PYTHONPATH=$CHECK_PATH:$PYTHONPATH
        alias pyccleandir="find . -name '*.pyc' -delete"
        alias checkcleandir='cd $CHECK_HOME ; pyccleandir ; cd $OLDPWD'
fi

