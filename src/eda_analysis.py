import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

df = pd.read_csv("data/manufacturing_data.csv")
# Handle both 'Time' and 'Timestamp' column names
time_col = 'Time' if 'Time' in df.columns else 'Timestamp'
# Fast parsing: date is DD-MM-YYYY, time is HH:MM:SS
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df[time_col], format='%d-%m-%Y %H:%M:%S')

print("=" * 80)
print("MANUFACTURING PROCESS HEALTH & OPERATIONAL EFFICIENCY ANALYSIS")
print("=" * 80)
print(f"\nDataset Shape: {df.shape}")
print(f"Date Range: {df['Date'].min()} to {df['Date'].max()}")
print(f"Machines: {df['Machine_ID'].nunique()}")
print(f"Operation Modes: {df['Operation_Mode'].unique()}")

# ============================================================
# 1. DATA VALIDATION & PREPARATION
# ============================================================
print("\n" + "=" * 80)
print("1. DATA VALIDATION & PREPARATION")
print("=" * 80)

print("\n--- Missing Values ---")
print(df.isnull().sum())

print("\n--- Data Types ---")
print(df.dtypes)

print("\n--- Sensor Range Validation ---")
sensor_cols = ['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW', 
               'Network_Latency_ms', 'Packet_Loss_%', 'Quality_Control_Defect_Rate_%',
               'Production_Speed_units_per_hr', 'Predictive_Maintenance_Score', 'Error_Rate_%']
for col in sensor_cols:
    print(f"{col}: Min={df[col].min():.2f}, Max={df[col].max():.2f}, Mean={df[col].mean():.2f}, Std={df[col].std():.2f}")

print("\n--- Operation Mode Distribution ---")
print(df['Operation_Mode'].value_counts())

print("\n--- Efficiency Status Distribution ---")
print(df['Efficiency_Status'].value_counts())
print(df['Efficiency_Status'].value_counts(normalize=True).mul(100).round(2))

# Save validation results
validation_results = {
    "total_records": int(len(df)),
    "date_range": {"min": df['Date'].min(), "max": df['Date'].max()},
    "n_machines": int(df['Machine_ID'].nunique()),
    "missing_values": df.isnull().sum().to_dict(),
    "sensor_ranges": {col: {"min": float(df[col].min()), "max": float(df[col].max()), 
                           "mean": float(df[col].mean()), "std": float(df[col].std())} for col in sensor_cols},
    "operation_mode_dist": df['Operation_Mode'].value_counts().to_dict(),
    "efficiency_dist": df['Efficiency_Status'].value_counts().to_dict()
}
with open("reports/validation_results.json", "w") as f:
    json.dump(validation_results, f, indent=2)

# ============================================================
# 2. MACHINE-LEVEL SENSOR HEALTH ANALYSIS
# ============================================================
print("\n" + "=" * 80)
print("2. MACHINE-LEVEL SENSOR HEALTH ANALYSIS")
print("=" * 80)

machine_health = df.groupby('Machine_ID').agg({
    'Temperature_C': ['mean', 'std', 'max'],
    'Vibration_Hz': ['mean', 'std', 'max'],
    'Power_Consumption_kW': ['mean', 'std', 'max'],
    'Predictive_Maintenance_Score': ['mean', 'min'],
    'Quality_Control_Defect_Rate_%': 'mean',
    'Error_Rate_%': 'mean',
    'Production_Speed_units_per_hr': 'mean',
    'Efficiency_Status': lambda x: (x == 'Low').sum()
}).round(2)

machine_health.columns = ['_'.join(col).strip() for col in machine_health.columns.values]
machine_health = machine_health.reset_index()

# Machine Health Index (composite)
machine_health['Machine_Health_Index'] = (
    100 - machine_health['Temperature_C_mean'] * 0.4 
    - machine_health['Vibration_Hz_mean'] * 0.6 
    - machine_health['Power_Consumption_kW_mean'] * 0.2
    - machine_health['Quality_Control_Defect_Rate_%_mean'] * 3
    - machine_health['Error_Rate_%_mean'] * 2
).clip(0, 100)

