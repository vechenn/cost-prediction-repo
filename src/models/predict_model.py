import pandas as pd
from darts import TimeSeries
from darts.models import CatBoostModel

def make_forecast(dataset: pd.DataFrame):

    features = list(df.columns.values)
    features.remove('date')
    features.remove('lme_price_smooth')
    # Aluminium price
    data_ts = TimeSeries.from_dataframe(dataset, time_col='date', value_cols='lme_price_smooth')
    # Past covariates
    data_past_cov = TimeSeries.from_dataframe(dataset, time_col='date', value_cols=features)
    # Load model

    catboost_model = CatBoostModel.load("../models/catboost_model.pkl")
    prediction = catboost_model.predict(n=4,
                                        series=data_ts,
                                        past_covariates=data_past_cov
                                        )
    prediction_array = prediction.pd_series().values
    return prediction_array

if __name__ == "__main__":
    import os
    current_dir = os.path.dirname(__file__)
    path_to_input = os.path.join(current_dir, '..', '..', 'data', 'processed')
    path_to_input = os.path.abspath(path_to_input)
    input_file_name = '/prepared_data.csv'

    df = pd.read_csv(path_to_input+input_file_name, parse_dates=[0], dtype='float32')
    prediction_array = make_forecast(dataset=df)
    print(*prediction_array)