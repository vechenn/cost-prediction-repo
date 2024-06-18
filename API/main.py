import sys
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import pandas as pd
from io import StringIO

sys.path.append("../src/features")
sys.path.append("../src/models")

from build_features import data_preprocessing, generate_ts_fresh_features
from predict_model import make_forecast

app = FastAPI()

class PredictionResponse(BaseModel):
    week_1: float
    week_2: float
    week_3: float
    week_4: float

@app.get('/', summary='Root')
def root():
    return {'Привет! Отправьте мне CSV-файл для предсказания.'}

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    # Преобразуем файл в DataFrame
    contents = await file.read()
    # df = pd.read_csv(StringIO(contents.decode('utf-8')), parse_dates=[0], dtype='float32')
    string_io = StringIO(contents.decode('utf-8'))
        
    # Преобразуем содержимое файла в Pandas DataFrame
    df = pd.read_csv(string_io, parse_dates=True, index_col=0, dtype='float32')
    # df['date'] = pd.to_datetime(df['date'])
    # Предобрабатываем данные
    df_preprocessed = data_preprocessing(df)

    # Получаем фичи
    df_features = generate_ts_fresh_features(df_preprocessed)
    df_features.reset_index(inplace=True)
    # Получаем прогноз
    predictions = make_forecast(df_features)

    # Выводим результат
    return PredictionResponse(
        week_1=round(predictions[0], 1),
        week_2=round(predictions[1], 1),
        week_3=round(predictions[2], 1),
        week_4=round(predictions[3], 1)
    )

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)