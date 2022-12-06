from fastapi import FastAPI, Request, UploadFile
import pandas as pd
import numpy as np
import sys
import urllib.parse
import requests
import schedule, time
from ml_logic.registry import load_model, pred
from datetime import datetime, timedelta
from ml_logic.weather_API import encode_weather
import os
from ml_logic.params import LOCAL_REGISTRY_PATH

app = FastAPI()

#app.state.model = load_model()

# ONLY IN CASE OF AUTOMATED PREDICTION - scheduled forecast call and prediction
#@app.get('/forecast_prediction')
#def forecast_and_predict():
#    forecast_df = encode_weather() # returns df prediction ready df of today + 5 days
#    model_df = load_model()
#    date = datetime.today()
#    for row in forecast_df:
#        prediction = pred(row, model_df)
#        name = f"{str(date).split(' ')[0]}.csv"
#        path = os.path.join(LOCAL_REGISTRY_PATH, 'raw_data/dump_pred', name)
#        prediction.to_csv(path)
#        date += timedelta(days=1)
#    return None

#schedule.every().day.at("00:00").do(forecast_and_predict)
#while True:
#    schedule.run_pending()
#    time.sleep(0)
# A "maybe" solution:
# run job until a specific datetime
#schedule.every(1).hours.until(datetime(2020, 5, 17, 11, 36, 20)).do(job)
#Look at the lecture on wednesday (model life circle: Prefect)


# prediction response
@app.post("/predict")
async def predict(date: Request):
    data = await date.body()
    data = data.decode()
    data = data.split()
    data = data[5]
    data = datetime.strptime(data, "%Y-%m-%d").date()

    print(data)
    return data

@app.get("/")
def root():
    # $CHA_BEGIN
    return dict(greeting="Hello")
    # $CHA_END
