from helper import *


st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
    layout="wide", page_title='COVID-19 | NATIONAL', page_icon='red.png')


df = get_data_1()

date_ = get_date(df)

st.markdown("<h1 style='text-align: center; letter-spacing:12px;font-size: 65px; color: #ffffff;'>COVID 19 NATIONAL UPDATES</h1>", unsafe_allow_html=True)


st.text('')
st.text('')
st.text('')
st.text('')

c1, c2, c3 = st.columns(3)
tot = df.groupby('Status')[['Total']].sum().values.flatten().tolist()

with c1:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{tot[0]}</span><br><br><span>CONFIRMED CASES</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')
    st.text('')

with c2:
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:10px;font-size: 28px; color: #ffffff;'>- OVERALL -</h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{tot[2]}</span><br><br><span>RECOVERED CASES</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')
    st.text('')

with c3:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{tot[1]}</span><br><br><span>DECEASED CASES</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')
    st.text('')

c11, c22, c33 = st.columns(3)
sr = df.copy()
sr = sr.tail(3)
sr = sr.T
tt1 = sr.loc['Total'].tolist()[0]
tt2 = sr.loc['Total'].tolist()[1]
tt3 = sr.loc['Total'].tolist()[2]

with c11:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{str(tt1)}</span><br><br><span>CONFIRMED CASES</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')
    st.text('')

with c22:
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:10px;font-size: 28px; color: #ffffff;'>- {date_.split(':')[1].strip().upper()} -</h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{str(tt2)}</span><br><br><span>RECOVERED CASES</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')
    st.text('')

with c33:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{str(tt3)}</span><br><br><span>DECEASED CASES</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')
    st.text('')

ch = None

cc1, cc2, cc3 = st.columns(3)
with cc2:
    st.text('')
    st.text('')
    ch = st.selectbox('CHOOSE CASES CATEGORY', [
        'Confirmed', 'Recovered', 'Deceased'])
    st.text('')
    st.text('')

col1, col2 = st.columns(2)

with col1:
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:10px;font-size: 18px; color: #ffffff;'>TOTAL CASES</h5>", unsafe_allow_html=True)
    st.text('')
    df_map = ready_map_data_tot(df)
    m = get_map(df_map, ch)
    folium_static(m, width=680, height=810)

with col2:
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:10px;font-size: 18px; color: #ffffff;'>CASES ON {date_.split(':')[1].strip().upper()}</h5>", unsafe_allow_html=True)
    st.text('')
    df_map = ready_map_data_daily(df)
    m = get_map(df_map, ch)
    folium_static(m, width=680, height=810)


col3, col4 = st.columns(2)
fig1, fig2 = area_scatter(df)

with col3:
    total_bar = count_plot_total(df)
    st.plotly_chart(total_bar, use_container_width=True)
    st.plotly_chart(fig1, use_container_width=True)

with col4:
    total_pie = pie_chart_total(df)
    st.plotly_chart(total_pie, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)

p = violin_plot_tot(df)
st.plotly_chart(p, use_container_width=True)

plot = get_st(df)
st.plotly_chart(plot, use_container_width=True)

st.text('')
st.text('')

c4, c5, c6 = st.columns(3)

state_ch = None

states = df.copy()
states = states.T
cols = states.loc['Status'].tolist()
states = states[3:]
states.columns = cols
states = states.groupby(by=states.columns, axis=1).sum()

states_recent = df.copy()
states_recent = states_recent.tail(3)
states_recent = states_recent.T
cols = states_recent.loc['Status'].tolist()
states_recent = states_recent[3:]
states_recent.columns = cols

with c5:
    state_ch = st.selectbox('CHOOSE STATE', states.index.tolist())
    st.text('')

st.text('')
st.text('')
st.text('')

c7, c8, c9 = st.columns(3)

with c7:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{str(int(states.loc[state_ch]['Confirmed']))}</span><br><br><span>CONFIRMED CASES</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')

with c8:
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:10px;font-size: 28px; color: #ffffff;'>- OVERALL -</h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{str(int(states.loc[state_ch]['Recovered']))}</span><br><br><span>RECOVERED CASES</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')

with c9:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{str(int(states.loc[state_ch]['Deceased']))}</span><br><br><span>DECEASED CASES</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')

st.text('')
st.text('')

f1, f2, f3, f4 = pplott(df, states, state_ch)

c10, c11, c12, c13 = st.columns([1, 2, 2, 1])

with c11:
    st.plotly_chart(f1, use_container_width=True)

with c12:
    st.plotly_chart(f2, use_container_width=True)

c14, c15 = st.columns(2)

with c14:
    st.plotly_chart(f3, use_container_width=True)

with c15:
    st.plotly_chart(f4, use_container_width=True)


c71, c81, c91 = st.columns(3)

with c71:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{str(int(states_recent.loc[state_ch]['Confirmed']))}</span><br><br><span>CONFIRMED CASES</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')

with c81:
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:10px;font-size: 28px; color: #ffffff;'>- {date_.split(':')[1].strip().upper()} -</h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{str(int(states_recent.loc[state_ch]['Recovered']))}</span><br><br><span>RECOVERED CASES</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')

with c91:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown(
        f"<h5 style='text-align: center; letter-spacing:2px;font-size: 22px; color: #888;'><span style='font-size: 40px;'>{str(int(states_recent.loc[state_ch]['Deceased']))}</span><br><br><span>DECEASED CASES</span></h5>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')


f11, f21 = pplott1(states_recent, state_ch)

if f11 != 0 and f21 != 0:
    c111, c121 = st.columns(2)

    with c111:
        st.plotly_chart(f11, use_container_width=True)

    with c121:
        st.plotly_chart(f21, use_container_width=True)
