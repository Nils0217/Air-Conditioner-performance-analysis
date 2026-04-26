# Step 3: Business Intelligence & Visualization

## Overview
Interactive dashboard analyzing IoT sensor data from 3 ductless-split AC units (AC01, AC02, AC03) at Room A200, Goa, India.  
Data period: March 2020 – August 2021 | ~510K records

---

## Tools Used

| Tool | Purpose | Audience |
|------|---------|----------|
| Power BI | Operations Overview + Performance Deep Dive | HR / Management |
| Streamlit | Environmental Correlation + Electricity Cost Analysis | Technical |

---

## Power BI Dashboard
**File:** `AC_Performance_Dashboard.pbix`

### Page 1 — Operations Overview
- 6 KPI cards: Avg Current, Anomaly Count, Avg Voltage, Avg Power Factor, Total Operating Hours, Total Records
- Monthly average current trend (3 units)
- Record distribution by season
- Environmental factors by season table
- Device capacity and anomaly summary table

### Page 2 — Performance Deep Dive
- Avg Power Factor monthly trend
- Load state distribution by device
- Average current by device and load state
- Hourly current heatmap (Matrix)

---

## Streamlit Dashboard
**Live App:** https://air-conditioner-performance-analysis-mjakk9w565r7rrdk5kddyl.streamlit.app/  
**File:** `app.py`

### Page 3 — Environmental Correlation
- Current distribution by external temperature (Box Plot)
- Avg Power Factor by humidity level (Line Chart)
- Average current by season and unit (Bar Chart)
- Current distribution by room temperature (Box Plot)

### Page 4 — Electricity Cost Analysis
- Best vs Worst case electricity cost by unit
- Cost breakdown by ToU tariff period (peak / off-peak / night)

**Sidebar filters:** AC Unit, Season

---

## Key Findings
- **AC01**: Healthy unit, stable PF ~0.97 across all seasons
- **AC02**: PF collapses to 0.48 during rainy season (Jun–Sep)
- **AC03**: Intermittent PF fault (0.37–0.55), worst during dry_hot + rainy seasons
- Peak-hour consumption accounts for the largest share of electricity costs
- Scheduling intensive cooling during off-peak/night tariff windows could yield meaningful savings

---

## Data Source
SplitSmart open-source dataset  
Cleaned CSV: [Goa_A200_AC_unit_performance_clean.csv](https://raw.githubusercontent.com/Nils0217/Air-Conditioner-performance-analysis/refs/heads/main/Cleaned%20dataset%20ready%20for%20analysis/Goa_A200_AC_unit_performance_clean.csv)