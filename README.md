# CHECK : Cluster Health and Environment ChecKing system



 Check is a flexible and easy to use software to have a status of Performance and Heath of HPC Cluster. The software is compososed by two directory/repository, **CHECK** contains the executable and all python libray infrastructure and **CHECKTEST** contains the description of architectures and test recipes. Check can be used via shell,parallel shell and via scheduler; if a parallel shared file system is not installed, **CHECK** can be distrubuted on all cluster node and is callable from the Master node. A **CHECKTEST** is a little python class based on *check_test_template*, so extend the code is very easy, it be enough add a python class in checktest directiory using **CHECKTEST** policy and at runtime your new test it will be available. The software is callable to command line and through lunch string it is possible redefine on the fly almost all paramenter conteined in configuration file.

***

## CHECK

### 0. *Environment setup*
**CHECK** not require a formal installation. You can download wherever you want the repository and use *source command* to load environment from setup_check.sh.
You find setup file in **check/bin** :

    source check/bin/setup_check.sh

After the environment was loaded, you find **CHECK** command in your $PATH and in the $CHECK_HOME variable you find check directory path; 
**CHECK** setup moreover add CHECK_HOME path to PYTHONPATH, so attention please when you use CHECK with other module or python package.

### 1. *Command line*
**CHECK** is callable only from commandline(CL), at the moment GUI is not implmented. Please, before launch remind to edit configuration file in *etc* (see next section). 
To see all CL flags use **--help** flag:


CHECK 0.1.003 START 
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



With no argument CHECK start and it warn you that ***CHECKtest list is empty***. To specifies what **CHECKTEST** you would like to run you must use **--check** flag:

    check --check linpack

This command implies that you haven't defined *linpack* test to targer architecture, *linpack* can benchmark all architetures. If you define a test to a target architecture, you must use:

    check --check linpack@x86

If you have just written **CHECKTEST** recipes(with install method) but you don't have generated the exe to launch the software, you can use the follow command to finalize the **CHECKTEST** installation:

    check --check linpack@x86 --install

For each **CHECKTEST**, **CHECK** return a **mark** ( e.g. OK,DOWN,WARNING ) defined in multybenchmark analysis class, you can personalize your analysis and call it with another sepcific flag:

    check --check linpack@x86,stream@x86 --analysis simple 

**CHECK** provide a very flexible environment, indeed you can define at runtime the CHECKTEST directory,loglevel and logfile overwriting the confinguration loaded from file.
To change **CHECKTEST** directory you can use this flag ( abbr. -checkTD):

    check --check my_personal_linpack --checktest_directory $HOME/my_personal_checktest

To change log level and logfile you can use:

    check --check linpack@x86 --loglevel INFO --logfile $HOME/log.check

The flags **--master** and **--hostlist** is used when you want to launch tests via scheduler on HPC cluster node. Trhough *master* flag you enable scheduler mode and with *hostlist* (to syntax see section below, abbr *-hpc*) you specifie the cluster nodes where **CHECK** launch the tests:

    check --check linpack@x86,linpack@knl --master --hostlist x86:node1,node2/knl:node3,node4/

The configuration flag takes a configuration file as input, in file you can specify all **CHECK** parameter and they will be overwrited conf file loaded to etc moreover you can add CL paramenter in this file with correct tname and format:

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

The CHECKTEST directory must have this structure:

                                 checktest
                                     |
                    ----------------------------------------
                    |                |                      | 
                architecture       test1                  test2
                - x86.json           |                      |
                - x512.json          |                 -----------------------
                - GPU.json           |                 |            |        |
                                     |             __init__.py     bin       tmp 
                                     |
                        --------------------------------
                        |      |           |           |
                        x86    x512_mem1   x512_mem2   GPU
                        |
                        |
                    -----------------------
                    |            |        |
                __init__.py     bin       in 