print("\n--- Top 10 Healthiest Machines ---")
print(machine_health.nlargest(10, 'Machine_Health_Index')[['Machine_ID', 'Machine_Health_Index', 'Predictive_Maintenance_Score_mean']])

print("\n--- Top 10 Unhealthiest Machines ---")
print(machine_health.nsmallest(10, 'Machine_Health_Index')[['Machine_ID', 'Machine_Health_Index', 'Predictive_Maintenance_Score_mean']])

# Threshold analysis
temp_threshold = 85
vib_threshold = 50
power_threshold = 100

near_threshold = machine_health[
    (machine_health['Temperature_C_max'] > temp_threshold) | 
    (machine_health['Vibration_Hz_max'] > vib_threshold) | 
    (machine_health['Power_Consumption_kW_max'] > power_threshold)
]
print(f"\n--- Machines Near Threshold Limits ---")
print(f"Temperature > {temp_threshold}°C: {(machine_health['Temperature_C_max'] > temp_threshold).sum()} machines")
print(f"Vibration > {vib_threshold} Hz: {(machine_health['Vibration_Hz_max'] > vib_threshold).sum()} machines")
print(f"Power > {power_threshold} kW: {(machine_health['Power_Consumption_kW_max'] > power_threshold).sum()} machines")
print(f"Total machines near any threshold: {len(near_threshold)}")

# Sensor stability across operation modes
mode_sensor = df.groupby(['Machine_ID', 'Operation_Mode']).agg({
    'Temperature_C': 'std',
    'Vibration_Hz': 'std',
    'Power_Consumption_kW': 'std'
}).reset_index()
print("\n--- Sensor Stability by Operation Mode (avg std across machines) ---")
print(mode_sensor.groupby('Operation_Mode')[['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW']].mean().round(2))

machine_health.to_csv("reports/machine_health_analysis.csv", index=False)

# ============================================================
# 3. PRODUCTION PERFORMANCE DIAGNOSTICS
# ============================================================
print("\n" + "=" * 80)
print("3. PRODUCTION PERFORMANCE DIAGNOSTICS")
print("=" * 80)

prod_by_machine = df.groupby('Machine_ID').agg({
    'Production_Speed_units_per_hr': ['mean', 'std', 'min', 'max'],
    'Quality_Control_Defect_Rate_%': 'mean',
    'Error_Rate_%': 'mean',
    'Efficiency_Status': lambda x: (x == 'Low').sum()
}).round(2)
prod_by_machine.columns = ['_'.join(col).strip() for col in prod_by_machine.columns.values]
prod_by_machine = prod_by_machine.reset_index()

print("\n--- Production Speed Statistics ---")
print(f"Overall Mean: {df['Production_Speed_units_per_hr'].mean():.2f}")
print(f"Overall Std: {df['Production_Speed_units_per_hr'].std():.2f}")

print("\n--- Top 10 Underperforming Machines (Low Speed + High Defect) ---")
prod_by_machine['Performance_Score'] = (
    prod_by_machine['Production_Speed_units_per_hr_mean'] / prod_by_machine['Production_Speed_units_per_hr_mean'].max() * 50
    - prod_by_machine['Quality_Control_Defect_Rate_%_mean'] / prod_by_machine['Quality_Control_Defect_Rate_%_mean'].max() * 30
    - prod_by_machine['Error_Rate_%_mean'] / prod_by_machine['Error_Rate_%_mean'].max() * 20
)
print(prod_by_machine.nsmallest(10, 'Performance_Score')[['Machine_ID', 'Production_Speed_units_per_hr_mean', 
      'Quality_Control_Defect_Rate_%_mean', 'Error_Rate_%_mean', 'Performance_Score']])

# Output consistency
print("\n--- Output Consistency (CV of Production Speed) ---")
prod_by_machine['Speed_CV'] = prod_by_machine['Production_Speed_units_per_hr_std'] / prod_by_machine['Production_Speed_units_per_hr_mean']
print(prod_by_machine.nlargest(10, 'Speed_CV')[['Machine_ID', 'Speed_CV']])

