Предсказание стоимости алюминия
==============================
Задача
------------
Прогнозирование стоимости алюминия на Лондонской бирже металлов (LME) на горизонте 30 дней.  
Практическая применимость решения поставленной задачи сводится к формированию оптимальной торговой стратегии или же к прогнозированию бюджета компаний-потребителей алюминия.

------------

Целевая переменная
------------
Здесь будет описание таргета

------------

Исходные данные
------------
Al_lme_prices.csv - стоимость алюминия на LME (London metal exchange)  
Основными "игроками" на рынке алюминия выступают Китай, США, Россия, Бразилия и Австралия, для этого собрана различная информация по странам:  
Country_PMI.csv - индекс производственной активности  
Country_resource_changing.csv - изменение запасов  
Country_inflation.csv - инфляция  
Country_vvp_per_human.csv - ввп на душу населения  
Trade_Map_exported_country - объемы экспорта  
Trade_Map_imported_country - объемы импорта  
Trade_Map_balance_country - экспорт-импорт баланс  

China_Chalco, China-Hongqiao, NOW_Norsk_Hydro, RUS_RUAL, USA_Alcoa_corp, USA_Kaiser - котировки акций крупных компаний по алюминию

Bloomberg_Industrial_Metals.csv, FTSE_ChinaA600_Industrial_Metal.csv, S&P_Metals_and_Mining_Select_Industry.csv - индексы

HKD=X - курс доллара к гонконгскому доллару    
RUB_CNY - курс рубля к юаню  
USD_RUB - курс доллара к рублю  

Большая часть данных в промежутке с 02 января 2018 по 27 октября 2023  
Некоторые помесячные и погодовые, требуется интерполяция, подготовка данных

------------

Метрика 
------------
Здесь будет описание метрики

------------

Организация репозитория (будет постепенно корректироваться и пополняться информацией)
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
