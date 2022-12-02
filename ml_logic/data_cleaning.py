import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date, timezone
import glob

def clean_data(folder_path):
    '''
    Function to clean data from raw files
    '''
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
    df_all['Out_Inn'] = df_all['Trips_out'] - df_all['Trips_in']

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

def get_imput(df, month_list):
    '''
    Make a dataframe as imput for the months that lacking data
    Input:
    - The dataframe that have values to calculate average from
    - List of months that need to be imputed
    '''
    df_12 = df[df['Month'].isin(month_list)]
    df_12['Day'] = df_12['Date'].dt.day
    df_imput = df_12.groupby(['Station_Id', 'Month', 'Day']).agg('mean')
    df_imput.reset_index(inplace=True)
    df_imput[['Trips_in','Trips_out']] = df_imput[['Trips_in','Trips_out']].apply(pd.Series.round)
    df_imput['Out_Inn'] = df_imput['Trips_out'] - df_imput['Trips_in']
    df_imput['Year'] = '2020'
    df_imput['Date'] = pd.to_datetime(df_imput[['Day','Month','Year']])
    df_imput['day_of_week'] = df_imput['Date'].dt.dayofweek

    return df_imput[['Station_Id', 'Date', 'Trips_in', 'Trips_out', 'Out_Inn', 'day_of_week',
       'Month']]


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
    return station.droplevel(level=0, axis=1)
