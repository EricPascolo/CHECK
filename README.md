# CHECK : Cluster Health and Environment ChecKing system



 Check is a flexible and easy to use software to have a faster snapshot of Performance and Status of HPC Cluster. The software is compososed by two directory/repository, this one **check** that contain the executable and all infrastructure python library and **checktest** that contain the description of architectures and  test recipes. Check can be used via shell,parallel shell and via scheduler, if a parallel shared file system is not installed, CHECK can be distrubute on all cluster node and call from the Master node. A CheckTest is a little python class based on checktest template, so extend the code is very easy, it be enough add a python class in checktest directiory using CHECK plugin policy and at runtime your new test it will be available. The software is callable to command line and through lunch string you can redefine on the fly almost all paramenter conteined in etc conf file.

***

## CHECK

### 0. Environment setup
CHECK not require a formal installation. You can download wherever you want and use *source command* to load environment from setup_check.sh.
You find setup file in **check/bin** :

    source check/bin/setup_check.sh

After the environment was loaded, you find **check** command in your $PATH and the in the $CHECK_HOME variable you find the check directory path. 
Check setup moreover add CHECK_HOME path to PYTHONPATH so attention please when you use CHECK with other module or python package.

### 1. Command line
Check is calleble only from commandline(CL). To see all CL flags use **--help** flag:


    usage: check [-h] [--master] [--install] [--daemon {start,submit,status,kill}]
                [--check CHECK [CHECK ...]] [--hpc HPC]
                [--configuration CONFIGURATION] [--analysis ANALYSIS]
                [--loglevel LOGLEVEL] [--logfile LOGFILE]
                [--checktest_directory CHECKTEST_DIRECTORY] [--hostlist HOSTLIST]

        Python check suite to HPC Cluster

    optional arguments:
    -h, --help            show this help message and exit
    --master              Master/slave flag
    --install             Install checktest
    --daemon {start,submit,status,kill}
                            Daemon command
    --check CHECK [CHECK ...], -c CHECK [CHECK ...]
                            List of check
    --hpc HPC             Cluster hostfile
    --configuration CONFIGURATION
                            Input file
    --analysis ANALYSIS   kind of analysis
    --loglevel LOGLEVEL   Input file
    --logfile LOGFILE     Input file
    --checktest_directory CHECKTEST_DIRECTORY, -checkTD CHECKTEST_DIRECTORY
                            check test directory
    --hostlist HOSTLIST, -hl HOSTLIST
                            List of Hostname to Master submission

With no argument CHECK start and warn you that ***CHECKtest list is empty***. To specifies what checktest you want to run you must use **--check** flag:

    check --check linpack


### 2. CHECK etc



### 3. MASTER/SLAVE 


### 4. LOG

***

## CHECKTEST

### 1. Structure of directory

### 2. Architecture

### 3. Write a CHECKTEST

----

## Developper guide