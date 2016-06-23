# Transfer metrics analytics

LHC experiments transfer more than 10 PB/week between all grid sites using the FTS transfer service.
In particular, CMS manages almost 5 PB/week of FTS transfers with PhEDEx.

FTS sends metrics about each transfer (e.g. transfer rate, duration) to a central HDFS storage at CERN.
We propose to use ML techniques to process this raw data and generate predictions of transfer rates/latencies on all
links between Grid sites.

The first task in this project is to prepare the data in a format suitable for ML, converting them json format ascii files to a flat table format. Process from unstructured to numerical representation needs to be done. 

The next step is to evaluate different ML algorithms for a regression problem, and produce predictions for the transfer rate on each link. We want to evaluate the performance of running ML algorithms with scripts based on common libraries (e.g. python scikit-learn) and compare with running ML directly on the Hadoop cluster with Spark.

Finally the predictions need to be fed back to PhEDEx  routing,  so that it can use a better estimate of transfer rates/latencies when choosing the best path to transfer each file.

After this is completed, additional goals for this project will be to extend the regression study also to data transferred using the xrootd protocol (for which we have raw data on HDFS) and to PhEDEx  transfer logs (which need to be imported into HDFS)

Tools to review:
  python language
  ML libraries
  HDFS, spark
