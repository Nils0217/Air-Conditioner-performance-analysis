# AC Unit Performance Analysis
### End-to-End Data Analytics Project | IoT Sensor Data | Goa, India

![Python](https://img.shields.io/badge/Python-3.10-blue) ![pandas](https://img.shields.io/badge/pandas-2.0-lightblue) ![MySQL](https://img.shields.io/badge/MySQL-8.0-orange) ![Colab](https://img.shields.io/badge/Google%20Colab-Notebook-yellow)

---

## Project Overview

This project analyzes four years of IoT sensor data (2019–2023) from three ductless-split AC units installed in Room A200 at BITS Pilani Goa Campus. The dataset is sourced from the open-access **SplitSmart** repository published by the Department of Energy.

The goal is to move from raw sensor readings to actionable maintenance recommendations — covering the full data pipeline from ETL through predictive modeling.

**Dataset:** ~510,000 records | 3 AC units (AC01, AC02, AC03) | 14 features  
**Source:** [SplitSmart Open Dataset — OpenEI](https://data.openei.org/submissions/5971)

---

## Project Pipeline

| Step | Topic | Tools | Status |
|------|-------|-------|--------|
| 1 | ETL & Data Cleaning | Python, pandas | ✅ Complete |
| 2 | Exploratory Data Analysis | Python, pandas, seaborn, MySQL | ✅ Complete |
| 3 | BI & Visualization | Tableau / Power BI | ✅ Complete |
| 4 | Predictive Modeling | scikit-learn, Google Colab | ✅ Complete|
| 5 | Maintenance Recommendations | — | ✅ Complete |

---

## Key Findings

### 🔴 AC03 — Intermittent Power Factor Failure
- Average PF drops to **0.62** overall; collapses to **0.37–0.55** during dry_hot (Mar–May) and rainy (Jun–Sep) seasons
- Bimodal PF distribution (clusters at 0.2–0.4 and 0.95–1.0) confirms **intermittent hardware fault**, not sensor noise
- Recovers to normal PF (~0.97) in cool season (Oct–Feb), indicating **temperature and humidity sensitivity**
- Root cause hypothesis: capacitor degradation triggered by sustained heat and humidity exposure

### 🔴 AC02 — Seasonal Shutdown Pattern
- PF collapses to **0.48** exclusively in rainy season (Jun–Sep)
- Operating rate drops to **0%** in November and near-zero in March and October
- Downtime pattern is **irregular** — inconsistent with planned maintenance, suggesting reactive shutdowns following fault events

### 🟢 AC01 — Healthy Baseline
- Maintains PF ~0.97 year-round with stable power output (~4,300–4,500W)
- Serves as the performance reference for all comparative analysis
- Consistently the highest-utilization unit (operating rate 40–99% monthly)

### 💡 Environmental Insight
- External temperature, room temperature, and humidity are **identical across all three units** (same room)
- AC01 operates normally under the same conditions → PF anomalies in AC02/AC03 are **hardware-driven, not environment-driven**
- All units show reduced operation in Jun–Aug, coinciding with peak humidity (85–90%) — humidity is a shared stressor

---

## Step 1: ETL & Data Cleaning

**Notebook:** `Step1_ETL.ipynb`

Key cleaning decisions:
- Records with Current > 35A dropped after cross-validating anomalous peaks across all units at identical timestamps
- **AC02:** CT reverse wiring corrected via `abs()` on Power Factor
- **AC03:** Firmware decimal error corrected on Power Factor values
- Standby PF artifacts (PF=0 when Current <5A) set to 0 explicitly
- Voltage outliers used 3×IQR threshold to preserve legitimate low-voltage records
- External temperature values outside 20–35°C replaced with in-range median
- `Real_Power` recalculated as `Current × Voltage × Power_Factor` after all upstream cleaning
- `unit_consumption` (~36% NaN) left uncleaned — hardware kWh counter, not used in analysis

**Output:** `Goa_A200_AC_unit_performance_clean.csv`

---

## Step 2: Exploratory Data Analysis

**Notebook:** `Step2_EDA_AC_Performance.ipynb`

### 2.1 Energy Consumption Pattern
- Hourly, monthly, and seasonal breakdown by load state (standby / normal / high_load / overload)
- Cold-start effect observed at 05:00–13:00: minor high_load elevation likely due to overnight heat accumulation

### 2.2 Equipment Health Analysis
- Power factor distribution analysis reveals AC03's bimodal fault signature
- Monthly operating rate analysis exposes AC02's irregular shutdown pattern
- Cross-validated with Goa climate data to isolate hardware vs environmental causes

### 2.3 Environmental Correlation
- Correlation matrix: environmental factors vs power metrics
- Scatter analysis: external temperature vs real power by season

### 2.4 Electricity Cost Estimation (MySQL + Python)
- Simulated Time-of-Use tariff (Peak: ₹8.50/kWh | Off-Peak: ₹6.00 | Night: ₹4.00)
- Best case (normal load) vs worst case (high_load + overload) cost comparison per unit

---

## Tech Stack

```
Data Engineering   │ Python, pandas, numpy
Analysis           │ pandas, scipy
Visualization      │ seaborn, matplotlib
Database           │ MySQL (electricity cost analysis)
Environment        │ Google Colab, PyCharm
Version Control    │ Git, GitHub
Dataset            │ SplitSmart (Open Energy Information, DOE)
```

---

## Repository Structure

```
├── Cleaned dataset ready for analysis/
│   └── Goa_A200_AC_unit_performance_clean.csv
├── Step1_ETL.ipynb
├── Step2_EDA_AC_Performance.ipynb
└── README.md
```

---

## About the Dataset

> SplitSmart provides a context-rich open dataset to facilitate research in energy-efficient ductless-split cooling systems. Data was collected over four years (2019–2023) in a living lab setting at BITS Pilani Goa Campus using IoT sensors.

**License:** [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
**Citation:** Kaushik, K. et al. (2023). SplitSmart: An Open Dataset for Enabling Research in Energy-Efficient Ductless-Split Air Conditioners. OpenEI.

---

## Contact

**Nils** | Data Analyst / Data Engineer  
[LinkedIn](https://linkedin.com/in/your-profile) · [Portfolio](https://your-website.com)
