import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta

st.set_page_config(
    page_title="6G Smart Factory - Manufacturing Health & Efficiency Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean UI Theme - Dark Only, No Glassmorphism, No Cyan
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ===== DARK ONLY THEME - FORCE DARK MODE ALWAYS ===== */

:root {
    --bg: #0f172a;
    --bg-card: #1e293b;
    --bg-hover: #334155;
    --border: #334155;
    --text: #f1f5f9;
    --text-muted: #94a3b8;
    --accent: #3b82f6;
    --accent-hover: #2563eb;
    --success: #22c55e;
    --warning: #f59e0b;
    --danger: #ef4444;
}

/* FORCE DARK: Override any light theme attempt */
html[data-theme="light"],
html[data-baseweb-theme="light"],
body[data-theme="light"],
.stApp[data-theme="light"] {
    --bg: #0f172a !important;
    --bg-card: #1e293b !important;
    --bg-hover: #334155 !important;
    --border: #334155 !important;
    --text: #f1f5f9 !important;
    --text-muted: #94a3b8 !important;
    --accent: #3b82f6 !important;
    --accent-hover: #2563eb !important;
    --success: #22c55e !important;
    --warning: #f59e0b !important;
    --danger: #ef4444 !important;
}

/* Global */
.stApp {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 95%;
}

/* Cards */
.glass-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    transition: all 0.2s ease;
}

.glass-card:hover {
    background: var(--bg-hover);
    border-color: var(--accent);
}

/* Metric Cards */
[data-testid="metric-container"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    transition: all 0.2s ease;
}

[data-testid="metric-container"]:hover {
    background: var(--bg-hover);
    border-color: var(--accent);
}

[data-testid="metric-container"] > div {
    color: var(--text) !important;
}

[data-testid="metric-container"] label {
    color: var(--text-muted) !important;
    font-weight: 500;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

section[data-testid="stSidebar"] .stSelectbox,
section[data-testid="stSidebar"] .stMultiSelect,
section[data-testid="stSidebar"] .stDateInput {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px;
    padding: 0.5rem;
}

section[data-testid="stSidebar"] label {
    color: var(--text-muted) !important;
    font-weight: 500;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.25rem;
    gap: 0.25rem;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 6px;
    color: var(--text-muted);
    font-weight: 500;
    font-size: 0.9rem;
    padding: 0.5rem 1rem;
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text);
    background: var(--bg-hover);
}

.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: #ffffff !important;
}

/* Dataframe */
.stDataFrame {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
}

.stDataFrame [data-testid="stTable"] {
    color: var(--text);
}

/* Plotly Charts */
.js-plotly-plot {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
}

/* Headers */
h1, h2, h3 {
    color: var(--text) !important;
    font-weight: 600;
    letter-spacing: -0.02em;
}

h1 {
    font-size: 2.25rem;
    font-weight: 700;
}

h2 {
    font-size: 1.5rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.75rem;
    margin-bottom: 1.5rem;
}

h3 {
    font-size: 1.125rem;
}

/* Buttons */
.stButton > button {
    background: var(--accent);
    color: #ffffff;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.625rem 1.5rem;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: var(--accent-hover);
    transform: translateY(-1px);
}

/* Expanders */
.streamlit-expanderHeader {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text);
    font-weight: 500;
}

.streamlit-expanderHeader:hover {
    background: var(--bg-hover);
    border-color: var(--accent);
}

.streamlit-expanderContent {
    background: var(--bg);
    border: 1px solid var(--border);
    border-top: none;
    border-radius: 0 0 8px 8px;
    color: var(--text);
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg);
}

::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-muted);
}

/* Markdown */
.stMarkdown {
    color: var(--text-muted);
}

.stMarkdown strong {
    color: var(--text);
}

/* Divider */
hr {
    border-color: var(--border) !important;
    margin: 2rem 0;
}

/* Selectbox */
[data-baseweb="select"] > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

