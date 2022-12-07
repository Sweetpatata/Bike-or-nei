import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from streamlit_folium import st_folium
import folium
import json

#from google.oauth2 import service_account

#credentials = service_account.Credentials.from_service_account_info(
#    st.secrets['gcp_service_account']
#)

#key = st.secrets.gcp_service_account.key

st.set_page_config(layout='wide')

'''
# Oslo City Bike
'''

st.markdown('**Welcome to prediction!**')

today = datetime.today()
td = timedelta(days=5)
max_day = today + td

with st.form(key='params_for_api'):

    date_to_predict = st.date_input('Please enter a date', value=datetime(2022,12,2))# min_value=today, max_value=max_day)
    bt1 = st.form_submit_button('Make prediction')

date_to_pick = date_to_predict.strftime("%Y-%m-%d")

#url = 'http://localhost:8000/predict'
url = 'https://bike2-hzg6p6d3ea-ew.a.run.app/predict'
if 'df' not in st.session_state:
        st.session_state['df'] = None

if bt1:
    temp = requests.post(url,files={'date':date_to_pick}).content.decode()
    json_object = json.loads(temp)
    df = pd.DataFrame(json_object)

    st.session_state['df'] = df

### detail expander
if st.session_state['df'] is not None:
    station_info = pd.read_csv('https://storage.googleapis.com/sweet_bucket/station_info.csv')
    #station_info = pd.read_csv('gs://sweet_bucket/station_info.csv')
    details_df = st.session_state['df'].merge(station_info, left_on='Station_Id', right_on='start_station_id')
    details_df = details_df.drop(columns=['Unnamed: 0', 'start_station_id'])
    details_df = details_df.set_index('Station_Id')
    details_df = details_df.iloc[:, [3,0,4,1,2]]
    details_df = details_df.rename({'name':'Station', 'In_Out': 'predicted delta', 'description':'Station description'}, axis='columns')

    with st.expander('Details'):
        st.dataframe(details_df)

    #station_info = pd.read_csv('gs://sweet_bucket/station_info.csv')

    #mapping
    df_to_map = station_info.merge(st.session_state['df'], left_on='start_station_id', right_on='Station_Id')

    m = folium.Map(width=500, height=800,location=[59.918569964063536, 10.750777377179256], zoom_start=13)

    for i in range(len(df_to_map)):
            if df_to_map['In_Out'][i] < -5:
                folium.CircleMarker(location=[df_to_map['lat'][i], df_to_map['lon'][i]],
                            popup=df_to_map['name'][i], tooltip=df_to_map['name'][i],
                            radius=int(df_to_map['In_Out'][i]*(-1)),
                            color='red', fill=True, fill_color='red').add_to(m)
            elif df_to_map['In_Out'][i] > -5 and df_to_map['In_Out'][i] < 5:
                folium.Circle(location=[df_to_map['lat'][i], df_to_map['lon'][i]],
                            popup=df_to_map['name'][i], tooltip=df_to_map['name'][i],
                            color='green', fill=True, fill_color='green').add_to(m)
            else:
                folium.CircleMarker(location=[df_to_map['lat'][i], df_to_map['lon'][i]],
                            popup=df_to_map['name'][i], tooltip=df_to_map['name'][i],
                            radius=int(df_to_map['In_Out'][i]),
                            color='yellow', fill=True, fill_color='yellow').add_to(m)

    st_data = st_folium(m, width=1500)
