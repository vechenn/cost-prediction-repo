import numpy as np
import pandas as pd
import os

def main():
    # Определяем путь к источникам относительно текущего файла make_dataset.py
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, '..', '..', 'data', 'external')
    # Преобразуем путь в абсолютный
    data_path = os.path.abspath(data_path)

    # Задам названия источников
    path_lme = '/aluminium_lme.xlsx'
    # Индексы
    path_bloomberg_industrial_metals = '/Bloomberg_industrial_metals.csv'
    path_ftse = '/FTSE_China_A600.csv'
    path_sp_metal = '/S&P_metals_&_mining_select_industry.csv'
    path_mosexchange = '/moexmm.csv'
    path_baltic_dry_index = '/baltic_dry_index.csv'
    # Курсы валют
    path_usd_clp = '/USD_CLP.csv'
    path_usd_cny = '/USD_CNY.csv'
    path_usd_jpy = '/USD_JPY.csv'
    path_usd_eur = '/USD_EUR.csv'
    path_usd_rub = '/USD_RUB.csv'
    path_usd_jpy = '/USD_JPY.csv'
    path_dxy = '/index_USD.csv'
    # Акции
    path_chalco = '/Chalco.csv'
    path_nohgqiao = '/Hongqiao.csv'
    path_norsk_hydro = '/norsk_hydro.csv'
    path_rusal = '/rus_rual.csv'
    path_alcoa = '/Alcoa_AA.csv'
    path_kaiser = '/Kaiser_KALU.csv'
    # Макроэкономика
    path_macro = '/additional_info.xlsx'
    # Импорт и экспорт
    path_trading = '/additional_info.xlsx'


    # LME aluminium
    df_al = pd.read_excel(data_path+path_lme)
    df_al.rename(columns={'lme_aluminium_cash_settlement':'lme_price',
                          'lme_aluminium_3_month':'lme_price_3features',
                          'lme_aluminium_stock':'lme_volume'
                          }, inplace=True)
    df_al.dropna(inplace=True)

    # Индексы
    df_bloomberg_metal = pd.read_csv(data_path+path_bloomberg_industrial_metals, sep=',')
    df_bloomberg_metal['date'] = pd.to_datetime(df_bloomberg_metal['Date'])
    df_bloomberg_metal.rename(columns={'Price':'bloomberg_metals_price',
                                       'Change %':'bloomberg_metals_change'
                                       }, inplace=True)
    df_bloomberg_metal.drop(columns=["Date", "Open", "High", "Low", "Vol."], inplace=True)
    df_bloomberg_metal['bloomberg_metals_change'] = df_bloomberg_metal['bloomberg_metals_change'].apply(lambda x: float(x[:-1]))
    df_bloomberg_metal.dropna(inplace=True)

    df_ftse = pd.read_csv(data_path+path_ftse, sep=',')
    df_ftse['date'] = pd.to_datetime(df_ftse['Date'])
    df_ftse.rename(columns={'Price':'ftse_index',
                                    'Change %':'ftse_index_change'
                                    }, inplace=True)
    df_ftse.drop(columns=["Date", "Open", "High", "Low", "Vol."], inplace=True)
    df_ftse['ftse_index_change'] = df_ftse['ftse_index_change'].apply(lambda x: float(x[:-1]))
    df_ftse['ftse_index'] = df_ftse['ftse_index'].apply(lambda x: float(''.join(x.split(','))) if ',' in str(x) else float(x))
    df_ftse.dropna(inplace=True)

    df_sp_metal = pd.read_csv(data_path+path_sp_metal, sep=',')
    df_sp_metal['date'] = pd.to_datetime(df_sp_metal['Date'])
    df_sp_metal.rename(columns={'Price':'sp_metals_price',
                                'Change %':'sp_metals_change'
                                }, inplace=True)
    df_sp_metal.drop(columns=["Date", "Open", "High", "Low", "Vol."], inplace=True)
    df_sp_metal['sp_metals_change'] = df_sp_metal['sp_metals_change'].apply(lambda x: float(x[:-1]))
    df_sp_metal['sp_metals_price'] = df_sp_metal['sp_metals_price'].apply(lambda x: float(''.join(x.split(','))) if ',' in str(x) else float(x))
    df_sp_metal.dropna(inplace=True)

    df_mosexchange = pd.read_csv(data_path+path_mosexchange, sep=',')
    df_mosexchange['date'] = pd.to_datetime(df_mosexchange['Дата'], dayfirst=True)
    df_mosexchange.rename(columns={'Цена':'mosexchange_price',
                                'Изм. %':'mosexchange_change'
                                }, inplace=True)
    df_mosexchange = df_mosexchange.loc[:,['date', 'mosexchange_price', 'mosexchange_change']]
    df_mosexchange['mosexchange_change'] = df_mosexchange['mosexchange_change'].str.replace(',', '.')
    df_mosexchange['mosexchange_change'] = df_mosexchange['mosexchange_change'].apply(lambda x: float(x[:-1]) if '%' in str(x) else float(x))
    df_mosexchange['mosexchange_price'] = df_mosexchange['mosexchange_price'].str.replace('.', '')
    df_mosexchange['mosexchange_price'] = df_mosexchange['mosexchange_price'].str.replace(',', '.').astype('float64')
    df_mosexchange.dropna(inplace=True)

    df_baltic_dry_index = pd.read_csv(data_path+path_baltic_dry_index, sep=',')
    df_baltic_dry_index['date'] = pd.to_datetime(df_baltic_dry_index['Дата'], dayfirst=True)
    df_baltic_dry_index.rename(columns={'Цена':'baltic_dry_index',
                                        'Изм. %':'baltic_dry_index_change'
                                        }, inplace=True)
    df_baltic_dry_index = df_baltic_dry_index.loc[:,['date', 'baltic_dry_index', 'baltic_dry_index_change']]
    df_baltic_dry_index['baltic_dry_index_change'] = df_baltic_dry_index['baltic_dry_index_change'].str.replace(',', '.')
    df_baltic_dry_index['baltic_dry_index_change'] = df_baltic_dry_index['baltic_dry_index_change'].apply(lambda x: float(x[:-1]) if '%' in str(x) else float(x))
    df_baltic_dry_index['baltic_dry_index'] = df_baltic_dry_index['baltic_dry_index'].str.replace('.', '')
    df_baltic_dry_index['baltic_dry_index'] = df_baltic_dry_index['baltic_dry_index'].str.replace(',', '.').astype('float64')
    df_baltic_dry_index.dropna(inplace=True)

    df_usd_clp = pd.read_csv(data_path+path_usd_clp, sep=',')
    df_usd_clp.rename(columns={'Цена':'usd_clp_price',
                            'Изм. %':'usd_clp_change'
                            }, inplace=True)
    df_usd_clp['date'] = pd.to_datetime(df_usd_clp['Дата'], dayfirst=True)
    df_usd_clp = df_usd_clp.loc[:,['date', 'usd_clp_price', 'usd_clp_change']]
    df_usd_clp['usd_clp_change'] = df_usd_clp['usd_clp_change'].str.replace(',', '.')
    df_usd_clp['usd_clp_change'] = df_usd_clp['usd_clp_change'].apply(lambda x: float(x[:-1]) if '%' in str(x) else float(x))
    df_usd_clp['usd_clp_price'] = df_usd_clp['usd_clp_price'].str.replace('.', '')
    df_usd_clp['usd_clp_price'] = df_usd_clp['usd_clp_price'].str.replace(',', '.').astype('float64')
    df_usd_clp.dropna(inplace=True)

    # Курсы валют
    df_usd_cny = pd.read_csv(data_path+path_usd_cny, sep=',')
    df_usd_cny.rename(columns={'Цена':'usd_cny_price',
                            'Изм. %':'usd_cny_change'
                            }, inplace=True)
    df_usd_cny['date'] = pd.to_datetime(df_usd_cny['Дата'], dayfirst=True)
    df_usd_cny = df_usd_cny.loc[:,['date', 'usd_cny_price', 'usd_cny_change']]
    df_usd_cny['usd_cny_change'] = df_usd_cny['usd_cny_change'].str.replace(',', '.')
    df_usd_cny['usd_cny_change'] = df_usd_cny['usd_cny_change'].apply(lambda x: float(x[:-1]) if '%' in str(x) else float(x))
    df_usd_cny['usd_cny_price'] = df_usd_cny['usd_cny_price'].str.replace('.', '')
    df_usd_cny['usd_cny_price'] = df_usd_cny['usd_cny_price'].str.replace(',', '.').astype('float64')
    df_usd_cny.dropna(inplace=True)

    df_usd_jpy = pd.read_csv(data_path+path_usd_jpy, sep=',')
    df_usd_jpy.rename(columns={'Цена':'usd_jpy_price',
                            'Изм. %':'usd_jpy_change'
                            }, inplace=True)
    df_usd_jpy['date'] = pd.to_datetime(df_usd_jpy['Дата'], dayfirst=True)
    df_usd_jpy = df_usd_jpy.loc[:,['date', 'usd_jpy_price', 'usd_jpy_change']]
    df_usd_jpy['usd_jpy_change'] = df_usd_jpy['usd_jpy_change'].str.replace(',', '.')
    df_usd_jpy['usd_jpy_change'] = df_usd_jpy['usd_jpy_change'].apply(lambda x: float(x[:-1]) if '%' in str(x) else float(x))
    df_usd_jpy['usd_jpy_price'] = df_usd_jpy['usd_jpy_price'].str.replace('.', '')
    df_usd_jpy['usd_jpy_price'] = df_usd_jpy['usd_jpy_price'].str.replace(',', '.').astype('float64')
    df_usd_jpy.dropna(inplace=True)

    df_usd_eur = pd.read_csv(data_path+path_usd_eur, sep=',')
    df_usd_eur.rename(columns={'Цена':'usd_eur_price',
                            'Изм. %':'usd_eur_change'
                            }, inplace=True)
    df_usd_eur['date'] = pd.to_datetime(df_usd_eur['Дата'], dayfirst=True)
    df_usd_eur = df_usd_eur.loc[:,['date', 'usd_eur_price', 'usd_eur_change']]
    df_usd_eur['usd_eur_change'] = df_usd_eur['usd_eur_change'].str.replace(',', '.')
    df_usd_eur['usd_eur_change'] = df_usd_eur['usd_eur_change'].apply(lambda x: float(x[:-1]) if '%' in str(x) else float(x))
    df_usd_eur['usd_eur_price'] = df_usd_eur['usd_eur_price'].str.replace('.', '')
    df_usd_eur['usd_eur_price'] = df_usd_eur['usd_eur_price'].str.replace(',', '.').astype('float64')
    df_usd_eur.dropna(inplace=True)

    df_usd_rub = pd.read_csv(data_path+path_usd_rub, sep=',')
    df_usd_rub.rename(columns={'Цена':'usd_rub_price',
                            'Изм. %':'usd_rub_change'
                            }, inplace=True)
    df_usd_rub['date'] = pd.to_datetime(df_usd_rub['Дата'], dayfirst=True)
    df_usd_rub = df_usd_rub.loc[:,['date', 'usd_rub_price', 'usd_rub_change']]
    df_usd_rub['usd_rub_change'] = df_usd_rub['usd_rub_change'].str.replace(',', '.')
    df_usd_rub['usd_rub_change'] = df_usd_rub['usd_rub_change'].apply(lambda x: float(x[:-1]) if '%' in str(x) else float(x))
    df_usd_rub['usd_rub_price'] = df_usd_rub['usd_rub_price'].str.replace('.', '')
    df_usd_rub['usd_rub_price'] = df_usd_rub['usd_rub_price'].str.replace(',', '.').astype('float64')
    df_usd_rub.dropna(inplace=True)

    df_dxy = pd.read_csv(data_path+path_dxy, sep=',')
    df_dxy.rename(columns={'Цена':'dxy_price',
                        'Изм. %':'dxy_change'
                        }, inplace=True)
    df_dxy['date'] = pd.to_datetime(df_dxy['Дата'], dayfirst=True)
    df_dxy = df_dxy.loc[:,['date', 'dxy_price', 'dxy_change']]
    df_dxy['dxy_change'] = df_dxy['dxy_change'].str.replace(',', '.')
    df_dxy['dxy_change'] = df_dxy['dxy_change'].apply(lambda x: float(x[:-1]) if '%' in str(x) else float(x))
    df_dxy['dxy_price'] = df_dxy['dxy_price'].str.replace('.', '')
    df_dxy['dxy_price'] = df_dxy['dxy_price'].str.replace(',', '.').astype('float64')
    df_dxy.dropna(inplace=True)

    # Акции
    df_chalco = pd.read_csv(data_path+path_chalco, sep=',')
    df_chalco['date'] = pd.to_datetime(df_chalco['Date'])
    df_chalco.rename(columns={'Close':'chalco_price',
                            'Volume':'chalco_volume'
                            }, inplace=True)
    df_chalco = df_chalco.loc[:,['date', 'chalco_price', 'chalco_volume']]
    df_chalco.dropna(inplace=True)
    
    df_hongqiao = pd.read_csv(data_path+path_nohgqiao, sep=',')
    df_hongqiao['date'] = pd.to_datetime(df_hongqiao['Date'])
    df_hongqiao.rename(columns={'Close':'hongqiao_price',
                                'Volume':'hongqiao_volume'
                                }, inplace=True)
    df_hongqiao = df_hongqiao.loc[:,['date', 'hongqiao_price', 'hongqiao_volume']]
    df_hongqiao.dropna(inplace=True)

    df_norsk_hydro = pd.read_csv(data_path+path_norsk_hydro, sep=',')
    df_norsk_hydro['date'] = pd.to_datetime(df_norsk_hydro['Date'])
    df_norsk_hydro.rename(columns={'Close':'norsk_hydro_price',
                                'Volume':'norsk_hydro_volume'
                                }, inplace=True)
    df_norsk_hydro = df_norsk_hydro.loc[:,['date', 'norsk_hydro_price', 'norsk_hydro_volume']]
    df_norsk_hydro.dropna(inplace=True)

    df_rusal = pd.read_csv(data_path+path_rusal, sep=',')
    df_rusal['date'] = pd.to_datetime(df_rusal['Date'])
    df_rusal.rename(columns={'Close':'rusal_price',
                            'Volume':'rusal_volume'
                            }, inplace=True)
    df_rusal = df_rusal.loc[:,['date', 'rusal_price', 'rusal_volume']]
    df_rusal.dropna(inplace=True)

    df_alcoa = pd.read_csv(data_path+path_alcoa, sep=',')
    df_alcoa['date'] = pd.to_datetime(df_alcoa['Date'])
    df_alcoa.rename(columns={'Close':'alcoa_price',
                            'Volume':'alcoa_volume'
                            }, inplace=True)
    df_alcoa = df_alcoa.loc[:,['date', 'alcoa_price', 'alcoa_volume']]
    df_alcoa.dropna(inplace=True)

    df_kaiser = pd.read_csv(data_path+path_kaiser, sep=',')
    df_kaiser['date'] = pd.to_datetime(df_kaiser['Date'])
    df_kaiser.rename(columns={'Close':'kaiser_price',
                            'Volume':'kaiser_volume'
                            }, inplace=True)
    df_kaiser = df_kaiser.loc[:,['date', 'kaiser_price', 'kaiser_volume']]
    df_kaiser.dropna(inplace=True)

    # Макроэкономика
    df_australia_fed_rate = pd.read_excel(data_path+path_macro,
                                sheet_name='macro',
                                header=None,
                                skiprows=3,
                                names=['date','australia_fed_rate_value'],
                                usecols="AK:AL"
                                )
    df_australia_fed_rate['date'] = pd.to_datetime(df_australia_fed_rate['date'], dayfirst=True)
    df_australia_fed_rate.dropna(inplace=True)

    df_brazil_pmi = pd.read_excel(data_path+path_macro,
                                sheet_name='macro',
                                header=None,
                                skiprows=3,
                                names=['date','brazil_pmi_value'],
                                usecols="AD:AE"
                                )
    df_brazil_pmi['date'] = pd.to_datetime(df_brazil_pmi['date'], dayfirst=True)
    df_brazil_pmi.dropna(inplace=True)

    df_brazil_inflation = pd.read_excel(data_path+path_macro,
                                sheet_name='macro',
                                header=None,
                                skiprows=3,
                                names=['date','brazil_inflation_value'],
                                usecols="AH:AI"
                                )
    df_brazil_inflation['date'] = pd.to_datetime(df_brazil_inflation['date'], dayfirst=True)
    df_brazil_inflation.dropna(inplace=True)

    df_brazil_fed_rate = pd.read_excel(data_path+path_macro,
                                sheet_name='macro',
                                header=None,
                                skiprows=3,
                                names=['date','brazil_fed_rate_value'],
                                usecols="AF:AG"
                                )
    df_brazil_fed_rate['date'] = pd.to_datetime(df_brazil_fed_rate['date'], dayfirst=True)
    df_brazil_fed_rate.dropna(inplace=True)

    df_china_gdp = pd.read_excel(data_path+path_macro,
                                sheet_name='macro',
                                header=None,
                                skiprows=3,
                                names=['date','china_gdp_value'],
                                usecols="A:B"
                                )
    df_china_gdp['date'] = pd.to_datetime(df_china_gdp['date'], dayfirst=True)
    df_china_gdp.dropna(inplace=True)

    df_china_pmi = pd.read_excel(data_path+path_macro,
                                sheet_name='macro',
                                header=None,
                                skiprows=3,
                                names=['date','china_pmi_value'],
                                usecols="C:D"
                                )
    df_china_pmi['date'] = pd.to_datetime(df_china_pmi['date'], dayfirst=True)
    df_china_pmi.dropna(inplace=True)

    df_china_inflation = pd.read_excel(data_path+path_macro,
                                sheet_name='macro',
                                header=None,
                                skiprows=3,
                                names=['date','china_inflation_value'],
                                usecols="E:F"
                                )
    df_china_inflation['date'] = pd.to_datetime(df_china_inflation['date'], dayfirst=True)
    df_china_inflation.dropna(inplace=True)

    df_china_fed_rate = pd.read_excel(data_path+path_macro,
                                sheet_name='macro',
                                header=None,
                                skiprows=3,
                                names=['date','china_fed_rate_value'],
                                usecols="G:H"
                                )
    df_china_fed_rate['date'] = pd.to_datetime(df_china_fed_rate['date'], dayfirst=True)
    df_china_fed_rate.dropna(inplace=True)

    df_china_composite_pmi = pd.read_excel(data_path+path_macro,
                                sheet_name='macro',
                                header=None,
                                skiprows=3,
                                names=['date','china_composite_pmi_value'],
                                usecols="I:J"
                                )
    df_china_composite_pmi['date'] = pd.to_datetime(df_china_composite_pmi['date'], dayfirst=True)
    df_china_composite_pmi.dropna(inplace=True)

    df_peru_gdp = pd.read_excel(data_path+path_macro,
                                sheet_name='macro',
                                header=None,
                                skiprows=3,
                                names=['date','peru_gdp_value'],
                                usecols="L:M"
                                )
    df_peru_gdp['date'] = pd.to_datetime(df_peru_gdp['date'], dayfirst=True)
    df_peru_gdp.dropna(inplace=True)

    df_peru_fed_rate = pd.read_excel(data_path+path_macro,
                                sheet_name='macro',
                                header=None,
                                skiprows=3,
                                names=['date','peru_fed_rate_value'],
                                usecols="N:O"
                                )
    df_peru_fed_rate['date'] = pd.to_datetime(df_peru_fed_rate['date'], dayfirst=True)
    df_peru_fed_rate.dropna(inplace=True)

    df_peru_inflation = pd.read_excel(data_path+path_macro,
                                sheet_name='macro',
                                header=None,
                                skiprows=3,
                                names=['date','peru_producer_price_index'],
                                usecols="P:Q"
                                )
    df_peru_inflation['date'] = pd.to_datetime(df_peru_inflation['date'], dayfirst=True)
    df_peru_inflation.dropna(inplace=True)

    df_peru_pmi = pd.read_excel(data_path+path_macro,
                                sheet_name='macro',
                                header=None,
                                skiprows=3,
                                names=['date','peru_consumer_price_index'],
                                usecols="R:S"
                                )
    df_peru_pmi['date'] = pd.to_datetime(df_peru_pmi['date'], dayfirst=True)
    df_peru_pmi.dropna(inplace=True)

    df_usa_gdp = pd.read_excel(data_path+path_macro,
                                sheet_name='macro',
                                header=None,
                                skiprows=3,
                                names=['date','usa_gdp_value'],
                                usecols="U:V"
                                )
    df_usa_gdp['date'] = pd.to_datetime(df_usa_gdp['date'], dayfirst=True)
    df_usa_gdp.dropna(inplace=True)

    df_usa_fed_rate = pd.read_excel(data_path+path_macro,
                                sheet_name='macro',
                                header=None,
                                skiprows=3,
                                names=['date','usa_fed_rate_value'],
                                usecols="W:X"
                                )
    df_usa_fed_rate['date'] = pd.to_datetime(df_usa_fed_rate['date'], dayfirst=True)
    df_usa_fed_rate.dropna(inplace=True)

    df_usa_inflation = pd.read_excel(data_path+path_macro,
                                sheet_name='macro',
                                header=None,
                                skiprows=3,
                                names=['date','usa_inflation_value'],
                                usecols="Y:Z"
                                )
    df_usa_inflation['date'] = pd.to_datetime(df_usa_inflation['date'], dayfirst=True)
    df_usa_inflation.dropna(inplace=True)

    df_usa_pmi = pd.read_excel(data_path+path_macro,
                                sheet_name='macro',
                                header=None,
                                skiprows=3,
                                names=['date','usa_pmi_value'],
                                usecols="AA:AB"
                                )
    df_usa_pmi['date'] = pd.to_datetime(df_usa_pmi['date'], dayfirst=True)
    df_usa_pmi.dropna(inplace=True)

    # Импорт и экспорт
    df_brazil_import = pd.read_excel(data_path+path_trading, sheet_name='trademap', header=0, usecols="A:B")
    df_brazil_import['date'] = pd.to_datetime(df_brazil_import['date']) + pd.offsets.MonthEnd()

    df_brazil_export = pd.read_excel(data_path+path_trading, sheet_name='trademap', header=0, usecols="C:D")
    df_brazil_export.rename(columns = {'date.1':'date'}, inplace=True)
    df_brazil_export['date'] = pd.to_datetime(df_brazil_export['date']) + pd.offsets.MonthEnd()


    df_usa_import = pd.read_excel(data_path+path_trading, sheet_name='trademap', header=0, usecols="E:F")
    df_usa_import.rename(columns = {'date.2':'date'}, inplace=True)
    df_usa_import['date'] = pd.to_datetime(df_usa_import['date']) + pd.offsets.MonthEnd()

    df_usa_export = pd.read_excel(data_path+path_trading, sheet_name='trademap', header=0, usecols="G:H")
    df_usa_export.rename(columns = {'date.3':'date'}, inplace=True)
    df_usa_export['date'] = pd.to_datetime(df_usa_export['date']) + pd.offsets.MonthEnd()


    df_china_import = pd.read_excel(data_path+path_trading, sheet_name='trademap', header=0, usecols="I:J")
    df_china_import.rename(columns = {'date.4':'date'}, inplace=True)
    df_china_import['date'] = pd.to_datetime(df_china_import['date']) + pd.offsets.MonthEnd()

    df_china_export = pd.read_excel(data_path+path_trading, sheet_name='trademap', header=0, usecols="K:L")
    df_china_export.rename(columns = {'date.5':'date'}, inplace=True)
    df_china_export['date'] = pd.to_datetime(df_china_export['date']) + pd.offsets.MonthEnd()


    df_australia_import = pd.read_excel(data_path+path_trading, sheet_name='trademap', header=0, usecols="M:N")
    df_australia_import.rename(columns = {'date.6':'date'}, inplace=True)
    df_australia_import['date'] = pd.to_datetime(df_australia_import['date']) + pd.offsets.MonthEnd()

    df_australia_export = pd.read_excel(data_path+path_trading, sheet_name='trademap', header=0, usecols="O:P")
    df_australia_export.rename(columns = {'date.7':'date'}, inplace=True)
    df_australia_export['date'] = pd.to_datetime(df_australia_export['date']) + pd.offsets.MonthEnd()

    list_of_df = [df_al, df_bloomberg_metal, df_ftse, df_sp_metal, df_mosexchange, df_baltic_dry_index,
    df_usd_clp, df_usd_cny, df_usd_jpy, df_usd_eur, df_usd_rub, df_dxy,
    df_chalco, df_hongqiao, df_norsk_hydro, df_rusal, df_alcoa, df_kaiser,
    df_australia_fed_rate, df_brazil_pmi, df_brazil_inflation, df_brazil_fed_rate,
    df_china_gdp, df_china_pmi, df_china_inflation, df_china_fed_rate, df_china_composite_pmi,
    df_peru_gdp, df_peru_fed_rate, df_peru_inflation, df_peru_pmi,
    df_usa_gdp, df_usa_fed_rate, df_usa_inflation, df_usa_pmi,
    df_brazil_import, df_brazil_export, df_usa_import, df_usa_export,
    df_china_import, df_china_export, df_australia_import, df_australia_export]

    #Подрезал данные с 1 ноября 2017 года по 31 мая 2024
    d = pd.date_range(start='11/1/2017', end='05/31/2024', freq="D")
    df = pd.DataFrame(data=d, columns=['date'])
    for i in list_of_df:
        df = df.join(i.set_index('date'), on='date', how='left')
    df.set_index('date', inplace=True)

    # Определяем путь к источникам относительно текущего файла make_dataset.py
    current_dir = os.path.dirname(__file__)
    path_to_save = os.path.join(current_dir, '..', '..', 'data', 'raw')
    # Преобразуем путь в абсолютный
    path_to_save = os.path.abspath(path_to_save)
    file_name = '/dataset_with_raw_data.csv'
    df.to_csv(path_to_save+file_name)

if __name__ == "__main__":
    main()
    