[data-baseweb="popover"] [role="listbox"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

[role="option"] {
    color: var(--text) !important;
}

[role="option"]:hover {
    background: var(--bg-hover) !important;
}

[role="option"][aria-selected="true"] {
    background: var(--accent) !important;
    color: #ffffff !important;
}

/* Alerts */
.stSuccess {
    background: rgba(34, 197, 94, 0.1) !important;
    border: 1px solid var(--success) !important;
    border-radius: 8px !important;
    color: var(--success) !important;
}

.stWarning {
    background: rgba(245, 158, 11, 0.1) !important;
    border: 1px solid var(--warning) !important;
    border-radius: 8px !important;
    color: var(--warning) !important;
}

.stError {
    background: rgba(239, 68, 68, 0.1) !important;
    border: 1px solid var(--danger) !important;
    border-radius: 8px !important;
    color: var(--danger) !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: var(--accent) !important;
}

/* Multi-select tags */
[data-baseweb="tag"] {
    background: var(--accent) !important;
    color: #ffffff !important;
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "manufacturing_data.csv")
    df = pd.read_csv(csv_path)
    # Handle both 'Time' and 'Timestamp' column names
    time_col = 'Time' if 'Time' in df.columns else 'Timestamp'
    # Fast parsing: date is DD-MM-YYYY, time is HH:MM:SS
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df[time_col], format='%d-%m-%Y %H:%M:%S')
    df['Hour'] = df['Datetime'].dt.hour
    df['Shift'] = pd.cut(df['Hour'], bins=[0, 8, 16, 24], labels=['Night', 'Day', 'Evening'], right=False)
    return df

@st.cache_data
def load_kpis():
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "reports", "kpis.json")
    with open(json_path, "r") as f:
        return json.load(f)

@st.cache_data
def load_machine_health():
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "reports", "machine_health_analysis.csv")
    return pd.read_csv(csv_path)

@st.cache_data
def load_production():
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "reports", "production_performance.csv")
    return pd.read_csv(csv_path)

df = load_data()
kpis = load_kpis()
machine_health = load_machine_health()
production = load_production()

# Sidebar Filters
st.sidebar.title("🔧 Dashboard Controls")

machine_options = ['All'] + sorted(df['Machine_ID'].unique().tolist())
selected_machine = st.sidebar.selectbox("Select Machine", machine_options)

mode_options = ['All'] + sorted(df['Operation_Mode'].unique().tolist())
selected_mode = st.sidebar.selectbox("Operation Mode", mode_options)

date_range = st.sidebar.date_input(
    "Date Range",
    value=(df['Datetime'].min().date(), df['Datetime'].max().date()),
    min_value=df['Datetime'].min().date(),
    max_value=df['Datetime'].max().date()
)

metric_options = {
    'Temperature_C': 'Temperature (°C)',
    'Vibration_Hz': 'Vibration (Hz)',
    'Power_Consumption_kW': 'Power (kW)',
    'Network_Latency_ms': 'Network Latency (ms)',
    'Packet_Loss_%': 'Packet Loss (%)',
    'Quality_Control_Defect_Rate_%': 'Defect Rate (%)',
    'Production_Speed_units_per_hr': 'Production Speed (units/hr)',
    'Predictive_Maintenance_Score': 'Maintenance Score',
    'Error_Rate_%': 'Error Rate (%)'
}
selected_metrics = st.sidebar.multiselect(
    "Metrics to Compare",
    options=list(metric_options.keys()),
    default=['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW'],
    format_func=lambda x: metric_options[x]
)

# Apply filters
filtered_df = df.copy()
if selected_machine != 'All':
    filtered_df = filtered_df[filtered_df['Machine_ID'] == selected_machine]
if selected_mode != 'All':
    filtered_df = filtered_df[filtered_df['Operation_Mode'] == selected_mode]
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df['Datetime'].dt.date >= start_date) & 
        (filtered_df['Datetime'].dt.date <= end_date)
    ]

# Main Title
st.title("🏭 6G-Enabled Smart Factory: Manufacturing Process Health & Operational Efficiency")
st.markdown("**Thales Group** | Real-time IIoT Analytics Dashboard")

# Tabs for Dashboard Modules
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Factory Health Overview", 
    "🔧 Machine Health Dashboard", 
    "📈 Production & Quality Panel", 
    "⚡ Efficiency Diagnostics View"
])