prod_by_machine.to_csv("reports/production_performance.csv", index=False)

# ============================================================
# 4. QUALITY & ERROR ANALYSIS
# ============================================================
print("\n" + "=" * 80)
print("4. QUALITY & ERROR ANALYSIS")
print("=" * 80)

# Defect rate correlation with sensors
sensor_cols_for_corr = ['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW', 
               'Network_Latency_ms', 'Packet_Loss_%',
               'Production_Speed_units_per_hr', 'Predictive_Maintenance_Score', 'Error_Rate_%']
corr_matrix_defect = df[sensor_cols_for_corr + ['Quality_Control_Defect_Rate_%']].corr()
sensor_defect_corr = corr_matrix_defect['Quality_Control_Defect_Rate_%'].sort_values(ascending=False)
print("\n--- Correlation with Defect Rate ---")
print(sensor_defect_corr)

# Error rate correlation
sensor_cols_for_corr2 = ['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW', 
               'Network_Latency_ms', 'Packet_Loss_%',
               'Production_Speed_units_per_hr', 'Predictive_Maintenance_Score',
               'Quality_Control_Defect_Rate_%']
corr_matrix_error = df[sensor_cols_for_corr2 + ['Error_Rate_%']].corr()
sensor_error_corr = corr_matrix_error['Error_Rate_%'].sort_values(ascending=False)
print("\n--- Correlation with Error Rate ---")
print(sensor_error_corr)
print("\n--- Correlation with Error Rate ---")
print(sensor_error_corr)

# Defect rate by machine and mode
defect_by_machine_mode = df.groupby(['Machine_ID', 'Operation_Mode'])['Quality_Control_Defect_Rate_%'].mean().reset_index()
print("\n--- Avg Defect Rate by Operation Mode ---")
print(df.groupby('Operation_Mode')['Quality_Control_Defect_Rate_%'].mean().sort_values(ascending=False).round(2))

# Error rate spikes
error_spikes = df[df['Error_Rate_%'] > df['Error_Rate_%'].quantile(0.95)]
print(f"\n--- Error Rate Spikes (top 5%) ---")
print(f"Count: {len(error_spikes)}")
print(f"Machines involved: {error_spikes['Machine_ID'].nunique()}")
print(f"Modes: {error_spikes['Operation_Mode'].value_counts().to_dict()}")

# Time-based analysis
df['Hour'] = df['Datetime'].dt.hour
defect_by_hour = df.groupby('Hour')['Quality_Control_Defect_Rate_%'].mean()
error_by_hour = df.groupby('Hour')['Error_Rate_%'].mean()
print("\n--- Defect Rate by Hour (Top 5) ---")
print(defect_by_hour.nlargest(5).round(2))
print("\n--- Error Rate by Hour (Top 5) ---")
print(error_by_hour.nlargest(5).round(2))

# ============================================================
# 5. EFFICIENCY STATUS DISTRIBUTION
# ============================================================
print("\n" + "=" * 80)
print("5. EFFICIENCY STATUS DISTRIBUTION")
print("=" * 80)

eff_dist = df['Efficiency_Status'].value_counts(normalize=True).mul(100).round(2)
print("\n--- Overall Efficiency Distribution ---")
print(eff_dist)

eff_by_mode = pd.crosstab(df['Operation_Mode'], df['Efficiency_Status'], normalize='index').mul(100).round(2)
print("\n--- Efficiency by Operation Mode (%) ---")
print(eff_by_mode)

df['Shift'] = pd.cut(df['Datetime'].dt.hour, bins=[0, 8, 16, 24], labels=['Night', 'Day', 'Evening'], right=False)
eff_by_shift = pd.crosstab(df['Shift'], df['Efficiency_Status'], normalize='index').mul(100).round(2)
print("\n--- Efficiency by Shift (%) ---")
print(eff_by_shift)

