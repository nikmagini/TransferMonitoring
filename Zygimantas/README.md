# Intro

This project represents my contribution to the *Transfer metrics analytics* project as a CERN Summer Student 2016. Here you will find:
- src/Python:
    + jsonUtilities.py - scripts to prepare custom .txt file with JSON objects to ML suitable format (.CSV file with hashed values).
    + benchmark.py | benchmark_conf.py - script to used to benchmark different algorithms with different parameters.
    + checPredictions.py - scritp to compare  predictions in _pred.txt_ file generated using tools from DCAFPilot package with .csv while on which predictions were made. *Obsolete*, and regression testing is preferred using benchmark.py .   
    + csvSplit.py - helper scrit to split .csv file to test|train. 
- Analysis: this contains *jupyter notebooks* used to learn scikit-learn and other packages. It also used to analyze data, run some ML algorithms with different parameters, make correlation matrix. Be my guess and have a look.
- Report: report of weekly work, some are non-essential, however, in *week8.md* I documented how I ran classification on data and what was the result.
- Report/snipets: contains peace of code and commands that I found useful for the project.
- data: input data used for testing scripts.

# Learning material

Good learning material I found about scikit-learn:
- https://www.youtube.com/watch?v=L7R4HUQ-eQ0
- https://github.com/jakevdp/sklearn_pycon2015
DCAFPilot tutorial (you should download and run locally):
- https://github.com/dmwm/DMWMAnalytics/blob/master/Popularity/DCAFPilot/doc/talks/Pilot1/index.html 

# Setup
 
## Project requirements

- Project targets Linux platform. That means if there is unusual error, run 'file [text]' command and check if its not DOS type document (ending with CRLF char). For example, python CSV library by default write files with CRLF char. 
- The project uses Python 2.7.
- Python dependencies: just look through all *import* statement in code.
- DCAFPilot: ML tool set. More about it on https://github.com/dmwm/DMWMAnalytics/tree/master/Popularity/DCAFPilot
- Jupyter-notebook: I used tutorial from  https://github.com/jakevdp/sklearn_pycon2015
- XGBoost: http://xgboost.readthedocs.io/en/latest/get_started/index.html


## Openstack VM setup
These are instructions to setup VM with DCAFPilot, however, you should ask for update. Also, before installing anything on VM, you should setup certificates(instructions after the letter)

```
Here is information you need:

https://cms-http-group.web.cern.ch/cms-http-group/tutorials/environ/vm-setup.html

if you'll not able to access this web page (it may require CMS authentication)
I put the same instructions over here:

https://www.dropbox.com/s/icqw8en2b5dxmg1/CMS_VM_setup.pdf?dl=0

You don't need step #3, #6

and for step #7 you need to use the following line

(VER=HG1603b REPO="comp.valya" A=/data/cfg/admin; ARCH=slc6_amd64_gcc493; cd
/data; $A/InstallDev -A $ARCH -R comp@$VER -s image -v $VER -r comp=$REPO -p
"admin frontend backend mongodb DCAFPilot")

This step will install all necessary software you need. Please check that
you have this package:

/data/srv/HG1603b/sw.valya/slc6_amd64_gcc493/cms/DCAFPilot/

and the version should be 0.1.24, if it is not this version do the following:
- modify /data/cfg/dcafpilot/deploy
and modify this line

  deploy_pkg comp cms+DCAFPilot

to this one:

  deploy_pkg comp cms+DCAFPilot 0.1.24

and perform step #7 again, i.e. run again

(VER=HG1603b REPO="comp.valya" A=/data/cfg/admin; ARCH=slc6_amd64_gcc493; cd
/data; $A/InstallDev -A $ARCH -R comp@$VER -s image -v $VER -r comp=$REPO -p
"admin frontend backend mongodb DCAFPilot")

Then you should have version 0.1.24 installed for you.

Now, to run/use DCAFPilot package you just need to source proper environment in your VM
like that:

source /data/srv/current/apps/DCAFPilot/etc/profile.d/init.sh

This will setup PYTHONPATH and all DCAF tools will be available for you, i.e.
model, merge_csv, transform_csv, etc.

Every tool has --help option, run it with it to get started.
```

Follow this tutorial to setup certificates. Without them you will get errors:
https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookStartingGrid#ObtainingCert


