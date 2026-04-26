import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ── Page setting ──────────────────────────────
st.set_page_config(
    page_title="AC Unit Performance Dashboard By Nils Liu",
    page_icon="❄️",
    layout="wide"
)

# ── Load Data ──────────────────────────────────
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Nils0217/Air-Conditioner-performance-analysis/refs/heads/main/Cleaned%20dataset%20ready%20for%20analysis/Goa_A200_AC_unit_performance_clean.csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.lower().str.strip()
    df['time_stamp'] = pd.to_datetime(df['time_stamp'])
    df['hour'] = df['time_stamp'].dt.hour
    df['month'] = df['time_stamp'].dt.month
    df['season'] = np.select(
        [df['month'].isin([3,4,5]), df['month'].isin([6,7,8,9])],
        ['dry_hot', 'rainy'],
        default='cool'
    )
    df['load_state'] = np.select(
        [df['current'] < 5, df['current'] < 22, df['current'] < 25],
        ['standby', 'normal', 'high_load'],
        default='overload'
    )
    df = df[df['current_flag'] != 'sensor_error']
    return df

df = load_data()


# ── Page Title ──────────────────────────────────
st.title("AC Unit Performance Dashboard")
st.markdown("**Facility:** Room A200, Goa, India | **Period:** Mar 2020 - Aug 2021 | Analyze by Chen Yu Liu (Nils)")

# ── Sidebar Filter ─────────────────────────────
st.sidebar.header("Filters")

selected_units = st.sidebar.multiselect(
    "Select AC Unit",
    options=df['device_id'].unique(),
    default=df['device_id'].unique()
)

selected_seasons = st.sidebar.multiselect(
    "Select Season",
    options=['cool', 'dry_hot', 'rainy'],
    default=['cool', 'dry_hot', 'rainy']
)

# ── Apply Filter ───────────────────────────────────
filtered_df = df[
    (df['device_id'].isin(selected_units)) &
    (df['season'].isin(selected_seasons))
]


# ── Section Header ─────────────────────────────
st.header("Environmental Correlation")

# Consistent color mapping across all charts
color_map = {
    'A200AC01': '#4C72B0',  # muted blue
    'A200AC02': '#DD8452',  # muted orange
    'A200AC03': '#55A868'   # muted green
}

# ── Chart 1: External Temp vs Current ──────────
col1, col2 = st.columns(2)

