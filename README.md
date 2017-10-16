# CHECK : Cluster Health and Environment ChecKing system



 Check is a flexible and easy to use software for showing the performance and health of an HPC Cluster. The software consists of two directories/repositories: **CHECK** contains the executable and the python library infrastructure and **CHECKTEST** contains the description of the architectures and test recipes. Check can be used via shell,parallel shell and via a scheduler; if a parallel shared file system is not installed, **CHECK** can be distrubuted on all cluster nodes and is callable from the Master node. A **CHECKTEST** is a little python class based on *check_test_template*, so extending the code is very easy: you just add a python class in the checktest directory using **CHECKTEST** policy and at runtime your new test will be available. The software is callable from the command line and through a launch string it is possible redefine on the fly almost all paramenters contained in configuration file.

***

## CHECK

### 0. *Environment setup*
**CHECK** does not require a formal installation. You can download wherever you want from the repository and use  the *source command* to load the environment from setup_check.sh.
You find setup file in **check/bin** :

    source check/bin/setup_check.sh

After the environment has loaded, you find the **CHECK** command in your $PATH and in the $CHECK_HOME variable you find the check directory path; 
**CHECK** setup also adds the CHECK_HOME path to PYTHONPATH, so attention please when you use CHECK with other modules or python packages.

### 1. *Command line*
**CHECK** is callable only from commandline(CL), since at the moment the GUI is not implmented. Please, before launch remember to edit the configuration file in *etc* (see next section). 
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



With no arguments CHECK starts and it warns you that ***checktest list is empty***. To specify what **CHECKTEST** you would like to run you must use the **--check** flag:

    check --check linpack

This command implies that you haven't defined *linpack* to test the target architecture - *linpack* can benchmark all architetures. If you define a test to a target architecture, you must use:

    check --check linpack@x86

If you have just written **CHECKTEST** recipes(with install method) but you haven't generated the exe to launch the software, you can use the follow command to finalize the **CHECKTEST** installation:

    check --check linpack@x86 --install

For each **CHECKTEST**, **CHECK** return a **mark** ( e.g. OK,DOWN,WARNING ) defined in multibenchmark analysis class, you can personalize your analysis and call it with another sepcific flag:

    check --check linpack@x86,stream@x86 --analysis simple 

**CHECK** provide a very flexible environment; indeed you can define at runtime the CHECKTEST directory,loglevel and logfile overwriting the configuration loaded from file.
To change the **CHECKTEST** directory you can use this flag ( abbr. -checkTD):

    check --check my_personal_linpack --checktest_directory $HOME/my_personal_checktest

To change log level and logfile you can use:

    check --check linpack@x86 --loglevel INFO --logfile $HOME/log.check

The flags **--master** and **--hostlist** are used when you launch tests, via the scheduler, on the HPC cluster node. Through *master* flag you enable scheduler mode and with *hostlist* (to syntax see section below, abbr *-hpc*) you specify the cluster nodes where **CHECK** launches the tests:

    check --check linpack@x86,linpack@knl --master --hostlist x86:node1,node2/knl:node3,node4/

The *--configuration* flag takes a configuration file as input, this file must be written in json format and is an easy way to avoid writing long **CHECK** command lines:

    check --configuration myconffile.json

In **CHECK** you can write all parameters in the command line, via theconfiguration file passed by command line or in the configuration file in the etc directory. The priority order used to assign a parameter vaule is as follows:

        command line > file pass by CL > file in etc

### 2. *CHECK etc*

