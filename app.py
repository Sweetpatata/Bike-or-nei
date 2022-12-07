import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from streamlit_folium import st_folium
import folium
import json
from branca.element import Template, MacroElement

st.set_page_config(layout='wide')
#st.image('/Users/frederickjohannson''/Desktop/bike_black.jpg')

#background image
def add_bg_from_url():
   st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://storage.googleapis.com/sweet_bucket/pexels-madison-inouye-1831234.jpg");
            background-attachment: fixed;
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_url()

# tab interface
#tab1, tab2 = st.tabs(['Prediction', 'Data'])

#with tab1:

'''
# Oslo City Bike - Maintenance Forecast
'''

st.markdown('**Predict bicycle station usage**')

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
    details_df = st.session_state['df'].merge(station_info, left_on='Station_Id', right_on='start_station_id')
    details_df = details_df.drop(columns=['Unnamed: 0', 'start_station_id'])
    details_df = details_df.set_index('Station_Id')
    details_df = details_df.iloc[:, [3,0,4,1,2]]
    details_df = details_df.rename({'name':'Station', 'In_Out': 'predicted flow: bikes per day', 'description':'Station description'}, axis='columns')
    details_df['predicted flow: bikes per day'] = details_df['predicted delta'].astype(int)

    with st.expander('Details'):
        st.dataframe(details_df)

    #mapping
    df_to_map = station_info.merge(st.session_state['df'], left_on='start_station_id', right_on='Station_Id')

    m = folium.Map(width=500, height=800,location=[59.918569964063536, 10.750777377179256], zoom_start=13)

    for i in range(len(df_to_map)):
            if df_to_map['In_Out'][i] < -5:
                folium.CircleMarker(location=[df_to_map['lat'][i], df_to_map['lon'][i]],
                                    tooltip="{}: {} bikes per day".format(df_to_map['name'][i], int(df_to_map['In_Out'][i])),
                            radius=int(df_to_map['In_Out'][i]*(-1)),
                            color='red', fill=True, fill_color='red').add_to(m)
            elif df_to_map['In_Out'][i] > -5 and df_to_map['In_Out'][i] < 5:
                folium.Circle(location=[df_to_map['lat'][i], df_to_map['lon'][i]],
                            tooltip="{}: {} bikes per day".format(df_to_map['name'][i], int(df_to_map['In_Out'][i])),
                            color='gray', fill=True, fill_color='gray').add_to(m)
            else:
                folium.CircleMarker(location=[df_to_map['lat'][i], df_to_map['lon'][i]],
                            tooltip="{}: {} bikes per day".format(df_to_map['name'][i], int(df_to_map['In_Out'][i])),
                            radius=int(df_to_map['In_Out'][i]),
                            color='blue', fill=True, fill_color='blue').add_to(m)

#legend and map builder
    template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>jQuery UI Draggable - Default functionality</title>
<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

<script src="https://code.jquery.com/jquery-1.12.4.js"></script>
<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>

</head>
<body>


<div id='maplegend' class='maplegend'
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
    border-radius:6px; padding: 10px; font-size:14px; right: 20px; top: 20px;'>

<div class='legend-title'></div>
<div class='legend-scale'>
<ul class='legend-labels'>
    <li><span style='background:red;opacity:0.7;'></span>replenish</li>
    <li><span style='background:gray;opacity:0.7;'></span>on par</li>
    <li><span style='background:blue;opacity:0.7;'></span>remove</li>

</ul>
</div>
</div>

</body>
</html>

<style type='text/css'>
.maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
.maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
.maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
.maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 5px;
    border: 1px solid #999;
    }
.maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
.maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

    macro = MacroElement()
    macro._template = Template(template)

    m.get_root().add_child(macro)

    st_data = st_folium(m, width=1500)

#with tab2:
#    st.dataframe(details_df)