For all 3rd party libraries like *memory_profiler* that I use for the project, they should be installed with *pip2.7*, so install it first.

# Data location
Follow top level README.md about that.

# Current project situation
At the moment script to transform data to ML suitable format is made. Also some ML algorithms were run on prepared data and compared. However, before continuing further work, attributes used for ML should be re-checked, because something is missing.

## Right attributes for machine learning

Attributes that are currently dropped:  

```python
# columns that are output and cant be used with ML
# so should be dropped out
drop_fields = ['timestamp_tr_comp',
               'timestamp_chk_src_ended',
               'timestamp_checksum_dest_ended',
               'timestamp_checksum_dest_ended',
               'tr_error_scope',
               't_failure_phase',
               'tr_error_category',
               't_final_transfer_state',
               'tr_bt_transfered',
               'time_srm_prep_end',
               'time_srm_fin_end',
               't__error_message',
               'tr_timestamp_complete'
               't_error_code'
               ]
# fields that correlating and useless        
drop_list_correlating =['file_metadata|name','file_metadata|dst_type',
                        'file_metadata|request_id','file_metadata|src_type',
                        'file_metadata|md5','file_metadata|src_rse',
                        'file_metadata|dst_rse','file_metadata|activity',
                        'file_metadata|scope','file_metadata|dest_rse']

```

It would be good idea to again inspect attributes that would be *outputs* in ML terms. Also, drop all all attributes that  have (anti)correlation value above 0.8. The following letter would give more insight about attributes:

```
The transfer workflow in FTS is : START -> PREPARATION+SOURCE CHECKSUM
(optional) -> COPY -> FINALIZATION -> DESTINATION CHECKSUM (optional) -> END

So these are all the timestamps for the events in a transfer, in the
expected time ordering.

I put comments after each time stamp


"tr_timestamp_start" - time when FTS starts the transfer workflow -
should be NOT NULL for all transfers, OK and failed

"time_srm_prep_st" - time when FTS starts the preparation of the file -
should be NOT NULL for all transfers, OK and failed

"timestamp_chk_src_st" - time when FTS starts the checksumming of the
source file - can be NULL or NOT NULL for any transfer (checksum is not
mandatory)

"timestamp_chk_src_ended" - time when FTS completes the checksumming of
the source file - can be NULL or NOT NULL for any transfer (checksum is
not mandatory)

"time_srm_prep_end" - time when FTS completes the preparation of the
file - should be NOT NULL for all transfers, OK and failed.

"timestamp_tr_st" - time when FTS starts the actual copy - should be NOT
NULL for all OK transfers. Should be NULL for transfers failed in the
preparation step. Should be NOT NULL for transfers failed in a later step.

"timestamp_tr_comp" - time when FTS completes the actual copy - should
be NOT NULL for all OK transfers. Should be NULL for transfers failed in
the preparation step. Should be NOT NULL for transfers failed in a later
step.

"time_srm_fin_st - time when FTS starts the finalization of the file -
should be NOT NULL for all OK transfers. Should be NULL for transfers
failed in the preparation step. Should be NOT NULL for transfers failed
in a later step.

"time_srm_fin_end" - time when FTS completes the finalization of the
file - should be NOT NULL for all OK transfers. Should be NULL for
transfers failed in the preparation step. Should be NOT NULL for
transfers failed in a later step.

"timestamp_checksum_dest_st" - time when FTS starts the checksum of the
destination file - should be NULL for transfers failed in the
preparation step. Can be NULL or NOT NULL for other transfers (checksum
is not mandatory)

"timestamp_checksum_dest_ended" - time when FTS completes the checksum
of the destination file - should be NULL for transfers failed in the
preparation step. Can be NULL or NOT NULL for other transfers (checksum
is not mandatory)

"tr_timestamp_complete" - time when FTS completes the transfer workflow
- should be NOT NULL for all transfers, OK and failed


As you can see, only the following timestamps don't depend on the
transfer success/failure: "tr_timestamp_start", "time_srm_prep_st",
"timestamp_chk_src_st", "timestamp_chk_src_ended",  "time_srm_prep_end",
"tr_timestamp_complete"

The other timestamps are partially correlated to transfer failure (they
will be NULL in case of failure in the preparation phase).
```   

