import pickle
import pandas as pd
from enum import Enum
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from darts import TimeSeries
from typing import List, Any
from io import StringIO


app = FastAPI()

def load_model(model_path: str = './model_cbr.pkl') -> Any:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

model = load_model()
prediction_step = 4 

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Проверяем, что файл в формате CSV
    if file.filename.endswith('.csv'):
        # Читаем содержимое файла в формате 'string'
        contents = await file.read()
        string_io = StringIO(contents.decode('utf-8'))
        
        # Преобразуем содержимое файла в Pandas DataFrame
        df = pd.read_csv(string_io, parse_dates=[0], dtype='float32')
        data_ts = TimeSeries.from_dataframe(df, time_col='date', value_cols='lme_price_smooth')
        data_past_cov = TimeSeries.from_dataframe(df, time_col='date', value_cols=df.columns.values[1:-5])
        
        pred_tmp = model.predict(
            n=prediction_step,
            series=data_ts,
            past_covariates=data_past_cov
           )
        
        # Возвращаем предсказания в ответе
        return {
            '1': round(pred_tmp.values()[0, 0], 2),
            '2': round(pred_tmp.values()[1, 0], 2),
            '3': round(pred_tmp.values()[2, 0], 2),
            '4': round(pred_tmp.values()[3, 0], 2)
        }
    else:
        return {"error": "File format not supported. Please upload a CSV file."}    

# Запуск сервера
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

