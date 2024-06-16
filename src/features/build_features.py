import numpy as np
import pandas as pd
import tsfresh
import logging
from tsfresh.utilities.dataframe_functions import make_forecasting_frame
from tsfresh import extract_features

def data_preprocessing(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Фукнция выполняет базовую предобработку входных данных:
    -преобразование в недельные дискреты
    -логарифмирование некоторых признаков
    -сглаживание таргета
    -смещение лагов
    -заполнение пропусков
    '''
    df['hongqiao_volume'] = df['hongqiao_volume'].replace(0, df['hongqiao_volume'].median())
    df_bfill = df.loc[:,('peru_producer_price_index',
                         'peru_consumer_price_index',
                         'export_china_value')].bfill()
    df_interpol = df.loc[:,('lme_price', 'lme_price_3features',
                            'bloomberg_metals_price', 'mosexchange_price',
                            'sp_metals_price', 'hongqiao_price', 'hongqiao_volume',
                            'norsk_hydro_price')].interpolate(method='time', limit_area='inside')
    df_fillna = pd.concat([df_interpol, df_bfill], axis=1)
    del df_bfill,
    del df_interpol

    df_fillna['log10_hongqiao_volume'] = np.log10(df_fillna['hongqiao_volume'])
    df_fillna['lme_price_smooth'] = df_fillna.lme_price.rolling(7, min_periods=1).mean()
    df_fillna.drop(columns=['hongqiao_volume', 'lme_price'], inplace=True)

    dataset_per_week = df_fillna.reset_index().groupby([pd.Grouper(key='date', freq='W')]).mean()
    del df_fillna

    dict_for_shift = {
        "export_china_value": 9,
        "peru_producer_price_index":9,
        "peru_consumer_price_index":9,
    }
    for i in dict_for_shift.items():
        dataset_per_week[i[0]] = dataset_per_week[i[0]].shift(i[1])

    dataset_per_week = dataset_per_week.iloc[:-1]
    dataset_per_week.dropna(inplace=True)
    preprocessed_dataset = dataset_per_week.copy()
    del dataset_per_week
    
    return preprocessed_dataset

def generate_ts_fresh_features(dataset: pd.DataFrame) -> pd.DataFrame:
    #logging.getLogger('tsfresh').setLevel(logging.WARNING)
    fc_parameters = {
        "abs_energy": None,
        "absolute_maximum": None,
        "cwt_coefficients": [{'widths': (2, 5, 10, 20), 'coeff': 0, 'w': 5},
                            {'widths': (2, 5, 10, 20), 'coeff': 0, 'w': 20}],
        "fft_coefficient": [{'coeff': 0, 'attr': 'real'}],
        "maximum": None,
        "median": None,
        "minimum": None,
        "quantile": [{'q': 0.1},
                    {'q': 0.3},
                    {'q': 0.4},
                    {'q': 0.6},
                    {'q': 0.8},
                    {'q': 0.9}],
        "root_mean_square": None
    }
    features_for_tsfresh = ["lme_price_smooth",
                            "lme_price_3features",
                            "peru_producer_price_index",
                            "sp_metals_price",
                            "peru_consumer_price_index",
                            "log10_hongqiao_volume",
                            "hongqiao_price",
                            "bloomberg_metals_price",
                            "mosexchange_price",
                            "norsk_hydro_price",
                            "export_china_value"
                            ]

    short_list = ['value__abs_energy_lme_price_3features_4_weeks',
                  'value__abs_energy_peru_producer_price_index_12_weeks',
                  'value__absolute_maximum_sp_metals_price_4_weeks',
                  'value__cwt_coefficients__coeff_0__w_20__widths_(2, 5, 10, 20)_peru_consumer_price_index_4_weeks',
                  'value__cwt_coefficients__coeff_0__w_5__widths_(2, 5, 10, 20)_peru_consumer_price_index_9_weeks',
                  'value__fft_coefficient__attr_"real"__coeff_0_lme_price_3features_2_weeks',
                  'value__maximum_lme_price_3features_12_weeks',
                  'value__maximum_lme_price_smooth_4_weeks',
                  'value__median_peru_producer_price_index_4_weeks',
                  'value__minimum_lme_price_3features_9_weeks',
                  'value__minimum_log10_hongqiao_volume_12_weeks',
                  'value__quantile__q_0.1_hongqiao_price_12_weeks',
                  'value__quantile__q_0.3_bloomberg_metals_price_9_weeks',
                  'value__quantile__q_0.4_lme_price_smooth_2_weeks',
                  'value__quantile__q_0.4_sp_metals_price_12_weeks',
                  'value__quantile__q_0.6_mosexchange_price_12_weeks',
                  'value__quantile__q_0.6_norsk_hydro_price_9_weeks',
                  'value__quantile__q_0.6_peru_producer_price_index_9_weeks',
                  'value__quantile__q_0.8_sp_metals_price_12_weeks',
                  'value__quantile__q_0.9_export_china_value_12_weeks',
                  'value__root_mean_square_lme_price_3features_9_weeks']
    
    cnt = 0
    
    extracted_features = pd.DataFrame(index=pd.date_range(start=dataset.index.min().strftime("%Y-%m-%d"), 
                                                          end=dataset.index.max().strftime("%Y-%m-%d"), 
                                                          freq='W'))
    extracted_features.index.name = 'date' # create frame with index 'date'
    #list_of_columns = dataset.columns.values.copy()
    for i in features_for_tsfresh: # loop over exogenous features
        cnt += 1
        for k in [2,4,9,12]: # loop over 2, 4, 9, 12 weeks window sizes
            series = dataset[i].copy() # slice on feature
            df_rolled = make_forecasting_frame(series, kind='price', max_timeshift=k, rolling_direction=1) # generate ts 
            df_features = extract_features(df_rolled[0].drop(columns=['kind']),
                                           column_id="id",
                                           column_sort="time",
                                           default_fc_parameters=fc_parameters) # generate special features
            suf = '_'+i+'_'+str(k)+'_weeks' # setup suffix
            df_features = df_features.add_suffix(suf) # setup suffix by the window size
            df_features.reset_index(inplace=True)
            df_features.drop(columns=['level_0'], inplace=True)
            df_features.rename(columns={'level_1': 'date'}, inplace=True) 
            df_features.set_index('date', inplace=True) # delete multiindex and setup new index
            df_features = df_features.dropna(axis=1) # dropna columns with Nan-s
            extracted_features = extracted_features.join(df_features,
                                                         on='date',
                                                         how='left') # join
            #print(f"Joined succesfully! Columns count is {extracted_features.shape[1]}")
            del series
            del df_rolled
            del df_features
        #print("Created features for", i)
        print(f"Left {len(features_for_tsfresh) - cnt} features")
    extracted_features = extracted_features.loc[:, short_list]
    extracted_features = extracted_features.iloc[1:]
    extracted_features = extracted_features.join(dataset["lme_price_smooth"], on='date', how='left')
    return extracted_features

if __name__ == "__main__":
    import os
    current_dir = os.path.dirname(__file__)

    path_to_input = os.path.join(current_dir, '..', '..', 'data', 'raw')
    path_to_input = os.path.abspath(path_to_input)
    input_file_name = '/dataset_with_raw_data.csv'

    path_to_output = os.path.join(current_dir, '..', '..', 'data', 'processed')
    path_to_output = os.path.abspath(path_to_output)
    output_file_name = '/prepared_data.csv'

    input_file = path_to_input+input_file_name
    output_file = path_to_output+output_file_name
    
    df = pd.read_csv(input_file, parse_dates=True, index_col=0) # read input file
    print("Start data preprocessing.")
    preprocessed_dataset = data_preprocessing(df=df)
    print("Start feature extraction.")
    extracted_features = generate_ts_fresh_features(dataset=preprocessed_dataset) # generate new features 
    print("Save prepared data.")
    extracted_features.to_csv(output_file) # save extracted deatures