In **check/etc/** directory you can define your configuration file in json format named *check_setting.json* . The configuration file in etc overwrites the configuration file template in **check/etc/default/**; if the first doesn't exist the last is read. The structure of file is as follows:

    {
    "loglevel":"DEBUG",
    "logtype":"both",   
    "logfile":"$HOME/checklog.txt",
    "resultfile":"$HOME/checkresult.txt",
    "checktest_directory":"$HOME/checktest/",
    "check_remote_source_path":"$SCRATCH_LOCAL/usprod/",
    "check_master_collecting_path":"$HOME/check_master_collection"
    }

In the configuration file you can use environment variables because check is able to resolve them. 

The **loglevel** parameter can have 3 values in descending order of verbosity:

 - DEBUG
 - INFO 
 - CRITICAL

**CHECK** run result and error are written as CRITICAL level, partial results and other configuration indformation are writed as INFO and developer information are written as DEBUG level.
The **logtype** field allow to choose where the log is printed:

 - cl : print log on terminal
 - file : print log on file
 - both : print log on terminal and file

If you choose *file* or *both* you can specify the path of the log file in field **logfile**.

The result of CHECK is always written in the log and in a file, you can choose the path of this file with **resultfile** field; in that file you find only the result of *last run* of **CHECK**.

The **checktest_directory** is the field where the path of the directory that contains checktests is defined.

**check_remote_source_path** is the path, in the remote node where  **CHECK** directory is located; this path is necessary for loading the check environment.

**check_master_collecting_path** is the path on the master node, where CHECK is launched and used to store the scheduler output file.

### 3. *MASTER mode and Architectures*

**CHECK** can use scheduler to submit the **CHECKTEST** directly on cluster nodes. At the moment **CHECK** create a job for each node and submit it to scheduler. The cluster node must be conteined on hostlist passed to CHECK by *--hostlist* flag.

The structure of the hostlist line is as follows:

        architecture#setting:hostname1,hostname2.../

The **architecture** is the name of the architecture file (without extension) in **CHECKTEST** directory and for each architecture you can define many scheduler **setting**. After ':' we must put the list of hostname separated by comma. You can specify in the same hostline different architectures, for example in a heterogenous HPC cluster, simply repeat the line without space between them.
    
    arch#setting:hostname1,hostname2.../arch2:hostname3,hostname4/

Is not necessary to specify a name of setting for each architecture, as in the example above for arch2 **CHECK** loads the *default* setting for that architecture.

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

**CHECKTEST** is a python package so at each directory level there must exist a _ init_.py file. The **CHECKTEST**  recipes are contained in  _ init_.py file at the end of descriptor directory. 
In the example structure reported above we have two **CHECKTEST** write extended:
  
  - test1/x86/__ init__.py this test is named *"test1"* and is designed to x86 target architecture
  - test2/__ init__.py this test is named *"test2"* and is designed to all architecture.

Into *__init__.py* the name of the python class to import in **CHECK** must have the same name of **CHECKTEST**, so in the previous example test1 or test2.

In **CHECK**, you select what **CHECKTEST** and the target architecture with the symbol **"@"**:
    
    check --check test1@x86

For each architecture file it is allowed have different configurations, so in the **CHECKTEST** directory we can have for arch1 many configurations and it is possible define them through the symbol **"\_"**. In example above for the x512 architecture file we have two different memory configurations x512_mem1,x512_mem2; this mean that in master mode on the node descripetd by x512 **CHECK** launch both x512_mem1,x512_mem2 **CHECKTEST**s; if you want launch only x512_mem1 test on the nodes you must have an architecture file with the same name.

In the test directory you can define **bin**,**in**,**out** and **tmp** directories and other but for the four cited before **CHECK** automatically generates and saves the path; if one of them is not used you can't generate.


### 2. Architecture
**CHECK** needs to find the architecture files when it is run in master mode to know the specs of the cluster nodes. The name of file in **architecture** directory must be equal to the name of the **CHECKTEST**s architecture. 

An architecture file is write in *json* format and contains a json object for each **setting**, a setting is a subset of the parameters for each architeture and in all architerture files must have a setting named *default*. 

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

The symbol  **_ noqueue _** indicates that the scheduler has an automatic selection of the queue, while the other information are classical parameter that you write in HPC job file. 

### 3. Write a CHECKTEST

**CHECK** provides a *template* to simplify the writing of **CHECKTEST** file, to write a compatible test with **CHECK** you must follow these rules:

 0) Import from **CHECK** the template to checktest class:

        from checklib.test.check_test_template import *

 1) Your test must be a python class, named as test directory and son of **CHECK**'s class **checktest** and specifies as global variable *exe* and *version*

        class linpack(checktest):

            """ Linpack class """
            exe = "xlinpack_xeon64"
            __version__ = "0.1.001"

 2) Test class can be have 5 polymorphic methods, if one is missing the corresponding father methods will be called:
   
   - **preproc** : action to execute before run
   - **run** : call with Popen exe and run the true benchmark
   - **postproc** : action to execute to extract results from output
   - **comparison** : given software outup assign a **mark** of the benchmark
   - **install** : recipes to download,compile and install the benchmark

 3) *comparison* method must return to CHECK a **check_result** object that is directly imported by the father class. The object has this structure:
    
        result = check_result()
        result._bechmark = "linpack"
        result.measure = 2000
        result.udm = "GFLOPS"
        result.status = "OK"

 4) In the *run* method it recommends using the Popen package from subprocess module to launch executable, subprocess is directly imported by father class. To collect stdout, it is recommended use a code like this:

         
        process = subprocess.Popen( [self.exe,"./input.txt"], shell=False,cwd=self.test_dir["in_dir"],stdout=subprocess.PIPE,env=os.environ)
        self.std_out, self.std_err = process.communicate()

 5) Use the directory structure provided by CHECK. If you put the executable in the **bin** absolute path is automatically generated given name of exe in *self.exe* variable. Use:
    
    - **bin** to store executable
    - **in** to store input file
    - **out** to store output
    - **tmp** to place temporaney file

 6) Check what CHECK's template  methods is offered to you, don't rewrite the useless code or if you think your code is useful for all integrated in the template. 

***