eff_by_machine = pd.crosstab(df['Machine_ID'], df['Efficiency_Status'], normalize='index').mul(100).round(2)
print("\n--- Machines with >30% Low Efficiency ---")
low_eff_machines = eff_by_machine[eff_by_machine['Low'] > 30]
print(low_eff_machines)

# ============================================================
# 6. CROSS-METRIC DIAGNOSTICS
# ============================================================
print("\n" + "=" * 80)
print("6. CROSS-METRIC DIAGNOSTICS")
print("=" * 80)

# Temperature vs Defect Rate
temp_defect = df.groupby(pd.cut(df['Temperature_C'], bins=10))['Quality_Control_Defect_Rate_%'].mean()
print("\n--- Temperature vs Defect Rate (binned) ---")
print(temp_defect.round(2))

# Vibration vs Error Rate
vib_error = df.groupby(pd.cut(df['Vibration_Hz'], bins=10))['Error_Rate_%'].mean()
print("\n--- Vibration vs Error Rate (binned) ---")
print(vib_error.round(2))

# Power vs Efficiency
power_eff = df.groupby('Efficiency_Status')['Power_Consumption_kW'].mean()
print("\n--- Power Consumption by Efficiency Status ---")
print(power_eff.round(2))

# Correlation matrix for key metrics
key_metrics = ['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW', 
               'Quality_Control_Defect_Rate_%', 'Error_Rate_%',
               'Production_Speed_units_per_hr', 'Predictive_Maintenance_Score',
               'Network_Latency_ms', 'Packet_Loss_%']
corr_matrix = df[key_metrics].corr().round(3)
print("\n--- Key Metrics Correlation Matrix ---")
print(corr_matrix)

# ============================================================
# 7. KPI CALCULATIONS
# ============================================================
print("\n" + "=" * 80)
print("7. KEY PERFORMANCE INDICATORS (KPIs)")
print("=" * 80)

kpis = {
    "Machine_Health_Index": {
        "description": "Composite score from temperature, vibration, power",
        "overall_mean": float(machine_health['Machine_Health_Index'].mean()),
        "by_machine": machine_health.set_index('Machine_ID')['Machine_Health_Index'].to_dict()
    },
    "Average_Production_Speed": {
        "description": "Mean output rate per machine",
        "overall_mean": float(df['Production_Speed_units_per_hr'].mean()),
        "by_machine": prod_by_machine.set_index('Machine_ID')['Production_Speed_units_per_hr_mean'].to_dict()
    },
    "Defect_Density_Score": {
        "description": "Defect rate relative to production volume",
        "overall_mean": float((df.loc[df['Production_Speed_units_per_hr'] > 0, 'Quality_Control_Defect_Rate_%'] / df.loc[df['Production_Speed_units_per_hr'] > 0, 'Production_Speed_units_per_hr'] * 1000).mean()),
        "by_machine": (df[df['Production_Speed_units_per_hr'] > 0].groupby('Machine_ID').apply(lambda x: (x['Quality_Control_Defect_Rate_%'] / x['Production_Speed_units_per_hr'] * 1000).mean())).to_dict()
    },
    "Error_Frequency_Index": {
        "description": "Rate of operational errors",
        "overall_mean": float(df['Error_Rate_%'].mean()),
        "by_machine": df.groupby('Machine_ID')['Error_Rate_%'].mean().to_dict()
    },
    "Efficiency_Distribution": {
        "description": "High / Medium / Low efficiency spread",
        "distribution": df['Efficiency_Status'].value_counts().to_dict(),
        "percentages": df['Efficiency_Status'].value_counts(normalize=True).mul(100).round(2).to_dict()
    }
}

print("\n--- KPI Summary ---")
for kpi, vals in kpis.items():
    if 'overall_mean' in vals:
        print(f"{kpi}: {vals['overall_mean']:.2f} - {vals['description']}")
    else:
        print(f"{kpi}: {vals['percentages']} - {vals['description']}")

with open("reports/kpis.json", "w") as f:
    json.dump(kpis, f, indent=2, default=str)

# ============================================================
# VISUALIZATIONS
# ============================================================
print("\n" + "=" * 80)
print("GENERATING VISUALIZATIONS")
print("=" * 80)

