# week 7
- After closer look to sample data I realised there is no point predicting if transfer fails (-1). Usually, if there was a transfer error, 'timestamp_tr_st' is lacking values as well making it easy for ML to predict if there will be a transfer error.   
- Tested XGBRegressor and GradientBoostingRegressor.
- Made a script to benchmark how much time and RAM takes to try specific ML algoritm with specific settings.