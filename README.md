CHECK: Cluster Health and Environment ChecKing system
=========


Check is a flexible and easy to use software for proving the performance and health of an HPC Cluster. The software consists of two directories/repositories: **CHECK** contains the executable and the python library infrastructure, and **CHECKTEST** includes the test and benchmark recipes and the description of the cluster. **CHECK** can be used via shell, parallel shell and scheduler; if a parallel file system is not present, **CHECK** can be distributed on all cluster nodes and is callable from the Master node. A **CHECKTEST** is a little python class based on *check_test_template*, so extending the code is very easy: you just add a python class in the **CHECKTEST** directory using **CHECKTEST** policy, and at runtime, your new test will be available. The software is callable from the command line, and through a launch string, it is possible to redefine on the fly almost all parameters contained in the configuration file. CHECK also has a report function that allows the examination of analysis results.

***

CHECK 0.3
------------------------------------------------

## 0. *Environment setup and configuration*

**CHECK** does not require a formal installation. You can download wherever you want from the repository and use the *source command* to load the environment from setup_check.sh, before first use configures the application using  **CHECK** etc file.

    $ git clone https://github.com/EricPascolo/CHECK.git  check

You find setup file in **check/bin** :

    $ source check/bin/setup_check.sh

After the environment has loaded, you find the **CHECK** command in your $PATH and the check directory path is set to $CHECK_HOME; 
**CHECK** setup also adds the CHECK_HOME path to PYTHONPATH, so attention please when you use CHECK with other modules or python packages.

### 0.1 *CHECK etc*

