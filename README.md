# 6G-Enabled Smart Factory: Manufacturing Process Health & Operational Efficiency Analysis

**Unified Mentor Project | Thales Group**

## Project Structure

```
ml project/
├── data/
│   └── manufacturing_data.csv          # Generated synthetic dataset (108K records)
├── src/
│   ├── generate_data.py                # Synthetic data generator
│   └── eda_analysis.py                 # Complete EDA analysis (6-step methodology)
├── dashboard/
│   └── app.py                          # Streamlit dashboard with 4 modules
├── reports/
│   ├── validation_results.json         # Data validation output
│   ├── machine_health_analysis.csv     # Per-machine health metrics
│   ├── production_performance.csv      # Production diagnostics
│   ├── kpis.json                       # Key Performance Indicators
│   ├── research_paper.md               # Full research paper
│   ├── executive_summary.md            # Government stakeholder summary
│   └── *.html                          # Interactive Plotly visualizations
├── requirements.txt                     # Python dependencies
└── README.md                           # This file
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Data (already done)
```bash
python src/generate_data.py
```

### 3. Run EDA Analysis
```bash
python src/eda_analysis.py
```
Outputs: Console analysis + JSON/CSV reports + HTML visualizations in `reports/`

### 4. Launch Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```
Access at: http://localhost:8501

## Dashboard Modules

| Tab | Description | Features |
|-----|-------------|----------|
| **Factory Health Overview** | Fleet-level KPIs & trends | Efficiency distribution, sensor averages, daily trends |
| **Machine Health Dashboard** | Per-machine diagnostics | Health scorecards, sensor trends, mode stability |
| **Production & Quality Panel** | Output & quality analysis | Speed vs defect scatter, error frequency, hourly patterns |
| **Efficiency Diagnostics View** | Deep efficiency analysis | Breakdowns by mode/shift/machine, cross-metric plots |

## Interactive Filters (Sidebar)
- **Machine Selector:** All 50 machines or individual
- **Operation Mode Filter:** normal, high-load, idle, startup, maintenance
- **Date Range Selector:** 90-day range
- **Metric Comparison Toggles:** Multi-select sensor metrics

## Key Deliverables

1. **Research Paper** (`reports/research_paper.md`) - Complete EDA, insights, recommendations
2. **Streamlit Dashboard** (`dashboard/app.py`) - Live interactive analytics
3. **Executive Summary** (`reports/executive_summary.md`) - Government stakeholder format

## Dataset Schema

| Column | Type | Description |
|--------|------|-------------|
| Date | str | Calendar date (YYYY-MM-DD) |
| Time | str | Timestamp (HH:MM:SS) |
| Machine_ID | str | M001-M050 |
| Operation_Mode | str | normal, high-load, maintenance, idle, startup |
| Temperature_C | float | Operating temperature (°C) |
| Vibration_Hz | float | Vibration frequency (Hz) |
| Power_Consumption_kW | float | Electrical power (kW) |
| Network_Latency_ms | float | 6G latency (ms) |
| Packet_Loss_% | float | Packet loss percentage |
| Quality_Control_Defect_Rate_% | float | Defect percentage |
| Production_Speed_units_per_hr | float | Output rate |
| Predictive_Maintenance_Score | float | AI maintenance readiness (0-100) |
| Error_Rate_% | float | Operational error percentage |
| Efficiency_Status | str | High, Medium, Low |

## Analytical Methodology (6 Steps)

1. **Data Validation & Preparation** - Range checks, missing values, standardization
2. **Machine-Level Sensor Health Analysis** - Per-machine patterns, thresholds, mode comparison
3. **Production Performance Diagnostics** - Speed trends, consistency, underperformers
4. **Quality & Error Analysis** - Sensor-quality correlations, error spikes, temporal patterns
5. **Efficiency Status Distribution** - Cross-tabs by mode, shift, machine
6. **Cross-Metric Diagnostics** - Temperature-defect, vibration-error, power-efficiency

## KPIs Calculated

- **Machine Health Index** - Composite from temp, vibration, power, defects, errors
- **Average Production Speed** - Mean output per machine
- **Defect Density Score** - Defects per 1000 units
- **Error Frequency Index** - Operational error rate
- **Efficiency Distribution** - High/Medium/Low spread

## Requirements

- Python 3.10+
- See `requirements.txt` for full list

## License

Project for Unified Mentor / Thales Group educational purposes.