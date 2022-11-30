import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_csv('/Users/frederickjohannson/code/Sweetpatata/bike-or-nei/raw_data/Oslo-historic-weather-data.csv')

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
print(historic_weather_df)