CHECKTEST is a python package so at each directory level must exist a _ init_.py file. The CHECKTESTs are conteined in  _ init_.py file at the end of descriptor directory. 
In the example structure reported above we have two CHECKTEST write extended:
  
  - test1/x86/__ init__.py this test is named *"test1"* and is designed to x86 target architecture
  - test2/__ init__.py this test is named *"test2"* and is designed to all architecture.

Into *__init__.py* the name of the class to import in CHECK must be named ad checktest so in the previous example test1 or test2.

In CHECK selected what CHECKTEST you woul'd run  you can defin the target architecture with the symbol **"@"**:
    
    check --check test1@x86

For each architecture files it is allow have different configuration, so in CHECKTEST directory we can have for arch1 many configuration and iti is possible trough the symbol **"*"**. In example above for he architecture file x512 we have two different memory configuration x512_mem1,x512_mem2; this mean that in master mode on the node descripetd by x512 CHECK launch both x512_mem1,x512_mem2 CHECKTESTs; if you want launch only x512_mem1 test on the nodes you must have an architecture file with the same name.

In test directory we can define **bin**,**in**,**out** and **tmp** directory and other but for the four cited CHECK automaticcaly generate the path; if one of this four is not used you can't generate.


### 2. Architecture
The architecture files need when CHECK is runned in master mode to know the features of the cluster nodes. The name of the file in **architeture** directory must be equals to name of CHECKTESTs architecture. 

An architecture file is write in *json* format and contain a json object for each **setting**, a setting is a subset of setting for each architeture, in all architerture file must have a setting named *default*. 

Below an architecture file example:

    {
    "default":{

        "number_of_nodes":"1",
        "ncpus":"36",
        "memory":"118GB",
        "walltime":"00:15:00",
        "queue":"__noqueue__",
        "account":"my_account"

    },

    "debug":{
        
            "number_of_nodes":"1",
            "ncpus":"36",
            "memory":"118GB",
            "walltime":"00:15:00",
            "queue":"debug",
            "account":"my_account"
        
            }

    }

The symbol  **_ noqueue _** indicate that the scheduler have an automatic selection of the queue while the other information is classical information that you write in HPC job file. The difference beetween two setting is that the first have automatic queue selection, indeed the second submit the job on *debug* queue.

### 3. Write a CHECKTEST

CHECK provides a *template* to simplify a write of CHECKTEST file, for write a compatible test with CHECK you must follow this rules:

 0) Import from CHECK the template to checktest class:

        from checklib.test.check_test_template import *

 1) Your test must be a python class, named as test directory and son of CHECK's class **checktest**, and specifies as global variable *exe* and *version*

        class linpack(checktest):

            """ Linpack class """
            exe = "xlinpack_xeon64"
            __version__ = "0.1.001"

 2) test class can be have 5 polymorphic methods, if one miss the corrisponding father methods will be called:
   
   - **preproc** : action to execute before run
   - **run** : call with Popen exe and run the true benchmark
   - **postproc** : action to execute to extract results from output
   - **comparison** : given software outup assign a **mark** of the benchmark
   - **install** : recipes to download,compile and install the benchmark

 3) *comparison* mehtod must return to CHECK a **check_result** object that is direct imported by father class. The object have this structure:
    
        result = check_result()
        result._bechmark = "linpack"
        result.measure = 2000
        result.udm = "GFLOPS"
        result.status = "OK"

 4) In *run* method it recomends to use Popen package from subprocess to launch executable, subprocess is directly imported by father class. To collect with python stdout and analyze before, it is recomanded use a code like that:

         
        process = subprocess.Popen( [self.exe,"./input.txt"], shell=False,cwd=self.test_dir["in_dir"],stdout=subprocess.PIPE,env=os.environ)
        self.std_out, self.std_err = process.communicate()

 5) Use the directory structure provide by CHECK. If you put executable in **bin** absolute path is automatically generetad given name of exe in *self.exe* variable. Use:
    
    - **bin** to store executable
    - **in** to store input file
    - **out** to store output
    - **tmp** to place temporaney file

 6) Check what CHECK's template  methods is offered, don't rewrite the useless code or if you think that the code is usefull for all integrated it in template. 
***
