import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from streamlit_folium import st_folium
import folium
import json

st.set_page_config(layout='wide')

'''
# Oslo City Bike
'''

st.markdown('**Welcome to prediction!**')

today = datetime.today()
td = timedelta(days=5)
max_day = today + td

with st.form(key='params_for_api'):

    date_to_predict = st.date_input('Please enter a date', value=today, min_value=today, max_value=max_day)
    bt1 = st.form_submit_button('Make prediction')

date_to_pick = date_to_predict.strftime("%Y-%m-%d")

url = 'https://bike-hzg6p6d3ea-ew.a.run.app'
if bt1:
    temp = requests.post(url,files={'date':date_to_pick}).content.decode()
    json_object = json.loads(temp)
    df = pd.DataFrame(json_object)

    if 'df' not in st.session_state:
        st.session_state['df'] = df

### detail expander
station_info = pd.read_csv('gs://sweet_bucket/station_info.csv')
details_df = st.session_state['df'].merge(station_info, left_on='Station_Id', right_on='start_station_id')
details_df = details_df.drop(columns=['Unnamed: 0', 'start_station_id'])
details_df = details_df.set_index('Station_Id')
details_df = details_df.iloc[:, [3,0,4,1,2]]
details_df = details_df.rename({'name':'Station', 'In_Out': 'predicted delta', 'description':'Station description'}, axis='columns')

with st.expander('Details'):
    st.dataframe(details_df)


# mapping
df_to_map = station_info.merge(st.session_state['df'], left_on='start_station_id', right_on='Station_Id')

m = folium.Map(width=500, height=800,location=[59.918569964063536, 10.750777377179256], zoom_start=13)

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