In **check/etc/** directory, you can set up your configuration file written in JSON format and named `check_setting.json`. The configuration file in etc overwrites the default configuration file in **check/etc/default/**; if a parameter is not found in the first, it will be read in the second. 
The structure of the file is as follows:

    {
    "loglevel":"DEBUG",
    "logfile":"$HOME/checklog.txt",
    "resultfile":"$HOME/checkresult.txt",
    "logtype":"cl",
    "checktest_directory":"$HOME/checktest/",
    "check_remote_source_path":"$CHECK_IM_REMOTE",
    "check_master_collecting_path":"$HOME/check_master_collection",
    "module_env_py_interface":"$MODULESHOME/init/python.py",
    "cluster_scheduler":" "
    }

In the configuration file, you can use environment variables because CHECK can resolve them. 

The `loglevel` parameter can have 3 values in descending order of verbosity:

 - DEBUG
 - INFO 
 - CRITICAL

**CHECK** run results and errors are written as CRITICAL level, partial results and other configuration information are written as INFO and developer information are written as DEBUG level.
The `logtype` field allows you to choose where the log is printed:

 - cl : print log on terminal
 - file : print log on file
 - both : print log on terminal and file

If you choose *file* or *both*, you can specify the log file path in field `logfile`.

The file of results set by `resultfile` field; contains the database of CHECK; here will be written all submission and result operations. The results data is explorable via `report` flag.

`checktest_directory` define the path of the directory of **CHECKTEST**.

`check_remote_source_path` is the path in the remote node where **CHECK** directory is located; this path is necessary to use the software without a parallel filesystem.

`check_master_collecting_path` is the path on the master node, where the job scheduler output file is stored.

`module_env_py_interface` is the path where is located the interface to Cluster Module Environment, is necessary to load modules, such as MPI, during a **CHECKTEST** run. 

`cluster_scheduler` is the name of the scheduler installed on the cluster, **CHECK** currently provides an interface to Slurm, PBS.




## 1. *Command line interface*

### 1.1 Basic command

**CHECK** is callable from the command line(CL):

    **** CHECK 0.2.2 - r64s08u38 - 17/03/2020 09:26:30 - 21fce0631c554459b526c2f25bf8791b
    21fce0631c554459b526c2f25bf8791b 09:26 [INFO] (checkloggin) : logger: check_file_stream_log type:cl
    21fce0631c554459b526c2f25bf8791b 09:26 [DEBUG] (__init__) : check_file_stream_log
    21fce0631c554459b526c2f25bf8791b 09:26 [CRITICAL] (__init__) : Checktest list is empty
    **** CHECK STOP - r64s08u38 - 17/03/2020 09:26:30 - 21fce0631c554459b526c2f25bf8791b

Each run of **CHECK** is identified with a unique **ID** number reported in each line of output. The first and last line reports: the version, the hostname, the time and the run **ID**.

To see all CL flags use `--help` flag:

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
    --logtype {cl,file,both}
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



The **CHECKTEST**s to run are set by  `--check` flag:

    check --check linpack@x86

This command will be launched the linpack benchmark with the setting of x86 architecture defined in the HPC directory.

To see which **CHECKTEST** are installed and on which architectures, use the flag `-checklist`:

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
  
To see **CHECK** parameters on runtime, use the flags `--checkparameter`:

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

Some **CHECKTEST** needs an installation before the first use. To finalize it, specify the **CHECKTEST** and adding the flag `--install`:

    check --check linpack@x86 --install

### 1.2 Mark and Analisys

For each **CHECKTEST**, **CHECK** assigns a **mark** to the node or the nodes pools among OK, DOWN, WARNING. The whole node/pool result is the combination of the single results from all benchmark launched on the node/pool. Currently, in **CHECK** only default analisys is implemented, and follow this schema:
	

|MARK         | DESCRIPTION                              |
|-------------|------------------------------------------|
|FAIL         | one or more tests have not been executed |
|DOWN         | one or more tests have returned DOWN     |
|DEEP WARNING | all test return WARNING                  |
|WARNING      | one or more tests have returned WARNING  |
|OK           | all test return OK                       |

You can add a personalized analysis in the **CHECK** and select with `--analysis` flag: 

     check --check linpack@x86,stream@x86 --analysis simple

### 1.3 Master/Slave submission

The flags `--master` / `--ssh` and `--hpc` are used to launch tests, via the scheduler/ssh, on the HPC cluster node from login or master node. Through `--master` flag you enable master/slave mode (via scheduler as default) and with `--hpc` you specify the architecture and cluster nodes where **CHECK** launches the tests:

    check --check linpack@x86,linpack@knl --master --hpc x86:node1,node2/knl:groupnode1/

You can also use predefined groups of nodes, like "groupnode1" in the string above. These groups of nodes are defined in the file `map.hpc` in *hpc* directory in  **CHECKTEST**. When you specify more than one node, the default behavior is to launch a unique job on the all nodes selected with the same architecture; but with the flag `--singleton` **CHECK** launches one job for each node selected in hpc flag (including those defined by a group):

    check --check linpack@x86,linpack@knl --master --hpc x86:node1,node2/knl:groupnode1/ --singleton

The *--ssh* flag, allows the submission of the remote command via ssh following the same rules above. In this case, the singleton flag is implicit.

**CHECK** allow to launch a job  a random set of nodes selected by the scheduler and this can be done by entering a `<job object>` in the nodes list:

    check --check linpack@x86 --master --hpc x86#gpu:node2,'<"nnodes"=4;"queue"="system";"ncpus"=10>',node3

In this case, the basic parameters of the *x86* architecture with the *gpu* setting will be overwritten and a job will be launched without specifying the nodes list by hostname. In a **\<job object>** all the parameters defined in the architecture can be overridden, only *hostlist* will be ignored. 

### 1.4 Etc on the fly

**CHECK** provides a very flexible environment. Indeed you can also define at runtime the all **CHECKTEST** parameters overwriting the configuration loaded from the configuration file. Some parameter have specific flag to set on CL, the other is overwriting by a configuration json file.

To change the **CHECKTEST** directory use `--checktest_directory` flag:

 check --check my_linpack@x86 --checktest_directory $HOME/my_personal_checktest

To change log level and logfile use `--loglevel`and `--logfile`:

 check --check linpack@x86 --loglevel INFO --logfile $HOME/log.check

The `--configuration` flag takes a configuration file as input, this file must be written in JSON format and is an easy way to avoid writing long **CHECK** command lines:

 check --configuration myconffile.json

In **CHECK**,  the parameter is organized by a hierarchical structure. If the parameter is not found, it is searched in the next setting layer:
        
| SETTING HIERARCHICAL ORDER   |
|:----------------------------:|
|Command line                  |
|Config file by `--config`     |
|Config file in /etc           | 
|Config file in /etc/default   |


## 2. *MASTER mode and Architectures*

**CHECK** can use a scheduler or ssh to submit the **CHECKTEST** directly on cluster nodes. At the moment **CHECK** created a job containing an instance of **CHECK** in *slave* mode and submit to the scheduler or launch an ssh command. 
The **ID** of the slave instance is the same as the master instance. 

CHECK is designed to run on the system without a parallel FS mounted. The position of the slave instance must be specified in the setting file via `check_remote_source_path` parameter. If the parallel FS is mounted,  the same installation of **CHECK** is usable both as master and slave, set the configuration parameter as $CHECK_IM_REMOTE.

The cluster nodes to run **CHECK** in slave mode is  passed  by `--hpc` flag with the following  structure :

    architecture#setting:hostname1,GroupOfNodes1.../

The **architecture** is the name of the architecture file (without extension) in **CHECKTEST**/hpc directory and for each architecture, it is possible to define many scheduler **settings** in the same JSON file. After ':'  the list of hostname or group of nodes separated by comma indicates the slave nodes. If the **setting** is not declared, the default is loaded. To specify in the same hostline different architectures,  simply repeat the line without space between them.
 
    arch#setting:hostname1,hostname2.../arch2:hostname3,hostname4/

