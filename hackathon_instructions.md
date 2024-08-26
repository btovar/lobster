# Lobster Conda Environment Setup
**Lobster now uses conda, never do cmsenv**

First login to glados, and then run the following commands. 
The general directory structure is: 
```
lobster-python3
    lobster
``` 
If you'd like to use a different setup, just adjust the paths accordingly.
```
unset PYTHONPATH

mkdir lobster-python3
cd lobster-python3

git clone https://github.com/NDCMS/lobster.git
cd lobster
git checkout lobster-python3

conda env create -f lobster_env.yaml
conda activate base
```

**Note:** this yaml creates an environment named `base`, if you'd like to change the name of the environment, edit the first line of lobster_env.yaml before installing


Then, still in the cloned lobster directory, run the following command: 
```
pip install -e .
```

Now that the `base` env is setup, in the future all you need to do is run the following: 
```
unset PYTHONPATH
unset PERL5LIB
conda activate base
```

# Running a Simple Config
In the lobster repository, there is a python script called "simple.py". This has been updated to work with `lobster-python3` and can be run in the following way: 

1. Set up the necessary CMSSW release in the same directory as where you're running the config file (see directions below).
2. unset the pythonpath and start the `base` environment 
3. in the lobster/examples directory, do:  `lobster process simple.py`
4. in the same directory, start a work_queue_factory with the following command: `work_queue_factory -T condor -M "lobster_$USER.*" -dall -o /tmp/${USER}_factory.debug -C factory.json --runos cc7-wq-7.11.1 > /tmp/${USER}_factory.log`

If the process is unable to write to disk and needs a scratch directory add the `-S` or `--scratch-dir` flag with a path to a temp folder.  
The lobster working folder works fine for this, e.g. `/tmpscratch/users/$USER/lobster_test_` + datetime.  

You can monitor the work_queue_factory by doing `work_queue_status` while in your conda environment.
You can monitor the lobster process status by doing `lobster status [lobster working dir path]`. 

After the jobs are completed, check the output. In general, lobster output is stored in `cephfs`. For this simple config, there should be an `output*.root` file stored in `/cms/cephfs/data/store/user/USERNAME/lobster_test_*/ttH` that is roughly 8 MB.

# Setting up a CMSSW environment for the simple example
For the simple.py script, we're using CMSSW_10_6_26. There are two options: 
1. install CMSSW_10_6_26 inside the same directory where simple.py is located 
    - `lobster/examples/`
    - inside the examples directory run `unset PERL5LIB` and `cmsrel CMSSW_10_6_26` (NOTE: this has to be done outside of lobster conda environment)
    - reminder: DO NO do cmsenv
2. install CMSSW_10_6_26 somewhere else, and edit the path in simple.py on line 45: `release='<your-path-to-CMSSW_10_6_26>'`

# Possible Errors
After submitting a lobster process and starting a work_queue_factory, if there are no errors in `process.err` or `process_debug.log` but workers are never assigned to the job, try the follwing: 
- Kill the current work_queue_factory. 
- Restart the work_queue_factory using the absolute path of work_queue: `nohup /afs/crc.nd.edu/group/ccl/software/x86_64/redhat9/cctools/stable/bin/work_queue_factory -T condor -M "lobster_$USER.*" -dall -o /tmp/${USER}_factory.debug -C factory.json --runos cc7-wq-7.11.1 > /tmp/${USER}_factory.log &`

If that does not result in workers being spawned, you can try running a worker directly with the following command, where path_to_your_conda_env  
is the base path where all the conda packages for your environment are installed, e.g. `$HOME/miniconda3/envs/base`:
- `apptainer exec --bind /cvmfs:/cvmfs --bind <path_to_your_conda_env>:/cctools /afs/crc.nd.edu/group/ccl/software/runos/images/cc7-wq-7.11.1.img /cctools/bin/work_queue_worker -M "lobster_$USER.*" -dall --cores 1 --disk 10000 -t 150`