# 1. Efficiency Distribution Pie Chart
fig = px.pie(df, names='Efficiency_Status', title='Overall Efficiency Distribution',
             color='Efficiency_Status', color_discrete_map={'High': 'green', 'Medium': 'orange', 'Low': 'red'})
fig.write_html("reports/efficiency_distribution.html")

# 2. Machine Health Index Heatmap
health_pivot = machine_health.set_index('Machine_ID')['Machine_Health_Index']
fig = px.bar(machine_health.sort_values('Machine_Health_Index'), x='Machine_ID', y='Machine_Health_Index',
             title='Machine Health Index by Machine', color='Machine_Health_Index',
             color_continuous_scale='RdYlGn')
fig.write_html("reports/machine_health_index.html")

# 3. Sensor Trends by Operation Mode
fig = make_subplots(rows=3, cols=1, subplot_titles=('Temperature by Mode', 'Vibration by Mode', 'Power by Mode'))
for i, sensor in enumerate(['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW']):
    mode_data = df.groupby('Operation_Mode')[sensor].mean().reset_index()
    fig.add_trace(go.Bar(x=mode_data['Operation_Mode'], y=mode_data[sensor], name=sensor), row=i+1, col=1)
fig.update_layout(height=800, title_text="Average Sensor Readings by Operation Mode")
fig.write_html("reports/sensors_by_mode.html")

# 4. Production Speed vs Defect Rate Scatter
fig = px.scatter(df, x='Production_Speed_units_per_hr', y='Quality_Control_Defect_Rate_%',
                 color='Efficiency_Status', facet_col='Operation_Mode',
                 color_discrete_map={'High': 'green', 'Medium': 'orange', 'Low': 'red'},
                 title='Production Speed vs Defect Rate by Operation Mode')
fig.write_html("reports/speed_vs_defect.html")

# 5. Correlation Heatmap
fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", 
                title="Key Metrics Correlation Matrix", color_continuous_scale='RdBu_r')
fig.write_html("reports/correlation_heatmap.html")

# 6. Temperature vs Defect Rate
fig = px.scatter(df, x='Temperature_C', y='Quality_Control_Defect_Rate_%',
                 color='Efficiency_Status', trendline='ols',
                 color_discrete_map={'High': 'green', 'Medium': 'orange', 'Low': 'red'},
                 title='Temperature vs Defect Rate')
fig.write_html("reports/temp_vs_defect.html")

# 7. Vibration vs Error Rate
fig = px.scatter(df, x='Vibration_Hz', y='Error_Rate_%',
                 color='Efficiency_Status', trendline='ols',
                 color_discrete_map={'High': 'green', 'Medium': 'orange', 'Low': 'red'},
                 title='Vibration vs Error Rate')
fig.write_html("reports/vib_vs_error.html")

# 8. Power vs Efficiency
fig = px.box(df, x='Efficiency_Status', y='Power_Consumption_kW',
             color='Efficiency_Status', color_discrete_map={'High': 'green', 'Medium': 'orange', 'Low': 'red'},
             title='Power Consumption by Efficiency Status')
fig.write_html("reports/power_by_efficiency.html")

# 9. Time Series - Defect Rate by Hour
fig = px.line(x=defect_by_hour.index, y=defect_by_hour.values,
              title='Average Defect Rate by Hour of Day', labels={'x': 'Hour', 'y': 'Defect Rate %'})
fig.write_html("reports/defect_by_hour.html")

# 10. Efficiency by Mode and Shift
eff_mode_shift = df.groupby(['Operation_Mode', 'Shift'])['Efficiency_Status'].value_counts(normalize=True).mul(100).unstack(fill_value=0)
fig = px.imshow(eff_mode_shift.T, text_auto='.1f', aspect="auto",
                title="Efficiency Distribution by Operation Mode and Shift (%)",
                color_continuous_scale='RdYlGn')
fig.write_html("reports/efficiency_mode_shift.html")

print("\nAll visualizations saved to reports/")
print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)