# ============================================================
# TAB 1: FACTORY HEALTH OVERVIEW
# ============================================================
with tab1:
    st.header("Factory Health Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Health Index", f"{kpis['Machine_Health_Index']['overall_mean']:.1f}/100")
    with col2:
        st.metric("Avg Production Speed", f"{kpis['Average_Production_Speed']['overall_mean']:.0f} units/hr")
    with col3:
        st.metric("Avg Defect Rate", f"{df['Quality_Control_Defect_Rate_%'].mean():.2f}%")
    with col4:
        st.metric("Avg Error Rate", f"{df['Error_Rate_%'].mean():.2f}%")
    
    st.markdown("---")
    
    # Efficiency Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        eff_dist = filtered_df['Efficiency_Status'].value_counts()
        fig = px.pie(
            values=eff_dist.values, 
            names=eff_dist.index,
            title="Efficiency Distribution",
            color=eff_dist.index,
            color_discrete_map={'High': '#2ecc71', 'Medium': '#f39c12', 'Low': '#e74c3c'},
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Average sensor metrics by efficiency
        sensor_cols = ['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW', 
                       'Network_Latency_ms', 'Packet_Loss_%', 'Error_Rate_%']
        avg_by_eff = filtered_df.groupby('Efficiency_Status')[sensor_cols].mean().T
        fig = go.Figure()
        for eff in ['High', 'Medium', 'Low']:
            if eff in avg_by_eff.columns:
                fig.add_trace(go.Bar(
                    name=eff, 
                    x=avg_by_eff.index, 
                    y=avg_by_eff[eff],
                    marker_color={'High': '#2ecc71', 'Medium': '#f39c12', 'Low': '#e74c3c'}[eff]
                ))
        fig.update_layout(title="Average Sensor Metrics by Efficiency Status", barmode='group', height=400)
        st.plotly_chart(fig, width='stretch')
    
    # Time series of key metrics
    st.subheader("Key Metrics Trend")
    daily_avg = filtered_df.set_index('Datetime').resample('D')[['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW', 
                                                                  'Quality_Control_Defect_Rate_%', 'Error_Rate_%', 
                                                                  'Production_Speed_units_per_hr']].mean().reset_index()
    
    fig = make_subplots(rows=3, cols=2, subplot_titles=('Temperature', 'Vibration', 'Power', 'Defect Rate', 'Error Rate', 'Production Speed'))
    metrics = ['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW', 'Quality_Control_Defect_Rate_%', 'Error_Rate_%', 'Production_Speed_units_per_hr']
    for i, metric in enumerate(metrics):
        row = i // 2 + 1
        col = i % 2 + 1
        fig.add_trace(go.Scatter(x=daily_avg['Datetime'], y=daily_avg[metric], mode='lines', name=metric), row=row, col=col)
    fig.update_layout(height=600, showlegend=False, title_text="Daily Average Metrics Trend")
    st.plotly_chart(fig, width='stretch')

# ============================================================
# TAB 2: MACHINE HEALTH DASHBOARD
# ============================================================
with tab2:
    st.header("Machine Health Dashboard")
    
    # Machine Health Scorecards
    st.subheader("Machine Health Scorecards")
    
    # Calculate health metrics per machine
    health_scores = machine_health[['Machine_ID', 'Machine_Health_Index', 'Predictive_Maintenance_Score_mean',
                                     'Temperature_C_mean', 'Vibration_Hz_mean', 'Power_Consumption_kW_mean',
                                     'Quality_Control_Defect_Rate_%_mean', 'Error_Rate_%_mean']].copy()
    health_scores.columns = ['Machine_ID', 'Health_Index', 'Maintenance_Score', 'Avg_Temp', 'Avg_Vib', 'Avg_Power', 'Avg_Defect', 'Avg_Error']
    health_scores = health_scores.sort_values('Health_Index', ascending=False)
    
    # Color code health index
    def health_color(val):
        if val >= 70:
            return 'background-color: #1e7e34; color: white'
        elif val >= 40:
            return 'background-color: #fff3cd; color: #1a1a1a'
        else:
            return 'background-color: #f8d7da; color: #721c24'
    
    styled = health_scores.style.map(health_color, subset=['Health_Index']).format({
        'Health_Index': '{:.1f}', 'Maintenance_Score': '{:.1f}', 
        'Avg_Temp': '{:.1f}', 'Avg_Vib': '{:.1f}', 'Avg_Power': '{:.1f}',
        'Avg_Defect': '{:.2f}', 'Avg_Error': '{:.2f}'
    })
    st.dataframe(styled, width='stretch', height=400)
    
    st.markdown("---")
    
    # Machine-wise sensor trends
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sensor Trends by Machine")
        if selected_machine != 'All':
            machine_df = filtered_df[filtered_df['Machine_ID'] == selected_machine]
        else:
            machine_df = filtered_df
        
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                           subplot_titles=('Temperature (°C)', 'Vibration (Hz)', 'Power (kW)'))
        for i, metric in enumerate(['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW']):
            daily = machine_df.set_index('Datetime').resample('D')[metric].mean().reset_index()
            fig.add_trace(go.Scatter(x=daily['Datetime'], y=daily[metric], mode='lines+markers', name=metric), row=i+1, col=1)
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("Health Index Distribution")
        fig = px.histogram(machine_health, x='Machine_Health_Index', nbins=20,
                          title="Machine Health Index Distribution",
                          color_discrete_sequence=['#3498db'])
        fig.add_vline(x=machine_health['Machine_Health_Index'].mean(), line_dash="dash", line_color="red",
                     annotation_text="Mean")
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
        
        # Operation mode comparison
        st.subheader("Sensor Stability by Operation Mode")
        mode_std = filtered_df.groupby('Operation_Mode')[['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW']].std().reset_index()
        fig = px.bar(mode_std, x='Operation_Mode', y=['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW'],
                    title="Sensor Variability (Std Dev) by Operation Mode", barmode='group')
        fig.update_layout(height=350)
        st.plotly_chart(fig, width='stretch')

