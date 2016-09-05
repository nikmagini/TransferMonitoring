# week 8
 
- Made presentation and report about project.
- *train_csv* utility from DCAFPilot doesnt like files with DOS like file endings (CRLF). 
- runned RandomForestClassifier on datasets.

# Error rate predictions 

## Step I took to run RandomForestClassifier
```bash 
# convert to CSV file
jsonUtilities.py -i xaa --ohfile train.csv

# preproces for machine learning using tools from DCAF package
transform_csv --fin=train.csv --target=timestamp_tr_dlt --target-thr=0 --fout=train_trans.csv 
transform_csv --fin=te

# train model and lets see predictions in train_trans.csv 
model --scorer=accuracy,precision,tpr,fpr,tnr,fnr --learner=RandomForestClassifier --train-file=train_trans.csv --target=target 

```

## results 
```
Feature ranking:
1. importance 0.362157, feature timestamp_tr_st
2. importance 0.194525, feature time_srm_fin_st
3. importance 0.126606, feature file_metadata|previous_attempt_id
4. importance 0.086381, feature timestamp_checksum_dest_st
5. importance 0.049907, feature file_metadata|filesize
6. importance 0.047545, feature t_error_code
7. importance 0.019818, feature t_timeout
8. importance 0.019171, feature file_metadata|dst_rse
9. importance 0.015477, feature dst_hostname
Score metric (accuracy_score): 0.999993412385
Score metric (precision_score): 1.0
Score metric (TPR): 0.99999242843
Score metric (FPR): 0.0
Score metric (TNR): 1.0
Score metric (FNR): 7.57157026796e-06

Atribute names:
block_size,buf_size,channel_type,chk_timeout,dest_srm_v,dst_hostname,dst_site_name,dst_url,endpnt,f_size,file_metadata,file_metadata|activity,file_metadata|adler32,
file_metadata|dest_rse_id,file_metadata|dst_rse,file_metadata|dst_type,file_metadata|filesize,file_metadata|md5,file_metadata|name,file_metadata|previous_attempt_id,
file_metadata|request_id,file_metadata|scope,file_metadata|src_rse,file_metadata|src_type,job_m_replica,job_metadata,job_metadata|issuer,job_metadata|multi_sources,
job_state,nstreams,retry,retry_max,src_hostname,src_site_name,src_srm_v,src_url,srm_space_token_dst,srm_space_token_src,t_channel,t_error_code,
t_timeout,tcp_buf_size,time_srm_fin_st,time_srm_prep_st,timestamp_checksum_dest_st,timestamp_chk_src_st,tr_timestamp_complete,tr_timestamp_start,
user_dn,vo,tr_id,timestamp_tr_st,target
```
It looks like 'timestamp_tr_st' and 'time_srm_fin_st' acounts for about 55% of the given away information saying if transfer failled or not. 

After dropping 'timestamp_tr_st' and 'time_srm_fin_st':
```
Feature ranking:
1. importance 0.229655, feature job_state
2. importance 0.201687, feature file_metadata|previous_attempt_id
3. importance 0.087222, feature timestamp_checksum_dest_st
4. importance 0.061385, feature t_timeout
5. importance 0.040316, feature job_metadata|issuer
6. importance 0.035348, feature chk_timeout
7. importance 0.035257, feature dst_hostname
8. importance 0.032307, feature f_size
9. importance 0.026518, feature t_error_code
Score metric (accuracy_score): 0.996452566514
Score metric (precision_score): 0.997538845226
Score metric (TPR): 0.998128416871
Score metric (FPR): 0.0111037086387
Score metric (TNR): 0.988896291361
Score metric (FNR): 0.00187158312948
```

I continued dropping fields until scores started droping:
```
[zmatonis@transmon5 TransMonData]$ model --scorer=accuracy,precision,tpr,fpr,tnr,fnr --learner=RandomForestClassifier --train-file=test_trans.csv --target=target --drops='timestamp_tr_st,time_srm_fin_st,file_metadata|previous_attempt_id,timestamp_checksum_dest_st,file_metadata|src_rse,dst_hostname,file_metadata|dst_rse,t_error_code,file_metadata|activity,t_timeout,time_srm_prep_st,file_metadata|dest_rse_id,job_m_replica,job_metadata|multi_sources,file_metadata|filesize,file_metadata|scope,f_size,t_channel,srm_space_token_dst,nstreams'
RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=None, max_features='auto', max_leaf_nodes=None,
            min_samples_leaf=1, min_samples_split=2,
            min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,
            oob_score=False, random_state=123, verbose=0, warm_start=False)
Split level: train 67.0%, validation 33.0%
Feature ranking:
1. importance 0.154420, feature src_hostname
2. importance 0.084637, feature tr_id
3. importance 0.083480, feature src_url
4. importance 0.081545, feature dst_url
5. importance 0.079678, feature file_metadata|request_id
6. importance 0.079150, feature file_metadata|name
7. importance 0.074268, feature timestamp_chk_src_st
8. importance 0.073631, feature user_dn
9. importance 0.073232, feature file_metadata|adler32
Score metric (accuracy_score): 0.876766272875
Score metric (precision_score): 0.911939492166
Score metric (TPR): 0.942490228922
Score metric (FPR): 0.443537414966
Score metric (TNR): 0.556462585034
Score metric (FNR): 0.0575097710776
```

It should be again inspected which atributes should be dropped. Nicolo wrote a brief instruction which atributes will be null if transfare fails. Documentation for atributes that would be output in ML terms also should be checked (ex _t_error_code_). Also corelation matrix should be done and atributes that (anti)corelates >80%  should be dropped. However, clasification aproach gives a good ideas which atributes "tells to much".