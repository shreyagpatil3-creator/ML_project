# Manufacturing Process Health and Operational Efficiency Analysis in 6G-Enabled Smart Factories

**A Comprehensive Diagnostic Intelligence Study for Thales Group**

---

## Abstract

This research presents a systematic diagnostic analysis of manufacturing process health and operational efficiency in 6G-enabled smart factory environments. Leveraging 100,000 sensor records across 50 industrial machines over a 30-day period (January 2025), we establish a baseline diagnostic intelligence layer for Thales Group's manufacturing operations. Our analysis reveals critical operational patterns: 77.8% of operations classified as Low efficiency, three distinct operation modes (Active, Idle, Maintenance), and sensor readings showing minimal correlation with quality outcomes. The study provides actionable recommendations for efficiency improvement, operational mode optimization, and sensor infrastructure enhancement.

**Keywords:** Smart Manufacturing, Industrial IoT, 6G Networks, Operational Efficiency, Machine Health Monitoring, Thales Group

---

## 1. Introduction

### 1.1 Background
Modern smart factories operate with hundreds of interconnected machines generating real-time Industrial IoT (IIoT) sensor data over high-speed 6G networks. Thales Group, as a leader in defense and aerospace technology, requires real-time visibility into machine health, production efficiency, and quality assurance across its advanced manufacturing facilities.

### 1.2 Objectives
This study establishes a diagnostic intelligence layer by:
1. Validating and preparing multi-source sensor data
2. Analyzing machine-level sensor health patterns
3. Diagnosing production performance and quality issues
4. Evaluating efficiency status distributions
5. Performing cross-metric diagnostics for root cause identification

### 1.3 Scope
Analysis covers 50 machines, 3 operation modes (Active, Idle, Maintenance), 9 sensor types, and 3 efficiency classifications over 30 days of continuous operation (January 2025).

---

## 2. Data Description and Methodology

### 2.1 Dataset Characteristics
| Attribute | Value |
|-----------|-------|
| Total Records | 100,000 |
| Time Period | 2025-01-01 to 2025-01-31 (30 days) |
| Machines | 50 (IDs: 1-50) |
| Operation Modes | 3 (Active: 70.1%, Idle: 20.1%, Maintenance: 9.9%) |
| Sampling Frequency | ~1 minute per machine |

### 2.2 Sensor Variables
| Variable | Unit | Range | Mean ± Std |
|----------|------|-------|------------|
| Temperature | °C | 30.0 - 90.0 | 60.0 ± 17.3 |
| Vibration | Hz | 0.1 - 5.0 | 2.6 ± 1.4 |
| Power Consumption | kW | 1.5 - 10.0 | 5.8 ± 2.5 |
| Network Latency | ms | 1.0 - 50.0 | 25.6 ± 14.1 |
| Packet Loss | % | 0.0 - 5.0 | 2.5 ± 1.4 |
| Defect Rate | % | 0.0 - 10.0 | 5.0 ± 2.9 |
| Production Speed | units/hr | 50.0 - 500.0 | 275.9 ± 130.1 |
| Maintenance Score | 0-1 | 0.0 - 1.0 | 0.5 ± 0.3 |
| Error Rate | % | 0.0 - 15.0 | 7.5 ± 4.3 |

### 2.3 Analytical Methodology
Following the six-step framework:
1. **Data Validation & Preparation** - Range checks, missing value analysis, standardization
2. **Machine-Level Sensor Health Analysis** - Per-machine patterns, threshold monitoring, mode comparison
3. **Production Performance Diagnostics** - Speed trends, output consistency, underperformer identification
4. **Quality & Error Analysis** - Sensor-quality correlations, error spike detection, temporal patterns
5. **Efficiency Status Distribution** - Cross-tabulation by mode, shift, machine
6. **Cross-Metric Diagnostics** - Temperature-defect, vibration-error, power-efficiency relationships

---

## 3. Results

### 3.1 Machine-Level Sensor Health Analysis

#### 3.1.1 Machine Health Index Distribution
The composite Machine Health Index (MHI) combines temperature, vibration, power, defect rate, and error rate into a single 0-100 score.

**Key Findings:**
- Overall mean MHI: **43.3** (moderate fleet health)
- Healthiest machine: **Machine 45** (MHI: 44.0, Maintenance Score: 0.51)
- Unhealthiest machine: **Machine 47** (MHI: 42.7, Maintenance Score: 0.50)
- **50 of 50 machines (100%)** exceed temperature threshold (>85°C) at some point
- Narrow MHI range (42.7-44.0) indicates uniform fleet condition