# ============================================================
# TAB 3: PRODUCTION & QUALITY PANEL
# ============================================================
with tab3:
    st.header("Production & Quality Panel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Production Speed vs Defect Rate")
        fig = px.scatter(
            filtered_df, 
            x='Production_Speed_units_per_hr', 
            y='Quality_Control_Defect_Rate_%',
            color='Efficiency_Status',
            facet_col='Operation_Mode' if selected_mode == 'All' else None,
            color_discrete_map={'High': '#2ecc71', 'Medium': '#f39c12', 'Low': '#e74c3c'},
            title='Production Speed vs Defect Rate by Operation Mode',
            trendline='ols',
            hover_data=['Machine_ID', 'Predictive_Maintenance_Score']
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("Error Frequency Visualization")
        error_by_machine_mode = filtered_df.groupby(['Machine_ID', 'Operation_Mode'])['Error_Rate_%'].mean().reset_index()
        fig = px.bar(
            error_by_machine_mode, 
            x='Machine_ID', 
            y='Error_Rate_%',
            color='Operation_Mode',
            title='Average Error Rate by Machine and Operation Mode',
            barmode='group'
        )
        fig.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig, width='stretch')
    
    # Production speed trends
    st.subheader("Production Speed Trends")
    speed_daily = filtered_df.set_index('Datetime').resample('D')['Production_Speed_units_per_hr'].mean().reset_index()
    fig = px.line(speed_daily, x='Datetime', y='Production_Speed_units_per_hr',
                 title='Daily Average Production Speed')
    fig.update_layout(height=350)
    st.plotly_chart(fig, width='stretch')
    
    # Defect rate by hour
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Defect Rate by Hour of Day")
        defect_by_hour = filtered_df.groupby('Hour')['Quality_Control_Defect_Rate_%'].mean().reset_index()
        fig = px.bar(defect_by_hour, x='Hour', y='Quality_Control_Defect_Rate_%',
                    title='Average Defect Rate by Hour')
        fig.update_layout(height=350)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("Error Rate by Hour of Day")
        error_by_hour = filtered_df.groupby('Hour')['Error_Rate_%'].mean().reset_index()
        fig = px.bar(error_by_hour, x='Hour', y='Error_Rate_%',
                    title='Average Error Rate by Hour')
        fig.update_layout(height=350)
        st.plotly_chart(fig, width='stretch')
    
    # Quality bottlenecks
    st.subheader("Quality Bottlenecks - Top Machines by Defect Rate")
    defect_by_machine = filtered_df.groupby('Machine_ID').agg({
        'Quality_Control_Defect_Rate_%': 'mean',
        'Error_Rate_%': 'mean',
        'Production_Speed_units_per_hr': 'mean',
        'Predictive_Maintenance_Score': 'mean'
    }).round(2).sort_values('Quality_Control_Defect_Rate_%', ascending=False).head(15)
    st.dataframe(defect_by_machine, width='stretch')

