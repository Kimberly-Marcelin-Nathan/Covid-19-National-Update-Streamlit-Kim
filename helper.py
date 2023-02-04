import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static
import json
import urllib
import numpy as np
from folium.plugins import HeatMap
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime


def get_data_1():
    url = 'https://api.covid19india.org/csv/latest/state_wise_daily.csv'
    urllib.request.urlretrieve(url, 'data1.csv')
    df1 = pd.read_csv('data1.csv', parse_dates=['Date'])
    columns = ['Date', 'Status', 'Total', 'Andaman and Nicobar Islands', 'Andhra Pradesh',
               'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
               'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi', 'Goa', 'Gujarat',
               'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand',
               'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra',
               'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry',
               'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
               'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
    df1.drop(['Date_YMD', 'UN'], axis=1, inplace=True)
    df1.columns = columns
    df1_ = df1.drop(['Date', 'Status'], axis=1)
    df1_ = np.abs(df1_)
    df1[df1_.columns] = df1_
    df1['Dadra and Nagar Haveli and Daman and Diu'] = df1['Dadra and Nagar Haveli'] + \
        df1['Daman and Diu']
    df1 = df1.drop(['Dadra and Nagar Haveli', 'Daman and Diu'], axis=1)
    return df1


def get_date(df):
    t = df.tail(1)['Date'].tolist()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    return f'Last Updated : {str(months[t.month - 1])} {str(t.day)} , {str(t.year)}'


def ready_map_data_tot(df):
    t = df.copy()
    t = t.drop('Date', axis=1)
    t = t.T
    cols = t.loc['Status']
    t = t[2:]
    t.columns = cols
    t = t.groupby(by=t.columns, axis=1).sum()
    t = t.reset_index()
    t.columns = ['State', 'Confirmed', 'Deceased', 'Recovered']
    tt = pd.read_csv('covid_cases_india.csv')
    state_ids = {}
    for i in range(len(tt)):
        state_ids[tt.iloc[i]['st_nm']] = tt.iloc[i]['state_code']
    t['State ID'] = t['State'].apply(
        lambda x: state_ids[x] if x in state_ids else 0)
    t = t[['State ID', 'State', 'Confirmed', 'Recovered', 'Deceased']]
    t = t.sort_values('State ID')
    t = t.reset_index(drop=True)
    return t


def ready_map_data_daily(df):
    t = df.copy()
    t = t.tail(3)
    t = t.T
    cols = t.loc['Status'].tolist()
    t = t.reset_index()
    t.columns = ['State'] + cols
    c = t.iloc[2][1]
    r = t.iloc[2][2]
    d = t.iloc[2][3]
    t = t[3:]
    t['Confirmed%'] = t['Confirmed'] / c * 100
    t['Recovered%'] = t['Recovered'] / r * 100
    t['Deceased%'] = t['Deceased'] / d * 100
    tt = pd.read_csv('covid_cases_india.csv')
    states = {}
    for i in range(len(tt)):
        states[tt.iloc[i]['st_nm']] = tt.iloc[i]['state_code']
    t['State ID'] = t['State'].apply(lambda x: states[x] if x in states else 0)
    t = t[['State ID', 'State', 'Confirmed', 'Confirmed%',
           'Recovered', 'Recovered%', 'Deceased', 'Deceased%']]
    t = t.sort_values('State ID')
    t = t.reset_index(drop=True)
    return t


def get_map(t, ch):
    json1 = f"states_india.geojson"
    m = folium.Map(location=[23.47, 82.5],
                   tiles='CartoDB dark_matter', zoom_start=5, min_zoom=4, max_zoom=7)
    india_covid_data = t.copy()
    folium.Choropleth(
        geo_data=json1,
        name="choropleth",
        data=india_covid_data,
        columns=["State ID", ch],
        key_on="feature.properties.state_code",
        fill_color="YlOrRd",
        fill_opacity=0.8,
        line_opacity=0.2,
        highlight=True,
        legend_name=ch+' Cases Today'
    ).geojson.add_child(
        folium.features.GeoJsonTooltip(['st_nm'], labels=False)
    ).add_to(m)
    return m


def count_plot_total(df):
    df = df.groupby('Status')[['Total']].sum()
    df = df.reset_index()
    return px.bar(df, x='Status', y='Total', color='Status', color_discrete_sequence=['#43bccd','#ea3546','#662e9b'])


def pie_chart_total(df):
    df = df.groupby('Status')[['Total']].sum()
    df = df.reset_index()
    return px.pie(data_frame=df, values='Total', names='Status', hole=0.5, color_discrete_sequence=['#43bccd','#ea3546','#662e9b'])


def area_scatter(df):
    fig1 = px.area(df, x='Date', y='Total', color='Status',
                   color_discrete_sequence=['#43bccd','#ea3546','#662e9b'])
    fig2 = px.scatter(df, x='Date', y='Total', color='Status', size='Total',
                      color_discrete_sequence=['#43bccd','#ea3546','#662e9b'])
    return fig1, fig2


def violin_plot_tot(df):
    date_state = df.copy()
    date_state = date_state[['Status', 'Total']]
    x1 = date_state[date_state['Status'] == 'Confirmed']['Total'].tolist()
    x2 = date_state[date_state['Status'] == 'Recovered']['Total'].tolist()
    x3 = date_state[date_state['Status'] == 'Deceased']['Total'].tolist()
    fig = go.Figure()
    fig.add_trace(go.Violin(y=x1, points='all',
                            box_visible=True, name='Confirmed', line_color='#43bccd'))
    fig.add_trace(go.Violin(y=x2, points='all',
                            box_visible=True, name='Recovered', line_color='#662e9b'))
    fig.add_trace(go.Violin(y=x3, points='all',
                            box_visible=True, name='Deceased', line_color='#ea3546'))
    return fig


def get_st(df):
    t = df.copy()
    t = t.T
    cols = t.loc['Status'].tolist()
    t = t[3:]
    t.columns = cols
    t = t.groupby(by=t.columns, axis=1).sum()
    t1 = t.sort_values(['Confirmed'], ascending=False)
    t2 = t.sort_values(['Recovered'], ascending=False)
    t3 = t.sort_values(['Deceased'], ascending=False)
    t1 = t1.head()[['Confirmed']]
    t2 = t2.head()[['Recovered']]
    t3 = t3.head()[['Deceased']]
    t1 = t1.reset_index()
    t2 = t2.reset_index()
    t3 = t3.reset_index()
    t1.columns = ['State', 'Count']
    t2.columns = ['State', 'Count']
    t3.columns = ['State', 'Count']
    fig = make_subplots(rows=1, cols=3)
    fig.add_trace(
        go.Bar(x=t1.State, y=t1.Count, name='Confirmed',
               textangle=0, marker_color='#43bccd'),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(x=t2.State, y=t2.Count, name='Recovered', marker_color='#662e9b'),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(x=t3.State, y=t3.Count, name='Deceased', marker_color='#ea3546'),
        row=1, col=3
    )
    fig.update_layout(title_text='T O P   5   S T A T E S', title_x=0.5, font=dict(
        family="Courier New, monospace",
        size=15,
        color='white'
    ))
    return fig


def pplott(df1, states, ch):
    st = states.loc[ch]
    x = ['Confirmed', 'Deceased', 'Recovered']
    f1 = px.bar(st, x=x, y=st.tolist(), color=x, color_discrete_sequence=[
                '#43bccd','#ea3546','#662e9b'])
    f2 = px.pie(st, names=x, values=st.tolist(), color_discrete_sequence=[
                '#43bccd','#ea3546','#662e9b'])
    date_state = df1.copy()
    date_state = date_state[['Status', ch]]
    x1 = date_state[date_state['Status'] == 'Confirmed'][ch].tolist()
    x2 = date_state[date_state['Status'] == 'Recovered'][ch].tolist()
    x3 = date_state[date_state['Status'] == 'Deceased'][ch].tolist()
    f3 = go.Figure()
    f3.add_trace(go.Violin(y=x1, points='all',
                           box_visible=True, name='Confirmed', marker_color='#43bccd'))
    f3.add_trace(go.Violin(y=x2, points='all',
                           box_visible=True, name='Recovered', marker_color='#662e9b'))
    f3.add_trace(go.Violin(y=x3, points='all',
                           box_visible=True, name='Deceased', marker_color='#ea3546'))
    dt = df1[['Date', 'Status', ch]]
    f4 = px.area(dt, x='Date', y=ch, color='Status',
                 color_discrete_sequence=['#43bccd','#ea3546','#662e9b'])
    return f1, f2, f3, f4


def pplott1(states, ch):
    st = states.loc[ch]
    x = ['Confirmed', 'Recovered', 'Deceased']
    if st.tolist()[0] == 0 and st.tolist()[1] == 0 and st.tolist()[2] == 0:
        return 0, 0
    f1 = px.bar(st, x=x, y=st.tolist(), color=x, color_discrete_sequence=[
               '#43bccd','#ea3546','#662e9b'])
    f2 = px.pie(st, names=x, values=st.tolist(), color_discrete_sequence=[
                '#43bccd','#ea3546','#662e9b'])
    return f1, f2