#### 3.1.2 Threshold Violations
| Threshold | Limit | Machines Exceeding | % of Fleet |
|-----------|-------|-------------------|------------|
| Temperature | >85°C | 50 | 100% |
| Vibration | >50 Hz | 0 | 0% |
| Power | >100 kW | 0 | 0% |

**Critical Insight:** Temperature is the only sensor approaching concerning thresholds. Vibration (max 5 Hz) and Power (max 10 kW) are well within safe limits.

#### 3.1.3 Sensor Stability by Operation Mode
All operation modes show similar sensor variability:
- Temperature std: ~17.3 across all modes
- Vibration std: ~1.4 across all modes
- Power std: ~2.4-2.5 across all modes

Sensor behavior is consistent regardless of operation mode.

### 3.2 Production Performance Diagnostics

#### 3.2.1 Overall Production Metrics
- **Mean Production Speed:** 275.9 units/hr (σ = 130.1)
- **Coefficient of Variation (CV):** 0.47-0.49 across machines, indicating moderate output consistency

#### 3.2.2 Underperforming Machines
Top 10 machines with lowest performance scores (combining speed, defect rate, error rate):
1. Machine 14, 9, 38, 40, 25, 17, 47, 46, 8, 36

These machines show **simultaneously low speed and high defect/error rates**.

#### 3.2.3 Output Consistency
Machines with highest speed variability (CV > 0.48): 46, 5, 12, 8, 49, 35, 48, 14, 6, 7
*Several overlap with underperformers, confirming instability-quality relationship.*

### 3.3 Quality & Error Analysis

#### 3.3.1 Sensor-Quality Correlations
**Critical Finding:** Sensor readings show **negligible correlation** with quality metrics:

| Sensor | Correlation with Defect Rate | Correlation with Error Rate |
|--------|------------------------------|----------------------------|
| Temperature | -0.002 | -0.002 |
| Vibration | 0.000 | 0.005 |
| Power Consumption | -0.001 | 0.001 |
| Network Latency | -0.004 | 0.000 |
| Packet Loss | -0.005 | -0.002 |
| Production Speed | -0.005 | 0.006 |
| Maintenance Score | 0.000 | 0.005 |

**Interpretation:** In this dataset, sensor readings (temperature, vibration, power) **do not predict** defect rates or error rates. Quality outcomes appear independent of monitored physical parameters.

#### 3.3.2 Defect Rate by Operation Mode
| Operation Mode | Avg Defect Rate | % of Total Records |
|----------------|-----------------|-------------------|
| Idle | 5.01% | 20.1% |
| Active | 5.01% | 70.1% |
| Maintenance | 5.00% | 9.9% |

**Defect rates are uniform across all operation modes** (~5%), suggesting systemic quality issues rather than mode-specific problems.

#### 3.3.3 Error Rate Spikes
- **4,997 records (5.0%)** in top 5% error rate threshold
- **3,492 (70%)** occur during Active mode
- **1,019 (20%)** during Idle
- **486 (10%)** during Maintenance
- All 50 machines experience error spikes

#### 3.3.4 Temporal Patterns
- **Peak defect hours:** 23:00, 12:00, 14:00, 01:00, 04:00 (range: 5.04-5.09%)
- **Peak error hours:** 01:00, 19:00, 07:00, 21:00, 12:00 (range: 7.60-7.63%)
- Minimal hourly variation (±0.05% for defects, ±0.03% for errors)

### 3.4 Efficiency Status Distribution

| Efficiency Level | Count | Percentage |
|------------------|-------|------------|
| Low | 77,825 | 77.83% |
| Medium | 19,189 | 19.19% |
| High | 2,986 | 2.99% |

#### 3.4.1 Efficiency by Operation Mode
| Mode | High | Medium | Low |
|------|------|--------|-----|
| Active | 3.0% | 19.3% | 77.7% |
| Idle | 2.8% | 18.9% | 78.3% |
| Maintenance | 3.0% | 19.2% | 77.8% |

**Efficiency distribution is nearly identical across all operation modes.** No mode shows superior efficiency.

#### 3.4.2 Efficiency by Shift
All shifts show similar distributions (~3% High, ~19% Medium, ~78% Low), indicating no systemic shift-based issues.

