import streamlit as st
import pandas as pd
import requests
import datetime
from streamlit_folium import st_folium
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster

st.set_page_config(layout='wide')

'''
# Oslo City Bike
'''

st.markdown('**Welcome to prediction!**')

with st.form(key='params_for_api'):

    date_to_predict = st.date_input('Please enter a date', value=datetime.datetime(2022, 12, 2))
    bt1 = st.form_submit_button('Make prediction')

date_to_pick = date_to_predict.strftime("%Y-%m-%d")

url = 'http://localhost:8000/predict'

temp = requests.post(url,files={'date':date_to_pick})

st.write(temp.content.decode())
df_correct_date =temp.content.decode()
df = pd.read_csv(f'gs://sweet_bucket/dump_pred/{df_correct_date[1:-1]}.csv')
df.columns = ['Unnamed: 0','Station_Id', 'In_Out']

# detail expander
station_info = pd.read_csv('gs://sweet_bucket/station_info.csv')
details_df = df.merge(station_info, left_on='Station_Id', right_on='start_station_id')
details_df = details_df.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y', 'start_station_id'])
details_df = details_df.set_index('Station_Id')
details_df = details_df.iloc[:, [3,0,4,1,2]]
details_df = details_df.rename({'name':'Station', 'In_Out': 'predicted delta', 'description':'Station description'}, axis='columns')

with st.expander('Details'):
    st.dataframe(details_df)

# mapping
df_to_map = station_info.merge(df, left_on='start_station_id', right_on='Station_Id')

m = folium.Map(width=500, height=800,location=[59.918569964063536, 10.750777377179256], zoom_start=15)

for i in range(len(df_to_map)):
        if df_to_map['In_Out'][i] < 0:
            folium.CircleMarker(location=[df_to_map['lat'][i], df_to_map['lon'][i]],
                        popup=df_to_map['name'][i], tooltip=df_to_map['name'][i],
                        radius=int(df_to_map['In_Out'][i]*(-1)),
                        color='red', fill=True, fill_color='red').add_to(m)
        elif df_to_map['In_Out'][i] == 0:
            folium.Circle(location=[df_to_map['lat'][i], df_to_map['lon'][i]],
                        popup=df_to_map['name'][i], tooltip=df_to_map['name'][i],
                        radius=int(df_to_map['In_Out'][i]*(-1)),
                        color='gray', fill=True, fill_color='gray').add_to(m)
        else:
            folium.CircleMarker(location=[df_to_map['lat'][i], df_to_map['lon'][i]],
                        popup=df_to_map['name'][i], tooltip=df_to_map['name'][i],
                        radius=int(df_to_map['In_Out'][i]),
                        color='blue', fill=True, fill_color='green').add_to(m)

st_data = st_folium(m, width=1500)
