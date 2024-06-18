import os
import argparse
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from darts import TimeSeries
    from darts.metrics import mape
    from darts.models import CatBoostModel
import optuna
from functools import partial
import random

SEED = 42
FORECAST_LEN = 4 # forecast horizon

import logging
optuna.logging.set_verbosity(optuna.logging.WARNING)

class LoggingCallback:
    def __init__(self, interval=1):
        self.interval = interval

    def __call__(self, study, trial):
        if trial.number % self.interval == 0:
            print(f"Trial number: {trial.number}, Trial value: {trial.value:.2f}, Trial params: {trial.params}", end='\n\n')
            print(f"Best trial: {study.best_trial.number}, Best value: {study.best_value:.2f}, Best params: {study.best_trial.params}", end='\n\n')

def set_seed(seed: int = SEED):
    """Set random seed for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)

def build_and_train_model(model_settings,
                          backtest_settings,
                          ts,
                          past_cov,
                          forecast_len=FORECAST_LEN):
    model = CatBoostModel(
        **model_settings,
        output_chunk_length=forecast_len,
        eval_metric = "MAPE",
        early_stopping_rounds = 15,
        task_type = "CPU",
        thread_count = 4,
        random_state=SEED
    )

    shift = max(model.model_params["lags"], model.model_params["lags_past_covariates"])
    
    if backtest_settings["rolling_window"]==True:
        ts_train = ts[-(backtest_settings["window_size"] + forecast_len) : -forecast_len]
        ts_valid = ts[-(forecast_len + shift) : ]
        past_cov_train = past_cov[-(backtest_settings["window_size"] + forecast_len) : -forecast_len]
        past_cov_valid = past_cov[-(forecast_len + shift) : ]
    else:
        ts_train = ts[ : -forecast_len]
        ts_valid = ts[-(forecast_len + shift) : ]
        past_cov_train = past_cov[ : -forecast_len]
        past_cov_valid = past_cov[-(forecast_len + shift) : ]
        
    model.fit(series=ts_train,
              past_covariates=past_cov_train,
              val_series=ts_valid,
              val_past_covariates=past_cov_valid,
              verbose=False
             )
    return model

def manual_backtest(model_settings,
                    ts,
                    past_covariates,
                    forecast_horizont=FORECAST_LEN, 
                    start_test=160,
                    step = 30,
                    save_curves=False,
                    rolling_window=False,
                    window_size=None,
                    verbose=True
                   ):
    '''
    Функция аналогична встроенной функции backtest
    '''
    shift = max(model_settings["lags"], model_settings["lags_past_covariates"])
    metrics = list() # Список для метрик
    prediction_curves = dict() # Список для последюущей визуализации кривых
    k=1
    # Скользящее или расширяющееся окно
    if rolling_window: 
        start_train = start_test - window_size
    else:
        start_train=0
    while True:
        if verbose is True:
            print('Iter #', k)
        cur_train = ts[start_train : start_test]
        cur_test = ts[start_test - shift : start_test + int(forecast_horizont)]
        # Есть ли экзогенные признаки
        if past_covariates is not None:
            past_cov_train = past_covariates[start_train : start_test]
            past_cov_test = past_covariates[start_test - shift : start_test + int(forecast_horizont)]
            
            model = CatBoostModel(
                **model_settings,
                output_chunk_length=forecast_horizont,
                eval_metric = 'MAPE',
                early_stopping_rounds = 15,
                task_type = "CPU",
                thread_count = 4,
                random_state=SEED
            )
            
            model.fit(series=cur_train,
                      val_series=cur_test,
                      past_covariates=past_cov_train,
                      val_past_covariates=past_cov_test)
            
            prediction = model.predict(int(forecast_horizont),
                                       series=cur_train,
                                       past_covariates=past_cov_train)
        # Если экзогенных признаков нет  
        else:            
            model = CatBoostModel(
                **model_settings,
                output_chunk_length=forecast_horizont,
                eval_metric = 'MAPE',
                early_stopping_rounds = 15,
                task_type = "CPU",
                thread_count = 4,
                random_state=SEED
            )
            
            model.fit(series=cur_train,
                      val_series=cur_test)
            
            prediction = model.predict(int(forecast_horizont),
                                       series=cur_train)
            
        # Вычисляем метрику и добавляем в список   
        metric = mape(cur_test, prediction, intersect=True)
        metrics.append(metric)
        # Добавляем спрогнозированную кривую в набор кривых для последующей отрисовки
        prediction_curves['pred_'+str(k)]=prediction
        k+=1
        
        start_test+=step
        if rolling_window:
            start_train+=step
        if start_test + int(forecast_horizont) > len(ts):
            break
            
    if save_curves==True:
        return metrics, prediction_curves
    else:
        return metrics

def objective(trial,
              ts,
              past_cov,
              forecast_len = FORECAST_LEN):
    
    settings = {
        "lags" : trial.suggest_int("lags", 1, 50),
        "lags_past_covariates" : trial.suggest_int("lags_past_covariates", 1, 50),
        "iterations" : trial.suggest_int("iterations", low=50, high=500, step=50),
        #"learning_rate" : trial.suggest_float("learning_rate", 1e-6, 0.1, log=True),
        "l2_leaf_reg" : trial.suggest_float("l2_leaf_reg", low=1.0, high=9.0, step=0.4),
        "depth" : trial.suggest_int("depth", 3, 8),
         "colsample_bylevel" : trial.suggest_float("colsample_bylevel", 0.1, 1.0),
        "min_data_in_leaf" : trial.suggest_int("min_data_in_leaf", 1, 200),
        "boosting_type" : trial.suggest_categorical("boosting_type", ["Ordered", "Plain"]),
        "bootstrap_type" : trial.suggest_categorical("bootstrap_type", ["Bayesian", "Bernoulli", "MVS"]),
    }
    if settings["bootstrap_type"] == "Bayesian":
        settings["bagging_temperature"] = trial.suggest_float("bagging_temperature", 0, 10)
    elif settings["bootstrap_type"] == "Bernoulli":
        settings["subsample"] = trial.suggest_float("subsample", 0.1, 1)
    
    settings_for_backtest = {
        "rolling_window" : trial.suggest_categorical("rolling_window", [True, False])
    }
    if settings_for_backtest["rolling_window"] == True:
        settings_for_backtest["window_size"] = trial.suggest_categorical("window_size", [52, 104])

    # Evaluate how good it is on the cross_validation for ts
    metrics = manual_backtest(model_settings=settings,
                              ts=ts,
                              past_covariates=past_cov,
                              **settings_for_backtest)
    mean_metric = np.mean(metrics)
    return mean_metric if mean_metric != np.nan else float("inf")

def setup_params(best_params):
    if best_params['rolling_window']==True:
        settings_for_backtest = {
            'rolling_window':True,
            'window_size': best_params['window_size']
        }
        del best_params['rolling_window']
        del best_params['window_size']
    else:
        settings_for_backtest = {
            'rolling_window':False
        }
        del best_params['rolling_window']
    return best_params, settings_for_backtest

def opt(ts, past_cov, iterations):
    opt_function=partial(objective, ts=ts, past_cov=past_cov)
    study = optuna.create_study(direction="minimize")
    study.optimize(opt_function, n_trials=iterations, callbacks=[LoggingCallback()])
    print("Number of finished trials: {}".format(len(study.trials)), end='\n\n')
    print(f"Best value: {study.best_value:.2f}, Best params: {study.best_trial.params}", end='\n\n')
    return study

def main(optuna: bool = False):
    current_dir = os.path.dirname(__file__)
    path_to_input = os.path.join(current_dir, '..', '..', 'data', 'processed')
    path_to_input = os.path.abspath(path_to_input)
    input_file_name = '/prepared_data.csv'

    dataset = pd.read_csv(path_to_input+input_file_name, parse_dates=[0], dtype='float32')
    print(dataset.shape)
    features = list(dataset.columns.values)
    features.remove('date')
    features.remove('lme_price_smooth')
    # Aluminium price
    data_ts = TimeSeries.from_dataframe(dataset, time_col='date', value_cols='lme_price_smooth')
    # Past covariates
    data_past_cov = TimeSeries.from_dataframe(dataset, time_col='date', value_cols=features)

    ts = data_ts[:-FORECAST_LEN]
    past_cov = data_past_cov[:-FORECAST_LEN]

    base_model_settings = {
        'lags': 30, 
        'lags_past_covariates': 44, 
        'iterations': 300, 
        'l2_leaf_reg': 2.6, 
        'depth': 6, 
        'colsample_bylevel': 0.334425755198824, 
        'min_data_in_leaf': 113, 
        'boosting_type': 'Plain', 
        'bootstrap_type': 'Bayesian', 
        'bagging_temperature': 3.6814160325002954
    }
    base_backtest_settings = {'rolling_window': True, 'window_size': 52}

    if optuna is True:
        print("Call opt function")
        study = opt(ts=ts, past_cov=past_cov, iterations=4)
        best_params = study.best_trial.params
        print("Call setup_params function")
        new_model_settings, new_backtest_settings = setup_params(best_params)
        print("Call build_and_train_model function")
        model = build_and_train_model(model_settings=new_model_settings,
                                      backtest_settings=new_backtest_settings,
                                      ts=data_ts,
                                      past_cov=data_past_cov
                                      )
        current_dir = os.path.dirname(__file__)
        path_to_save_model = os.path.join(current_dir, '..', '..', 'models')
        path_to_save_model = os.path.abspath(path_to_save_model)
        model_file_name = '/catboost_model_'
        now = datetime.now()
        today_date = now.strftime("%Y-%m-%d-%H-%M")
        model.save(path_to_save_model+model_file_name+today_date+'.pkl')
        print(f"New hyperparameters are found. The trained model was saved with the name: {path_to_save_model+model_file_name+today_date+'.pkl'}")
        return
    else:
        print("Call build_and_train_model function")
        model = build_and_train_model(model_settings=base_model_settings,
                                      backtest_settings=base_backtest_settings,
                                      ts=data_ts,
                                      past_cov=data_past_cov
                                      )
        current_dir = os.path.dirname(__file__)
        path_to_save_model = os.path.join(current_dir, '..', '..', 'models')
        path_to_save_model = os.path.abspath(path_to_save_model)
        model_file_name = '/catboost_model_'
        now = datetime.now()
        today_date = now.strftime("%Y-%m-%d-%H-%M")
        model.save(path_to_save_model+model_file_name+today_date+'.pkl')
        print(f"The trained model was saved with the name: {path_to_save_model+model_file_name+today_date+'.pkl'}")
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скрипт чтения именованных аргументов.")
    parser.add_argument("--optuna", type=bool, required=False, help="Аргумент определяет, есть ли необходимость в подборе гиперпараметров.")
    args = parser.parse_args()
    set_seed()
    main(optuna = args.optuna)