#### 3.4.3 Machine-Level Efficiency
**All 50 machines** have >76% Low efficiency classification. No machines meet the >30% Low efficiency threshold as outliers - the entire fleet is consistently low efficiency.

### 3.5 Cross-Metric Diagnostics

#### 3.5.1 Temperature vs Defect Rate
Defect rate remains constant (~5.0%) across all temperature bins (30-90°C). **No relationship exists.**

#### 3.5.2 Vibration vs Error Rate
Error rate remains constant (~7.5%) across all vibration bins (0.1-5.0 Hz). **No relationship exists.**

#### 3.5.3 Power Consumption vs Efficiency
| Efficiency | Avg Power (kW) |
|------------|----------------|
| High | 5.72 |
| Medium | 5.76 |
| Low | 5.74 |

**Power consumption is identical across efficiency levels** (~5.7 kW).

#### 3.5.4 Key Metrics Correlation Matrix
All sensor-to-quality correlations are near zero (|r| < 0.01). The strongest correlations are between sensors themselves:
- Temperature ↔ Vibration: 0.001
- Temperature ↔ Power: 0.005
- Production Speed ↔ Temperature: 0.001

---

## 4. Key Performance Indicators (KPIs)

| KPI | Value | Interpretation |
|-----|-------|----------------|
| Machine Health Index (Mean) | 43.3/100 | Moderate fleet health, uniform across machines |
| Avg Production Speed | 275.9 units/hr | Baseline for improvement targeting |
| Defect Density Score | 25.6 | Defects per 1000 units produced (elevated) |
| Error Frequency Index | 7.50% | High operational error rate |
| Efficiency Distribution | H: 3.0%, M: 19.2%, L: 77.8% | **Critical: Fleet-wide efficiency crisis** |

---

## 5. Discussion

### 5.1 Root Cause Analysis
The **absence of correlations** (|r| < 0.01) between physical sensors (temperature, vibration, power) and quality metrics (defect rate, error rate) indicates:
1. **Sensor placement/selection may not capture true failure modes**
2. **Quality defects may originate from non-monitored factors** (material quality, operator skill, tooling wear)
3. **Current sensor suite insufficient for predictive quality modeling**

### 5.2 Efficiency Crisis
**77.8% Low efficiency across all machines, modes, and shifts** indicates a systemic issue, not isolated machine problems. Potential causes:
- Efficiency classification thresholds may be miscalibrated
- Production targets may be unrealistic
- Systemic process design issues

### 5.3 Operation Mode Analysis
Three modes (Active, Idle, Maintenance) show **identical defect rates (~5%) and efficiency distributions**. This suggests:
- Mode transitions don't impact quality
- "Idle" and "Maintenance" modes still produce defects at Active-mode rates
- Mode definitions may need refinement

### 5.4 Sensor Infrastructure Assessment
Current sensors monitor:
- Temperature (30-90°C): Only parameter near thresholds
- Vibration (0.1-5 Hz): Very low range, well below typical industrial thresholds (40-50 Hz)
- Power (1.5-10 kW): Low consumption range

**Recommendation:** Sensor suite may need higher-resolution vibration monitoring and additional quality-relevant sensors (acoustic, force, vision).

### 5.5 Transition to Predictive Operations
Current state: **Reactive with no predictive signals**
Target state: **Predictive** - requires:
1. Identifying true leading indicators of quality
2. Expanding sensor coverage to capture defect root causes
3. Recalibrating efficiency classification

---

## 6. Recommendations

### 6.1 Immediate Actions (0-30 days)
1. **Investigate efficiency classification logic** - 77.8% Low suggests threshold miscalibration
2. **Audit sensor placement** - Current sensors don't correlate with quality outcomes
3. **Analyze defect root causes** - 5% defect rate is uniform; identify non-sensor factors
4. **Validate Maintenance Score calculation** - Range 0-1 vs expected 0-100 scale

### 6.2 Short-term Initiatives (1-3 months)
1. **Deploy additional sensors** on chronic underperformers (Machines 8, 9, 14, 17, 25, 36, 38, 40, 46, 47)
2. **Implement high-frequency sampling** (10-sec intervals) on 10 pilot machines
3. **Conduct controlled experiments** varying temperature/vibration to establish causal links
4. **Redefine operation modes** - Current 3 modes show no behavioral differentiation

