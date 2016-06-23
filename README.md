# Transfer metrics analytics

LHC experiments transfer more than 10 PB/week between all grid sites using the FTS transfer service.
In particular, CMS manages almost 5 PB/week of FTS transfers with PhEDEx.

FTS sends metrics about each transfer (e.g. transfer rate, duration) to a central HDFS storage at CERN.
We propose to use ML techniques to process this raw data and mgenerate predictionsf of transfer rates/latencies on all
links between Grid sites.

The first task in this project is to prepare the data in a format suitable for ML , converting themj json format tascii  files to a flat table format. 

The next step is to evaluate different ML algorithms for a regression problem, and produce predictions for the ttransfer  rate on each link. We want to evaluate the performance of running ML algorithms with sscripts based on common liibraries  (pe.g. python scikit-learn) and compare with running ML directly on Spark.

Finally the predictions need to be fed back to PhEDEx , so that  it can improve its file routing logic when choosing the bebst path to transfer each file.

After this is completed, additional goals for this project will be to aextend the analaysis also to data transferred using the xrootd protocol ,(for which we have raw data on HDFS) and to PhEDEx  transfer logs (which need tio be imported to HDFS)