# ============================================================
# TAB 4: EFFICIENCY DIAGNOSTICS VIEW
# ============================================================
with tab4:
    st.header("Efficiency Diagnostics View")
    
    # Efficiency Status Breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Efficiency Status Breakdown")
        eff_counts = filtered_df['Efficiency_Status'].value_counts()
        fig = px.bar(x=eff_counts.index, y=eff_counts.values,
                    color=eff_counts.index,
                    color_discrete_map={'High': '#2ecc71', 'Medium': '#f39c12', 'Low': '#e74c3c'},
                    title='Efficiency Status Count')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("Efficiency by Operation Mode")
        eff_mode = pd.crosstab(filtered_df['Operation_Mode'], filtered_df['Efficiency_Status'], normalize='index').mul(100).round(1)
        
        # Ensure all efficiency columns exist
        for eff in ['High', 'Medium', 'Low']:
            if eff not in eff_mode.columns:
                eff_mode[eff] = 0.0
        
        fig = px.imshow(eff_mode.T, text_auto=True, aspect="auto",
                       title="Efficiency Distribution by Operation Mode (%)",
                       color_continuous_scale='RdYlGn',
                       labels=dict(x="Operation Mode", y="Efficiency", color="%"))
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    
    # Machine and Mode Comparisons
    st.subheader("Machine Efficiency Comparison")
    eff_machine = pd.crosstab(filtered_df['Machine_ID'], filtered_df['Efficiency_Status'], normalize='index').mul(100).round(1)
    
    # Ensure all efficiency columns exist
    for eff in ['High', 'Medium', 'Low']:
        if eff not in eff_machine.columns:
            eff_machine[eff] = 0.0
    
    eff_machine = eff_machine.sort_values('Low', ascending=False)
    
    fig = go.Figure()
    for eff in ['High', 'Medium', 'Low']:
        fig.add_trace(go.Bar(name=eff, x=eff_machine.index, y=eff_machine[eff],
                            marker_color={'High': '#2ecc71', 'Medium': '#f39c12', 'Low': '#e74c3c'}[eff]))
    fig.update_layout(barmode='stack', title='Efficiency Distribution by Machine (%)', 
                     xaxis_tickangle=-45, height=500)
    st.plotly_chart(fig, width='stretch')
    
    # Cross-metric diagnostics
    st.subheader("Cross-Metric Diagnostics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Temperature vs Defect Rate**")
        fig = px.scatter(filtered_df, x='Temperature_C', y='Quality_Control_Defect_Rate_%',
                        color='Efficiency_Status', trendline='ols',
                        color_discrete_map={'High': '#2ecc71', 'Medium': '#f39c12', 'Low': '#e74c3c'},
                        opacity=0.5)
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.markdown("**Vibration vs Error Rate**")
        fig = px.scatter(filtered_df, x='Vibration_Hz', y='Error_Rate_%',
                        color='Efficiency_Status', trendline='ols',
                        color_discrete_map={'High': '#2ecc71', 'Medium': '#f39c12', 'Low': '#e74c3c'},
                        opacity=0.5)
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Power Consumption vs Efficiency**")
        fig = px.box(filtered_df, x='Efficiency_Status', y='Power_Consumption_kW',
                    color='Efficiency_Status',
                    color_discrete_map={'High': '#2ecc71', 'Medium': '#f39c12', 'Low': '#e74c3c'},
                    title='Power Consumption by Efficiency Status')
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.markdown("**Production Speed vs Efficiency**")
        fig = px.box(filtered_df, x='Efficiency_Status', y='Production_Speed_units_per_hr',
                    color='Efficiency_Status',
                    color_discrete_map={'High': '#2ecc71', 'Medium': '#f39c12', 'Low': '#e74c3c'},
                    title='Production Speed by Efficiency Status')
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    
    # Efficiency by Shift
    st.subheader("Efficiency by Shift")
    eff_shift = pd.crosstab(filtered_df['Shift'], filtered_df['Efficiency_Status'], normalize='index').mul(100).round(1)
    
    # Ensure all efficiency columns exist
    for eff in ['High', 'Medium', 'Low']:
        if eff not in eff_shift.columns:
            eff_shift[eff] = 0.0
    
    fig = px.imshow(eff_shift.T, text_auto=True, aspect="auto",
                   title="Efficiency Distribution by Shift (%)",
                   color_continuous_scale='RdYlGn')
    fig.update_layout(height=300)
    st.plotly_chart(fig, width='stretch')

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🏭 6G-Enabled Smart Factory Manufacturing Analytics Dashboard | Thales Group | Unified Mentor Project</p>
    <p>Data: Simulated IIoT Sensor Data | Last Updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)