# CHECK : Cluster Health and Environment ChecKing system


 Check is a flexible and easy to use software for showing the performance and health of an HPC Cluster. The software consists of two directories/repositories: **CHECK** contains the executable and the python library infrastructure and **CHECKTEST** contains the description of the architectures and test recipes. Check can be used via shell,parallel shell and via a scheduler; if a parallel  file system is not installed, **CHECK** can be distributed on all cluster nodes and is callable from the Master node. A **CHECKTEST** is a little python class based on *check_test_template*, so extending the code is very easy: you just add a python class in the checktest directory using **CHECKTEST** policy and at runtime your new test will be available. The software is callable from the command line and through a launch string it is possible redefine on the fly almost all paramenters contained in the configuration file.

***



## CHECK 0.2



### 0. *Environment setup*
**CHECK** does not require a formal installation. You can download wherever you want from the repository and use  the *source command* to load the environment from setup_check.sh.
You find setup file in **check/bin** :

    source check/bin/setup_check.sh

After the environment has loaded, you find the **CHECK** command in your $PATH and in the $CHECK_HOME variable you find the check directory path; 
**CHECK** setup also adds the CHECK_HOME path to PYTHONPATH, so attention please when you use CHECK with other modules or python packages.



### 1. *Command line*
**CHECK** is callable only from commandline(CL), since at the moment the GUI is not implmented. Please, before launch remember to edit the configuration file in *etc* (see next section). 
When you call **CHECK** command, you obtain an output like this:

    **** CHECK 0.2.2 - r64s08u38 - 17/03/2020 09:26:30 - 21fce0631c554459b526c2f25bf8791b
    21fce0631c554459b526c2f25bf8791b 09:26 [INFO] (checkloggin) : logger: check_file_stream_log type:cl
    21fce0631c554459b526c2f25bf8791b 09:26 [DEBUG] (__init__) : check_file_stream_log
    21fce0631c554459b526c2f25bf8791b 09:26 [CRITICAL] (__init__) : Checktest list is empty
    **** CHECK STOP - r64s08u38 - 17/03/2020 09:26:30 - 21fce0631c554459b526c2f25bf8791b

Each run of **CHECK** is identify with unique **ID** number reported in each line of output, it's very confortable if you run multiple istance of **CHECK** or you want repeat analys on the same node without change output file. 
The first and last line report the version, the hostname, the time and the **ID** of run.

To see all CL flags use **--help** flag:

    usage: check [-h] [--master] [--check CHECK [CHECK ...]] [--checklist]
             [--checkparameters] [--configuration CONFIGURATION]
             [--cluster_scheduler CLUSTER_SCHEDULER] [--install] [--ssh]
             [--analysis ANALYSIS] [--loglevel LOGLEVEL] [--logfile LOGFILE]
             [--resultfile RESULTFILE] [--logtype {c,l,,,f,i,l,e,,,b,o,t,h}]
             [--hpc HPC] [--singleton] [--hpc_cluster_map HPC_CLUSTER_MAP]
             [--checktest_directory CHECKTEST_DIRECTORY]
             [--check_remote_source_path CHECK_REMOTE_SOURCE_PATH]
             [--check_master_collecting_path CHECK_MASTER_COLLECTING_PATH]

    CHECK : Cluster Health and Environment ChecKing system

    optional arguments:
    -h, --help            show this help message and exit
    --master              Master slave flag
    --check CHECK [CHECK ...]
                            List of check
    --checklist           Print checktest list
    --checkparameters     Print CHECK parameter
    --master_id MASTER_ID Set id from master
    --configuration CONFIGURATION
                            Input file
    --cluster_scheduler CLUSTER_SCHEDULER
                            Name of scheduler
    --install             Install checktest
    --ssh                 Enable SSH, disable scheduler submission
    --analysis ANALYSIS   kind of analysis
    --loglevel LOGLEVEL   Log level 
    --logfile LOGFILE     Log file
    --resultfile RESULTFILE
                            Log file
    --logtype {c,l,,,f,i,l,e,,,b,o,t,h}
                            Log type
    --hpc HPC             List of Hostname to Master submission
    --singleton           Force submission to each node of group
    --hpc_cluster_map HPC_CLUSTER_MAP
                            Cluster map description file
    --checktest_directory CHECKTEST_DIRECTORY
                            check test directory
    --check_remote_source_path CHECK_REMOTE_SOURCE_PATH
                            Remote CHECK directory path
    --check_master_collecting_path CHECK_MASTER_COLLECTING_PATH
                            Directory path where collect scheduler job results