# ── Chart 1: External Temp vs Current (Box Plot) ──
with col1:
    st.subheader("External Temp vs Current")
    plot_df1 = filtered_df[filtered_df['load_state'].isin(['normal','high_load'])].copy()
    plot_df1['temp_bin_num'] = (plot_df1['external_temp'] // 2 * 2).astype(int)
    plot_df1['temp_bin'] = plot_df1['temp_bin_num'].astype(str) + '°C'
    fig1 = px.box(
        plot_df1,
        x='temp_bin', y='current',
        color='device_id',
        color_discrete_map=color_map,
        category_orders={'temp_bin': sorted(plot_df1['temp_bin'].unique(), key=lambda x: int(x.replace('°C', '')))},
        labels={'temp_bin': 'External Temp Range', 'current': 'Current (A)'},
        title="Current Distribution by External Temperature"
    )
    fig1.update_traces(marker_line_width=0.5)
    st.plotly_chart(fig1, use_container_width=True)

# ── Chart 2: Humidity vs Power Factor (Box Plot) ──
with col2:
    st.subheader("Humidity vs Power Factor")
    plot_df2 = filtered_df[filtered_df['load_state'].isin(['normal','high_load'])].copy()
    plot_df2['humidity_bin'] = (plot_df2['humidity'] // 5 * 5).astype(int)
    hum_avg = plot_df2.groupby(['humidity_bin','device_id'])['power_factor'].mean().reset_index()
    fig2 = px.line(
        hum_avg,
        x='humidity_bin', y='power_factor',
        color='device_id',
        color_discrete_map=color_map,
        labels={'humidity_bin': 'Humidity (%)', 'power_factor': 'Avg Power Factor'},
        title="Avg Power Factor by Humidity Level"
    )
    fig2.update_traces(line_width=2)
    st.plotly_chart(fig2, use_container_width=True)

# Divider
st.markdown("---")

col3, col4 = st.columns(2)

# ── Chart 3: Avg Current by Season ─────────────
with col3:
    st.subheader("Avg Current by Season")
    season_avg = filtered_df[
        filtered_df['load_state'].isin(['normal','high_load'])
    ].groupby(['season','device_id'])['current'].mean().reset_index()
    fig3 = px.bar(
        season_avg,
        x='season', y='current',
        color='device_id',
        color_discrete_map=color_map,
        barmode='group',
        labels={'current': 'Avg Current (A)', 'season': 'Season'},
        title="Average Current by Season and Unit"
    )
    fig3.update_traces(marker_line_width=1, marker_line_color='Black')
    st.plotly_chart(fig3, use_container_width=True)

# ── Chart 4: Room Temp vs Current (Line) ───────
# Chart 4: Room Temp Box Plot
with col4:
    st.subheader("Room Temp vs Current")
    plot_df4 = filtered_df[filtered_df['load_state'].isin(['normal','high_load'])].copy()
    plot_df4['temp_bin_num'] = (plot_df4['room_temp'] // 3 * 3).astype(int)
    plot_df4['temp_bin'] = plot_df4['temp_bin_num'].astype(str) + '°C'
    fig4 = px.box(
        plot_df4,
        x='temp_bin', y='current',
        color='device_id',
        color_discrete_map=color_map,
        category_orders={'temp_bin': sorted(plot_df4['temp_bin'].unique(), key=lambda x: int(x.replace('°C','')))},
        labels={'temp_bin': 'Room Temp Range', 'current': 'Current (A)'},
        title="Current Distribution by Room Temperature"
    )
    fig4.update_traces(marker_line_width=0.5)
    st.plotly_chart(fig4, use_container_width=True)


# ── Page 4: Electricity Cost Analysis ──────────
st.markdown("---")
st.header("Electricity Cost Analysis")

# ToU tariff setup
INTERVAL_HOURS = 2 / 60
tariff_rates = {'peak': 8.50, 'off_peak': 6.00, 'night': 4.00}

def get_tariff_period(hour):
    if 9 <= hour < 18:    return 'peak'
    elif 18 <= hour < 22: return 'off_peak'
    else:                 return 'night'

# Apply tariff to filtered data
cost_df = filtered_df.copy()
cost_df['tariff_period'] = cost_df['hour'].apply(get_tariff_period)
cost_df['rate_per_kwh']  = cost_df['tariff_period'].map(tariff_rates)
cost_df['kwh_estimated'] = (cost_df['real_power'] / 1000) * INTERVAL_HOURS
cost_df['cost_inr']      = cost_df['kwh_estimated'] * cost_df['rate_per_kwh']

col1, col2 = st.columns(2)

# ── Chart 1: Best vs Worst Cost ─────────────────
with col1:
    st.subheader("Best vs Worst Case Cost")
    best  = cost_df[cost_df['load_state'] == 'normal'].groupby('device_id')['cost_inr'].sum()
    worst = cost_df[cost_df['load_state'].isin(['high_load','overload'])].groupby('device_id')['cost_inr'].sum()
    cost_compare = pd.DataFrame({
        'best_case_INR' : best,
        'worst_case_INR': worst
    }).reset_index()
    cost_melted = cost_compare.melt(
        id_vars='device_id',
        value_vars=['best_case_INR','worst_case_INR'],
        var_name='scenario', value_name='cost_INR'
    )
    fig5 = px.bar(
        cost_melted,
        x='device_id', y='cost_INR',
        color='scenario',
        barmode='group',
        color_discrete_map={
            'best_case_INR' : '#2196F3',
            'worst_case_INR': '#F44336'
        },
        labels={'cost_INR': 'Total Cost (INR)', 'device_id': 'Device'},
        title="Best vs Worst Case Electricity Cost by Unit"
    )
    fig5.update_traces(marker_line_width=1, marker_line_color='Black')
    st.plotly_chart(fig5, use_container_width=True)

# ── Chart 2: Cost by Tariff Period ─────────────
with col2:
    st.subheader("Cost by Tariff Period")
    period_cost = cost_df.groupby(['device_id','tariff_period'])['cost_inr'].sum().reset_index()
    fig6 = px.bar(
        period_cost,
        x='device_id', y='cost_inr',
        color='tariff_period',
        barmode='stack',
        color_discrete_map={
            'peak'    : '#F44336',
            'off_peak': '#FF9800',
            'night'   : '#3F51B5'
        },
        labels={'cost_inr': 'Total Cost (INR)', 'device_id': 'Device'},
        title="Electricity Cost by Tariff Period"
    )
    fig6.update_traces(marker_line_width=1, marker_line_color='Black')
    st.plotly_chart(fig6, use_container_width=True)