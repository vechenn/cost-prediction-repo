Предсказание стоимости алюминия
==============================
1.Задача
------------
Здесь будет описание задачи
------------

2.Целевая переменная
------------
Здесь будет описание таргета
------------

3.Исходные данные
------------
Al_lme_prices.csv - Котировки алюминия на London metal exchange

Основными "игроками" на рынке алюминия выступают Китай, США, Россия, Бразилия и Австралия, для этого собрана различная информация по странам
*_PMI.csv - индекс производственной активности
*_resource_changing.csv - изменение запасов
*_inflation.csv - инфляция
*_vvp_per_human.csv - ввп на душу населения

Trade_Map_exported_* - объемы экспорта
Trade_Map_imported_* - объемы импорта
Trade_Map_balance_* - экспорт-импорт баланс

China_Chalco, China-Hongqiao, NOW_Norsk_Hydro, RUS_RUAL, USA_Alcoa_corp, USA_Kaiser - котировки акций крупных компаний по алюминию

Bloomberg_Industrial_Metals.csv, FTSE_ChinaA600_Industrial_Metal.csv, S&P_Metals_and_Mining_Select_Industry.csv - индексы

HKD=X - курс гонконгского доллара к доллару
RUB_CNY - курс рубля к юаню
USD_RUB - курс доллара к рублю

Большая часть данных в промежутке с 02 января 2018 по 27 октября 2023
Некоторые помесячные и погодовые, требуется интерполяция, подготовка данных
------------

4.Метрика 
------------
Здесь будет описание метрики
------------

5.Организация репозитория будет постепенно корректироваться и пополняться информацией
------------

    ├── LICENSE
    ├── Makefile           <- 
    ├── data
    │   ├── external       <- Данные из внешних источников
    │   ├── interim        <-
    │   ├── processed      <-
    │   └── raw            <-
    │
    ├── docs               <-
    │
    ├── models             <-
    │
    ├── notebooks          <-
    │
    ├── references         <-
    │
    ├── reports            <-
    │   └── figures        <-
    │
    ├── requirements.txt   <-
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
