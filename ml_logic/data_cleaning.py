import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date, timezone, timedelta
import glob

def clean_data(folder_path):
    files = glob.glob(f'{folder_path}/*.csv')
    df_raw = pd.DataFrame()
    for file in files:
        df_raw = pd.concat([df_raw, pd.read_csv(file, parse_dates=['started_at', 'ended_at'])])

    df_raw['start_date'] = df_raw['started_at'].dt.date
    df_raw['end_date'] = df_raw['ended_at'].dt.date

    # Calculate the number of trips out from a station on a given date
    df_out = df_raw.groupby(['start_station_id', 'start_date']).agg('count')
    df_out = df_out[['started_at']]
    df_out.columns = ['Number_of_trips_out']

    # Calculate the number of trips out from a station on a given date
    df_in = df_raw.groupby(['end_station_id', 'end_date']).agg('count')
    df_in = df_in[['started_at']]
    df_in.columns = ['Number_of_trips_in']

    # Merge the two datasets
    df_all = df_in.merge(df_out, left_index=True, right_on=['start_station_id', 'start_date'])

    df_all.reset_index(inplace=True)
    df_all.columns = [['Station_Id', 'Date', 'Trips_in', 'Trips_out']]
    df_all.columns = [name[0] for name in df_all.columns]
    df_all['In_Out'] = df_all['Trips_in'] - df_all['Trips_out']

    # Convert the Date column back to datetime
    df_all['Date'] = pd.to_datetime(df_all['Date'])

    return df_all

def get_date_feature(cleaned_df):
    '''
    Function to get the day of week and month number from the cleaned data
    '''
    cleaned_df['day_of_week'] = cleaned_df['Date'].dt.dayofweek
    cleaned_df['Month'] = cleaned_df['Date'].dt.month

    return cleaned_df

def imput_missing_data(df_all):
    '''
    Make a dataframe as imput for the months that lacking data
    Input:
    - The dataframe that have values to get from
    '''
    df_12 = df_all[(df_all['Date'] >= '2020-12-30') & (df_all['Date'] <= '2021-02-26')]
    df_12['Date_new'] = df_12['Date'] - timedelta(days=364)
    df_12 = df_12.drop(columns=['Date'])
    df_12 = df_12.rename({'Date_new':'Date'}, axis=1)
    df_12['Month'] = df_12['Date'].dt.month
    return df_12


def merge_imput(df, df_imput):
    '''
    Merge the cleaned data with the imput dataframe
    Return a clean dataframe without any month mising
    '''
    return pd.concat([df, df_imput])

def station_info(df):
    '''
    Function to get info for each station.
    This is used to for the map after the model have return some prediction
    '''
    station = df.groupby('start_station_id').agg({'start_station_latitude':[('lat', 'first')],
                                             'start_station_longitude':[('lon', 'first')],
                                             'start_station_name':[('name', 'first')],
                                             'start_station_description':[('description', 'first')]})
    station = station.droplevel(level=0, axis=1)
    return station.reset_index()

def get_all_unique_station(df_cleaned):
    '''
    Function to turn the cleaned dataframe in to a dictionary with
    '''
    df_dict = {}
    for station in df_cleaned['Station_Id'].unique():
        df_station = df_cleaned[df_cleaned['Station_Id'] == station]
        df_station.set_index('Date', inplace=True)
        df_station = df_station.drop(columns='Station_Id')
        df_dict["{}".format(station)] = df_station
    return df_dict

def clean_weather_data(weather_file_path):
    df = pd.read_csv(weather_file_path)
    df['dt_iso'] = df['dt_iso'].apply(lambda x: x.split(' ')[0])
    df_grouped_by_day = pd.DataFrame(df.groupby('dt_iso').agg({'temp_min':'min',
                                                           'temp_max':'max',
                                                           'wind_speed':'mean',
                                                           'rain_1h':'sum',
                                                           'snow_1h':'sum'}))
    historic_weather_df = df_grouped_by_day.reset_index()
    historic_weather_df = historic_weather_df.rename({'dt_iso':'date',
                                                  'wind_speed':'wind_speed_avg',
                                                  'rain_1h':'rainfall_total',
                                                  'snow_1h':'snow_total'}, axis=1)
    return historic_weather_df

def merge_weather(df_bike, df_weather):
    df_bike['temp_min'] = df_bike['Date'].map(df_weather.set_index('Date')['temp_min'])
    df_bike['temp_max'] = df_bike['Date'].map(df_weather.set_index('Date')['temp_max'])
    df_bike['wind_speed_avg'] = df_bike['Date'].map(df_weather.set_index('Date')['wind_speed_avg'])
    df_bike['rainfall_total'] = df_bike['Date'].map(df_weather.set_index('Date')['rainfall_total'])
    df_bike['snow_total'] = df_bike['Date'].map(df_weather.set_index('Date')['snow_total'])
    return df_bike