With no arguments CHECK starts and it warns you that ***checktest list is empty***. To specify what **CHECKTEST** you would like to run you must use the **--check** flag:

    check --check linpack

This command implies that you haven't defined *linpack* to test the target architecture - *linpack* can benchmark all architetures. If you define a test to a target architecture, you must use:

    check --check linpack@x86

You can see all **CHECKTEST** installed with the flag **--checklist**:

    check --cheklist
        
    -ARCHITECTURES AVAILABLE:
    --- arch1
    ----- default
    ----- queue1
    --- arch2
    ----- default
    ----- queue2
        
    -CHECKTEST AVAILABLE:

    --- test1@arch1
    --- test2@arch1
    --- test1@arch2
    --- test2@arch2
  
and you can see **CHECK** parameters with flags **--checkparameter**:

    -- check : ['test1@arch1,test2@arch1']
    -- check_master_collecting_path : $HOME/check_master_collection
    -- check_remote_source_path : /cinecalocal/usprod/
    -- checkparameters : True
    -- checktest_directory : $HOME/checktest/
    -- hostlist : arch1:node1,node2/
    -- logfile : $HOME/checklog.txt
    -- logger_name : check_file_stream_log
    -- loglevel : DEBUG
    -- logtype : cl
    -- master : True
    -- resultfile : $HOME/checkresult.txt

If you have just written **CHECKTEST** recipes(with install method) but you haven't generated the exe to launch the software, you can use the follow command to finalize the **CHECKTEST** installation:

    check --check linpack@x86 --install

For each **CHECKTEST**, **CHECK** return a **mark** ( e.g. OK,DOWN,WARNING ) defined in multibenchmark_analysis class. You can personalize your analysis and call it with another specific flag:

    check --check linpack@x86,stream@x86 --analysis simple 

**CHECK** provides a very flexible environment; indeed you can define at runtime the CHECKTEST directory,loglevel and logfile overwriting the configuration loaded from file.
To change the **CHECKTEST** directory you can use this flag ( abbr. -checkTD):

    check --check my_personal_linpack --checktest_directory $HOME/my_personal_checktest

To change log level and logfile you can use:

    check --check linpack@x86 --loglevel INFO --logfile $HOME/log.check

The flags **--master** / **--ssh** and **--hpc** are used when you launch tests, via the scheduler/ssh, on the HPC cluster node. Through *master* flag you enable master slave mode (via scheduler as default) and with *hpc* (for syntax see section below, abbr *-hpc*) you specify the cluster nodes where **CHECK** launches the tests:

    check --check linpack@x86,linpack@knl --master --hpc x86:node1,node2/knl:groupnode1/

You can also use predefined groups of nodes, like "groupnode1" in the string above. These groups of nodes are defined in the file map.hpc  in architecture directory. When you specify a group of node you can launch a 1 job on the all nodes of the group or multiple job, one for each node, the default behaviour is the first, to use the second you must add a flag **--singleton**:

    check --check linpack@x86,linpack@knl --master --hpc x86:node1,node2/knl:groupnode1/ --singleton

If you add *--ssh*, the submission of remote command is via ssh following the same rules above, in this case the singleton flag is implicit.

The *--configuration* flag takes a configuration file as input, this file must be written in json format and is an easy way to avoid writing long **CHECK** command lines:

    check --configuration myconffile.json

In **CHECK** you can write all parameters in the command line, via theconfiguration file passed by command line or in the configuration file in the etc directory. The priority order used to assign a parameter vaule is as follows:

        command line > file passed by CL > file in etc



### 2. *CHECK etc*