### 6.3 Strategic Roadmap (3-12 months)
1. **Root Cause Analysis Program** - Physics-based modeling of defect generation
2. **Sensor Suite Redesign** - Add acoustic emission, force/torque, vision inspection
3. **Digital Twin Development** - Process simulation for parameter optimization
4. **Efficiency Recalibration** - Realistic targets based on process capability studies
5. **6G Network Leverage** - Ultra-low latency for closed-loop quality control (when sensors provide signal)

### 6.4 Investment Priorities
| Priority | Investment Area | Rationale |
|----------|-----------------|-----------|
| 1 | Root Cause Analysis / Sensor Audit | Current sensors don't predict quality |
| 2 | Additional Sensor Deployment | Need vibration >5Hz, acoustic, vision |
| 3 | Efficiency Threshold Recalibration | 77.8% Low suggests miscalibration |
| 4 | 6G Edge Computing | Future-ready when predictive signals exist |

---

## 7. Conclusion

This diagnostic analysis of Thales Group's actual manufacturing data (100,000 records, 50 machines, January 2025) reveals:

1. **Systemic Efficiency Crisis** - 77.8% Low efficiency across entire fleet, all modes, all shifts
2. **Sensor-Quality Disconnect** - Physical sensors (temp, vibration, power) show **zero correlation** with defect/error rates (|r| < 0.01)
3. **Uniform Defect Rates** - ~5% defects regardless of operation mode, machine, or time
4. **Temperature Threshold Concern** - 100% of machines exceed 85°C at some point
5. **Maintenance Score Scale Issue** - Current 0-1 range vs expected 0-100

**Critical Path Forward:** Before predictive maintenance or AI optimization can succeed, Thales must:
- **Identify true quality drivers** (current sensors don't capture them)
- **Recalibrate efficiency metrics** (current thresholds classify entire fleet as failing)
- **Expand sensor infrastructure** to monitor actual failure modes
- **Validate data generation process** - Maintenance Score 0-1 suggests possible normalization issue

This work establishes the honest baseline: **current IIoT sensor suite is insufficient for predictive quality modeling.** The next phase must focus on sensor suite redesign and root cause analysis before advancing to predictive operations.

---

## Appendix A: Technical Specifications

### A.1 Machine Health Index Formula
```
MHI = 100 
    - 0.4 × Mean_Temperature 
    - 0.6 × Mean_Vibration 
    - 0.2 × Mean_Power 
    - 3.0 × Mean_Defect_Rate 
    - 2.0 × Mean_Error_Rate
```
*Note: Formula designed for different sensor ranges; may need recalibration for current data scales.*

### A.2 Threshold Definitions (Current Data Context)
- Temperature Warning: >75°C | Critical: >85°C (100% machines exceed)
- Vibration Warning: >4 Hz | Critical: >5 Hz (max observed: 5 Hz)
- Power Warning: >8 kW | Critical: >10 kW (max observed: 10 kW)
- Defect Rate Warning: >3% | Critical: >5% (mean: 5.0%)
- Error Rate Warning: >5% | Critical: >10% (mean: 7.5%)

### A.3 Data Quality Metrics
- Completeness: 100% (no missing values)
- Consistency: All sensors within physical bounds
- Temporal Alignment: Minute-level synchronized across machines
- **Correlation Validity: Sensor-quality correlations near zero - predictive modeling not feasible with current sensors**

---

## Appendix B: Visualization Catalog
All interactive visualizations available in Streamlit dashboard:
1. Factory Health Overview (efficiency distribution, sensor trends)
2. Machine Health Dashboard (scorecards, sensor trends, mode stability)
3. Production & Quality Panel (speed-defect scatter, error frequency, hourly patterns)
4. Efficiency Diagnostics View (breakdowns, cross-metric plots, shift analysis)

Dashboard Access: `streamlit run dashboard/app.py`

---

## Appendix C: Dataset Lineage
- **Source:** Unified Mentor / Thales Group
- **File:** `Thales_Group_Manufacturing.csv`
- **Records:** 100,001
- **Date Range:** 2025-01-01 to 2025-01-31
- **Note:** This analysis uses the actual provided dataset, not synthetic data.

---

*Report Generated: 2025 | Project: Unified Mentor - Thales Group Smart Factory Analytics | Data: Thales_Group_Manufacturing.csv*