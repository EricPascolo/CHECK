# CHECK : Cluster Health and Environment ChecKing system



 Check is a flexible and easy to use software to have a faster snapshot of Performance and Status of HPC Cluster. The software is compososed by two directory/repository, this one **check** that contain the executable and all infrastructure python library and **checktest** that contain the description of architectures and  test recipes. Check can be used via shell,parallel shell and via scheduler, if a parallel shared file system is not installed, CHECK can be distrubute on all cluster node and call from the Master node. A CheckTest is a little python class based on checktest template, so extend the code is very easy, it be enough add a python class in checktest directiory using CHECK plugin policy and at runtime your new test it will be available. The software is callable to command line and through lunch string you can redefine on the fly almost all paramenter conteined in etc conf file.

***

## CHECK

### 0. *Environment setup*
CHECK not require a formal installation. You can download wherever you want and use *source command* to load environment from setup_check.sh.
You find setup file in **check/bin** :

    source check/bin/setup_check.sh

After the environment was loaded, you find **check** command in your $PATH and the in the $CHECK_HOME variable you find the check directory path. 
Check setup moreover add CHECK_HOME path to PYTHONPATH so attention please when you use CHECK with other module or python package.

### 1. *Command line*
Check is calleble only from commandline(CL), before launch remind to edit configuration file in *etc* (see next guide section). 
To see all CL flags use **--help** flag:


    CHECK 0.1.002 START 
    usage: check [-h] [--master] [--install] [--check CHECK [CHECK ...]]
                [--configuration CONFIGURATION] [--analysis ANALYSIS]
                [--loglevel LOGLEVEL] [--logfile LOGFILE]
                [--checktest_directory CHECKTEST_DIRECTORY] [--hostlist HOSTLIST]

        CHECK : Cluster Health and Environment ChecKing system

    optional arguments:
    -h, --help            show this help message and exit
    --master              Master/slave flag
    --install             Install checktest
    --check CHECK [CHECK ...], -ct CHECK [CHECK ...]
                            List of check
    --configuration CONFIGURATION
                            Input file
    --analysis ANALYSIS   kind of analysis
    --loglevel LOGLEVEL   Input file
    --logfile LOGFILE     Input file
    --checktest_directory CHECKTEST_DIRECTORY, -checkTD CHECKTEST_DIRECTORY
                            check test directory
    --hostlist HOSTLIST, -hpc HOSTLIST
                            List of Hostname to Master submission


With no argument CHECK start and warn you that ***CHECKtest list is empty***. To specifies what checktest you want to run you must use **--check** flag:

    check --check linpack

This command implies that you have defined *linpack* test to not targer architecture. If you define a test to a target architecture, you must use:

    check --check linpack@x86

If you have just written CHECKTEST recipes(with install method) but you don't have generate the executable to launch the software, you can use the follow command to finalize the CHECKTEST installation:

    check --check linpack@x86 --install

For each CHECKTEST, CHECK return a **mark** ( in example OK,DOWN,WARNING ) defined in multybenchmark analysis class, you can personalize your analysis and call it with a sepcific flag:

    check --check linpack@x86,stream@x86 --analysis simple 

To provide a very flexible environment,you can define at runtime the CHECKTEST directory,loglevel and logfile overwriting the confinguration loaded from file.
To change CHECKTEST directory you can use this flag:

    check --check my_personal_linpack --checktest_directory $HOME/my_personal_checktest

To change log level and logfile you can use:

    check --check linpack@x86 --loglevel INFO --logfile $HOME/log.check

The flags **--master** and **--hostline** is used when you use a scheduler to submit CHECKTEST on cluster node. Trhough *master* flag you enable scheduler mode and with *hostlist* (to syntax see section below) you specifies the cluster nodes where CHECK launch the bechmark:

    check --check linpack@x86,linpack@knl --master --hostlist x86:node1,node2/knl:node3,node4/

The configuration flag take a configuration file as input, in file you can specify all CHECK parameter to overwrite conf file loaded to etc moreover you can add CL paramenter in this file with correct tname and format:

    check --configuration myconffile.json

### 2. *CHECK etc*

In **check/etc/** directory you can define your configuration file in json format named check_setting.json . Configuration file in etc overwrite the configuration file template in **check/etc/default/**

    {
    "loglevel":"DEBUG",
    "logtype":"both",   
    "logfile":"$HOME/checklog.txt",
    "resultfile":"$HOME/checkresult.txt",
    "checktest_directory":"$HOME/checktest/",
    "check_remote_source_path":"$SCRATCH_LOCAL/usprod/",
    "check_master_collecting_path":"$HOME/check_master_collection"
    }

In configuration file you can use environment variable beecuase check is able to resolve the string. 

The **loglevel** parameter can have 3 value in order of verbosity:

 - DEBUG
 - INFO 
 - CRITICAL

CHECK run result and error are write as CRITICAL level, partial results and other configuration indformation are writed as INFO and developper information are writed as DEBUG level.
The **logtype** field allow to choose where the log is printed:

 - cl : print log on terminal
 - file : print log on file
 - both : print log on terminal and file

If you choose *file* or *both* you can specify the path of log file in field **logfile**.

The result of CHECK is always write in the log and in a file, you can choose the path of this file with **resultfile** field; in that file you find only the result of last run of CHECK.

The **checktest_directory** is the field where is defined the path of the directory that contain checktests.

**check_remote_source_path** is the path in remote node where is located *check* directory, this path is necessary to load check environment.

**check_master_colletting_path** is path on the node where CHECK i launched as master where to store scheduler output file.

### 3. *MASTER mode and Architectures*

Check can use scheduler to submit the checktest directly on cluster node. At the moment CHECK create a job for each node and submit it to scheduler. The cluster node must be conteined on hostlist pass to CHECK by *--hostlist* flag.

The structure of the line of hostlist is the follow:

        arch#setting:hostname1,hostname2.../

The **architecture** is the name of architecture file in CHECKTEST directory and for each architecture can have different scheduler **setting**. After ':' we must put the list of hostname separated by comma. We can specifies in the same hostline different architectures, in example for etherogeneus HPC cluster, simply reapeat che line without space among them.
    
    arch#setting:hostname1,hostname2.../arch2:hostname3,hostname4/

Is not necessary to specify a name of setting for each architecture, as in the second arch in the line below but in this case we load *default* setting for that architecture.

***

## CHECKTEST

### 1. Structure of directory

### 2. Architecture

### 3. Write a CHECKTEST

----

## Developper guide