In **check/etc/** directory you can define your configuration file in json format named *check_setting.json* . The configuration file in etc overwrites the configuration file template in **check/etc/default/**; if the first doesn't exist the second is read. The structure of file is as follows:

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

**CHECK** run results and errors are written as CRITICAL level, partial results and other configuration information are written as INFO and developer information are written as DEBUG level.
The **logtype** field allows you to choose where the log is printed:

 - cl : print log on terminal
 - file : print log on file
 - both : print log on terminal and file

If you choose *file* or *both* you can specify the path of the log file in field **logfile**.

The result of CHECK is always written in the log and in a file, you can choose the path of this file with **resultfile** field; in that file you find only the result of *last run* of **CHECK**.

The **checktest_directory** is the field where the path of the directory that contains checktests is defined.

**check_remote_source_path** is the path, in the remote node where  **CHECK** directory is located; this path is necessary for loading the check environment.

**check_master_collecting_path** is the path on the master node, where CHECK is launched and used to store the scheduler output file.



### 3. *MASTER mode and Architectures*

**CHECK** can use a scheduler or ssh to submit the **CHECKTEST** directly on cluster nodes. At the moment **CHECK** created a job containing a istance of **CHECK** in *slave* mode and submit to scheduler or lauch ad ssh command. 
The **ID** of the slave instance is the same as the master instance. 

CHECK is designed to run on the system without a parallel FS mounted, so the position of the slave instance must be specified in the setting file via *check_remote_source_path* parameter; if the parallel FS is mouted you can use the same installation of **CHECK** as master and slave, setting the configuration parameter as $CHECK_IM_REMOTE.

The cluster node must be present on hostlist passed to CHECK by *--hpc* flag.

The structure of the hostlist line is as follows:

        architecture#setting:hostname1,GroupOfNodes1.../

The **architecture** is the name of the architecture file (without extension) in **CHECKTEST** directory and for each architecture you can define many scheduler **setting**. After ':' we must put the list of hostname or group of nodes separated by comma. You can specify in the same hostline different architectures, for example in a heterogenous HPC cluster, simply repeat the line without space between them.
    
    arch#setting:hostname1,hostname2.../arch2:hostname3,hostname4/

It is not necessary to specify a name of setting for each architecture, as in the example above for arch2 **CHECK** loads the *default* setting for that architecture.

If your cluster is not scheduler equipped or you pre allocate the nodes, you can use directly ssh to submit **CHECK** remote commad, adding to command line the flag *--ssh*, in this case the architecture needs only to indentify a pool of nodes where ssh launch a slave command. When you add *--ssh* flag you implicitly use *--master --singleton* flag.



### 4. CHECK OUTPUT

**CHECK** have two type of output, the log and the resultfile. The log can be printed on command line or file and in master mode, each job sumbitted via scheduler report its log in the job output file named *check_nodename*, the job output files are collected in *check_master_collecting_path* set in check_setting.json.

The most important output is the **checkresult file** writed as collection of json objects, the position of this file is set through the parameter *resultfile* in check_setting.json. You can find in the results file two type of json: master_submission or result; i.e. the command below produce 3 json object.

     check --check linpack@x86,stream@x86 --ssh --hpc x86:node1,node2

Master_submission json contains all information regards the submission:

        {
        "master_submission": {
            "hpc": "node1,node2", 
            "arch": "x86#default", 
            "id": "77179d4427964d6da83aa4de9e463b99", 
            "check": "linpack@x86,stream@x86"
        }
        }

The result object contains partial results with measure, unit and the final mark of the node. If **CHECK** is used 
in slave mode the information *slave_mode* is reported and the unique *ID* is the same as the master who submitted. it.

        {
        "RESULT": "OK", 
        "hostname": "node1", 
        "PARTIAL": [
            {
            "linpack": {
                "status": "OK", 
                "arch": "x86", 
                "value": "1036.6957", 
                "unit": "GFLOPS"
            }
            }, 
            {
            "stream": {
                "status": "OK", 
                "arch": "x86", 
                "value": "95483.0", 
                "unit": "MB/s"
            }
            }
        ], 
        "id": "77179d4427964d6da83aa4de9e463b99", 
        "slave_mode": true
        }

        {
        "RESULT": "OK", 
        "hostname": "node2", 
        "PARTIAL": [
            {
            "linpack": {
                "status": "OK", 
                "arch": "x86", 
                "value": "1021.1955", 
                "unit": "GFLOPS"
            }
            }, 
            {
            "stream": {
                "status": "OK", 
                "arch": "x86", 
                "value": "95662.0", 
                "unit": "MB/s"
            }
            }
        ], 
        "id": "77179d4427964d6da83aa4de9e463b99", 
        "slave_mode": true
        }
        
The *check result* file in conclusion is a logbook of all operation done from this instance of **CHECK**. Trough the unique ID number it is possible to date back to and group all operation that **CHECK** done.    

***

## CHECKTEST



### 1. Structure of directory

The CHECKTEST directory must have this structure:

                                 checktest
                                     |
                    ----------------------------------------
                    |                |                      | 
                architecture       test1                  test2
                - map.hpc            |                      |
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
In the example structure reported above we have two **CHECKTEST** written explicity:
  
  - test1/x86/__ init__.py this test is named *"test1"* and is designed to x86 target architecture
  - test2/__ init__.py this test is named *"test2"* and is designed to all architecture.

Into *__init__.py* the name of the python class to import in **CHECK** must have the same name of **CHECKTEST**, so in the previous example test1 or test2.

In **CHECK**, you select what **CHECKTEST** and the target architecture with the symbol **"@"**:
    
    check --check test1@x86

For each architecture file it is allowed have different configurations, so in the **CHECKTEST** directory we can have for arch1 many configurations and it is possible define them through the symbol **"\_"**. In example above for the x512 architecture file we have two different memory configurations x512_mem1,x512_mem2; this means that in master mode on the node describe by x512 **CHECK** launch both x512_mem1,x512_mem2 **CHECKTEST**s; if you want to launch only x512_mem1 test on the nodes you must have an architecture file with the same name.

In the test directory you can define **bin**,**in**,**out** and **tmp** directories and other but for this four cited before **CHECK** automatically generates and saves the path; if one of them is not used you don't need to created.



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

The symbol  **_ noqueue _** indicates that the scheduler has an automatic selection of the queue, while the other information are classical parameters that you write in HPC job file. 



### 3. HPC MAP
A convenience can be to define a group of nodes accumulated by certain properties and this in **CHECK** can be done via file.
In the same directory of architectures there is the file **map.hpc** where node groups can be specified, the file has a very simple format, for each line is specified the name of the group and after the space the list of hostnames separated by comma:

    group1 hostname1,hostname2
    group2 hostname3,hostname4,hostname1,
    group3 hostname1,hostname2,hostname4,hostname5



### 4. Write a CHECKTEST

**CHECK** provides a *template* to simplify the writing of **CHECKTEST** file, to write a compatible test with **CHECK** you must follow these rules:

 0) Import from **CHECK** the template to checktest class:

        from checklib.test.check_test_template import *

 1) Your test must be a python class, named as test directory and son of **CHECK**'s class **checktest** and specifies as global variable *exe* and *version*

        class linpack(checktest):

            """ Linpack class """
            exe = "xlinpack_xeon64"
            __version__ = "0.1.001"

 2) The test class can be have 5 polymorphic methods, if one is missing the corresponding father methods will be called:
   
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

 4) In the *run* method we recommend using the Popen package from Subprocess module to launch the executable; subprocess is directly imported by the father class. To collect stdout, it is recommended to use a code like this:

         
        process = subprocess.Popen( [self.exe,"./input.txt"], shell=False,cwd=self.test_dir["in_dir"],stdout=subprocess.PIPE,env=os.environ)
        self.std_out, self.std_err = process.communicate()

 5) Use the directory structure provided by CHECK. If you put the executable in the **bin** absolute path is generated automatically  given name of exe in *self.exe* variable. Use:
    
    - **bin** to store executable
    - **in** to store input file
    - **out** to store output
    - **tmp** to place temporaney file

 6) Before writing new code, check what is in **checktest** template and if you think your code could be usefull to the others add to the template.

***



## CHECK VERSION rules

- +1.0.0 a major release increment means a big improvement of functionalities of CHECK
- 0.+1.0 a minor release increment means an implementation of features 
- 0.0.+1 a minor minor release increment means a general bugfix

***