If your cluster is not scheduler equipped or have pre-allocated the nodes, submit **CHECK** remote command use ssh, adding to command line the flag `--ssh`, in this case the architecture needs only to identify a pool of nodes where ssh launch a slave command.  Add *--ssh* flag implies use *--master --singleton* flag.




## 3. CHECK OUTPUT

To print the result on **CHECKTEST**, operation and activity of **CHECK** use `--report` flag. The results are searchable by:

- Id
    - `--report id:id` - return all results with specific ID and, in case of master_submission, the list of node without result
    - `--report id:id#hostname`  return one specific result of hostname selected by ID
- Node
    - `--report node:hostname`  return all checktests and results selected by hostname
    - `--report node:hostname#checktest` - return a specific (linpack or Stream, ..) checktest and results selected by hostname
- Checktest name 
    - `--report checktest:checktest` - return all partial of a specific checktest (id,hostname,checktest - (linpack or Stream, ..))
    - `--report checktest:checktest#id` - return all partial of a specific checktest (linpack or Stream, ..) selected by id(hostname,checktest)
- Master 
    - `--report master:n` print last n master_submission, if n=0 print all master submission, the default value is 1


### 3.1 OUTPUT FILES

**CHECK** have two types of output, the log and the resultfile. The log can be printed on the command line or file and in master mode, each job submitted via scheduler report its log in the job output file named *check_nodename*. In addition, the job results and submission operation are collected in *check_master_collecting_path* set in check_setting.json.

The most important output is the **checkresult file**, which is the database of CHECK operation write as a collection of JSON objects. This file's position is set through the parameter *resultfile* in check_setting.json. This file s explorable with `--report` flag described above. 
In the **checkresult file**, two types of JSON are defined: master_submission or result; i.e. the command below produces 3 JSON objects.

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

The result object contains partial results with measure, unit and the final mark of the node. If **CHECK** is used in slave mode, the information *slave_mode* is reported, and the unique *ID* is the same as the master who submitted it.

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
        
The JSON above, to increase readability have been exploded over several lines, but in the file each line contains a complete JSON. It is not recommended to edit this file by hand. Trough the unique ID number, it is possible to date back to and group all operations that **CHECK** done. 

***

CHECKTEST
------------------------------------------------


## 1. Structure of directory

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

Into `__init__.py` the name of the python class to import in **CHECK** must have the same name of **CHECKTEST**, so in the previous example test1 or test2.

In **CHECK**, you select what **CHECKTEST** and the target architecture with the symbol `"@"`:
    
    check --check test1@x86

For each architecture file it is allowed have different configurations, so in the **CHECKTEST** directory we can have for arch1 many configurations and it is possible define them through the symbol `"\_"`. In example above for the x512 architecture file we have two different memory configurations x512_mem1,x512_mem2; this means that in master mode on the node describe by x512 **CHECK** launch both x512_mem1,x512_mem2 **CHECKTEST**s; if you want to launch only x512_mem1 test on the nodes you must have an architecture file with the same name.

In the test directory you can define **bin**,**in**,**out** and **tmp** directories and other but for this four cited before **CHECK** automatically generates and saves the path; if one of them is not used you don't need to created.



## 2. Architecture
**CHECK** needs to find the architecture files when it is run in master mode to know the specs of the cluster nodes. The name of file in **architecture** directory must be equal to the name of the **CHECKTEST**s architecture. 

An architecture file is write in *json* format and contains a json object for each **setting**, a setting is a subset of the parameters for each architeture and in all architerture files must have a setting named *default*. 

Below an architecture file example:

    {
    "default":{

        "nnodes":"1",
        "ncpus":"36",
        "memory":"118GB",
        "walltime":"00:15:00",
        "queue":"__noqueue__",
        "account":"my_account"

    },

    "debug":{
        
        "nnodes":"1",
        "ncpus":"36",
        "memory":"118GB",
        "walltime":"00:15:00",
        "queue":"debug",
        "account":"my_account"
    
        }

    }

The symbol  `_ noqueue _` indicates that the scheduler has an automatic selection of the queue, while the other information are classical parameters that you write in HPC job file. 

### 3. HPC MAP
A convenience can be to define a group of nodes accumulated by certain properties and this in **CHECK** can be done via file.
In the same directory of architectures there is the file **map.hpc** where node groups can be specified, the file has a very simple format, for each line is specified the name of the group and after the space the list of hostnames separated by comma:

    group1 hostname1,hostname2
    group2 hostname3,hostname4,hostname1,
    group3 hostname1,hostname2,hostname4,hostname5



## 4. Write a CHECKTEST

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



 CHECK VERSION rules
--------------------------
- +1.0.0 a major release increment means a big improvement of functionalities of CHECK
- 0.+1.0 a minor release increment means an implementation of features 
- 0.0.+1 a minor minor release increment means a general bugfix

***