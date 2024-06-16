Предсказание стоимости алюминия
==============================
Задача
------------
Прогнозирование стоимости алюминия на Лондонской бирже металлов (LME) на горизонте 4 недель.  
Практическая применимость решения поставленной задачи сводится к формированию оптимальной торговой стратегии или же к прогнозированию бюджета компаний-потребителей алюминия.

------------

Целевая переменная
------------
Абсолютное значение стоимости алюминия на бирже LME

------------

Исходные данные
------------
Основными "игроками" на рынке алюминия выступают Китай, США, Россия, Бразилия и Австралия, для этого собрана различная информация, связанная с данными странами. Собрана информация о котировках акций некоторых компаний, связанных с промыслом алюминия.  
Подробную информацию об источниках можно найти в docs/source_description.xlsx
Некоторые данные поступают с задержкой.  
Некоторые помесячные/поквартальные, требуется интерполяция, подготовка данных.  

------------

Метрика 
------------
MAPE  

------------

Организация репозитория (будет постепенно корректироваться и пополняться информацией)
------------

    ├── LICENSE
    ├── Makefile           <- 
    ├── data
    │   ├── external       <- Данные из внешних источников
    │   ├── interim        <- 
    │   ├── processed      <- Обработанные данные, готовые для использования при моделировании
    │   └── raw            <- Сырые данные, собранные в единный фрейм
    │
    ├── docs               <- Папка содержит excel таблицу с описанием источников
    │
    ├── models             <- Модели в формате *.pkl
    │
    ├── notebooks          <- jupyter ноутбуки
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
    │   ├── data           <- Скрипт для загрузки и компоновки данных в единный фрейм
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Скрипт для генерации необходимых признаков
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
