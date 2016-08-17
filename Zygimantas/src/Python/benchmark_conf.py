"""
Configuration file for benchmark.py script.
"""


from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

atribute_drop_list = (
    'tr_id', 't_error_code', 'tr_timestamp_complete', 'timestamp_tr_st',
    'block_size', 'buf_size', 'channel_type',
    'dst_site_name', 'src_site_name', 't_timeout',
    'src_srm_v', 'tcp_buf_size', 'file_metadata|name',
    'file_metadata|dst_type', 'file_metadata|request_id', 'file_metadata|src_type',
    'file_metadata|md5', 'file_metadata|src_rse',
    'file_metadata|dst_rse', 'file_metadata|activity',
    'file_metadata|scope', 'file_metadata|dest_rse_id'
)
# atribute_drop_list=[]


model_train_parameter = [
    # {'subsample':0.7 , 'learning_rate':0.05,'n_estimators': 1},
    # {'subsample':0.7 , 'learning_rate':0.05,'n_estimators': 10},
    {'n_estimators': 50},
    {'n_estimators': 100},
    {'n_estimators': 200},
    # {'subsample':0.7 , 'learning_rate':0.05,'n_estimators': 500},
    # {'subsample':0.7 , 'learning_rate':0.05,'n_estimators': 1000},
    # {'subsample':0.7 , 'learning_rate':0.05,'n_estimators': 1,'objective':'reg:logistic'},
    # {'subsample':0.7 , 'learning_rate':0.05,'n_estimators': 10,'objective':'reg:logistic'},
    # {'subsample':0.7 , 'learning_rate':0.05,'n_estimators': 50,'objective':'reg:logistic'},
    # {'subsample':0.7 , 'learning_rate':0.05,'n_estimators': 100,'objective':'reg:logistic'},
    # {'subsample':0.9 , 'learning_rate':0.1,'n_estimators': 200,'objective':'reg:logistic'},
    # {'subsample':0.85 , 'learning_rate':0.1,'n_estimators': 200,'objective':'reg:logistic'},
    # {'subsample':0.85 , 'learning_rate':0.15,'n_estimators': 200,'objective':'reg:logistic'},
    # {'subsample':0.9 , 'learning_rate':0.1,'n_estimators': 200,'objective':'reg:logistic'},
    # {'subsample':0.9 , 'learning_rate':0.15,'n_estimators': 200,'objective':'reg:logistic'},
    # # {'subsample':0.9 , 'learning_rate':0.1,'n_estimators': 200,'objective':'reg:logistic'},
    # # {'subsample':0.9 , 'learning_rate':0.15,'n_estimators': 200,'objective':'reg:logistic'},
    # {'subsample':0.95 , 'learning_rate':0.15,'n_estimators': 200,'objective':'reg:logistic'},
    # {'subsample':0.95 , 'learning_rate':0.2,'n_estimators': 200,'objective':'reg:logistic'},
    # {'subsample':1 , 'learning_rate':0.15,'n_estimators': 200,'objective':'reg:logistic'},
    # {'subsample':1 , 'learning_rate':0.2,'n_estimators': 200,'objective':'reg:logistic'},
    # {'subsample':0.7 , 'learning_rate':0.05,'n_estimators': 500,'objective':'reg:logistic'},
    # {'subsample':0.9 , 'learning_rate':0.1,'n_estimators': 1000,'objective':'reg:logistic'},
]


# model_train_parameter =[
#     {'n_estimators': 1},
#     {'n_estimators': 10}
# ]


model_func_l = [
    ('GradientBoostingRegressor', GradientBoostingRegressor),
    ('RandomForestRegressor', RandomForestRegressor),
    # ('XGBRegressor', XGBRegressor)
]
