# CHECK : Cluster Health and Environment ChecKing system



 Check is a flexible and easy to use software to have a faster snapshot of Performance and Status of HPC Cluster. The software is compososed by two directory/repository, this one **check** that contain the executable and all infrastructure python library and **checktest** that contain the description of architectures and  test recipes. Check can be used via shell,parallel shell and via scheduler, if a parallel shared file system is not installed, CHECK can be distrubute on all cluster node and call from the Master node. A CheckTest is a little python class based on checktest template, so extend the code is very easy, it be enough add a python class in checktest directiory using CHECK plugin policy and at runtime your new test it will be available. The software is callable to command line and through lunch string you can redefine on the fly almost all paramenter conteined in etc conf file.

***

## CHECK

### 0. Environment setup

### 1. Command line



### 2. CHECK etc



### 3. MASTER/SLAVE 


### 4. LOG

***

## CHECKTEST

### 1. Structure of directory

### 2. Architecture

### 3. Write a CHECKTEST

