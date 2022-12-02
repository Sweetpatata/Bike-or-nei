import pandas as pd
import numpy as np
import sys
import urllib.parse
import requests
from datetime import datetime, date, timezone, timedelta
from sklearn.preprocessing import OneHotEncoder

BASE_URL = "https://weather.lewagon.com"
#oslo_lat = 59.919602443955355
#oslo_lon = 10.752152108688852


def weather_forecast(lat=59.919602443955355, lon=10.752152108688852):
    '''Return a 5-day weather forecast for the city, given its latitude and longitude.'''
    url = urllib.parse.urljoin(BASE_URL, "/data/2.5/forecast")
    forecasts = requests.get(url, params={'lat': lat, 'lon': lon, 'units': 'metric'}).json()['list']
    return forecasts

def check_float(column):
    '''Returns formated columns according to transfor_forecast function requirements'''
    for index, row in enumerate(column):
        if type(row)==float:
            column[index] = 0
        else:
            column[index] = row['3h']
    return column

def transform_forecast():
    uncleaned_forecast = pd.DataFrame(weather_forecast(oslo_lat, oslo_lon))
    uncleaned_forecast = uncleaned_forecast.drop(columns=['dt','weather','clouds','visibility','pop','sys'])

    uncleaned_forecast['temp_min'] = uncleaned_forecast['main'].apply(lambda x: x['temp_min'])
    uncleaned_forecast['temp_max'] = uncleaned_forecast['main'].apply(lambda x: x['temp_max'])
    uncleaned_forecast['wind_speed'] = uncleaned_forecast['wind'].apply(lambda x: x['speed'])

    if 'snow' in uncleaned_forecast.columns:
        check_float(uncleaned_forecast['snow'])
    if 'rain' in uncleaned_forecast.columns:
        check_float(uncleaned_forecast['rain'])

    uncleaned_forecast = uncleaned_forecast.drop(columns=['main','wind',])
    uncleaned_forecast['dt_txt'] = uncleaned_forecast['dt_txt'].apply(lambda x: x.split(' ')[0])


    day_grouped_forecast = uncleaned_forecast.groupby('dt_txt').agg({'temp_min':'min',
                                                                    'temp_max':'max',
                                                                    'wind_speed':'mean'})

    if 'snow' in uncleaned_forecast.columns:
        day_grouped_forecast['snow_total'] = uncleaned_forecast.groupby('dt_txt').agg({'snow':'sum'})['snow']
    else:
        day_grouped_forecast['snow_total'] = 0
    if 'rain' in uncleaned_forecast.columns:
        day_grouped_forecast['rainfall_total'] = uncleaned_forecast.groupby('dt_txt').agg({'rain':'sum'})['rain']
    else:
        day_grouped_forecast['rainfall_total'] = 0

    cleaned_forecast = day_grouped_forecast.reset_index()
    cleaned_forecast = cleaned_forecast.rename({'dt_txt':'date',
                                                'wind_speed':'wind_speed_avg'}, axis=1)

    cleaned_forecast['date'] = pd.to_datetime(cleaned_forecast['date'])
    cleaned_forecast['day_of_week'] = cleaned_forecast['date'].dt.dayofweek
    cleaned_forecast['Month'] = cleaned_forecast['date'].dt.month


    return cleaned_forecast

transform_forecast()
