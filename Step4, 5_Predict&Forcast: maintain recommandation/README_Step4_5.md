# Step 4 & 5 — Data Science Analysis & Maintenance Recommendations
### SplitSmart Dataset | Goa A200 Facility | AC01 · AC02 · AC03

---

## Overview

This notebook covers the modeling and recommendation phases of the SplitSmart IoT analysis project.
Three ductless-split AC units at a facility in Goa, India were analyzed using ~503,000 sensor readings
spanning March 2020 to August 2021.

The work is split into two parts:

- **Step 4** — Data science analysis: anomaly detection, PF monitoring, and power regression
- **Step 5** — Actionable maintenance and operational recommendations derived from the findings

---

## Dataset

| Property | Value |
|----------|-------|
| Source | [SplitSmart open dataset](https://github.com/Nils0217/Air-Conditioner-performance-analysis) |
| Records | 503,678 (after sensor_error removal) |
| Units | A200AC01, A200AC02, A200AC03 |
| Date range | 2020-03-09 to 2021-08-25 |
| Sampling interval | ~10 minutes |
| Location | Goa, India |

Cleaned dataset produced in Step 1 (ETL). Raw data is the open-source SplitSmart dataset.

---

## Notebook Structure

| Section | Method | Output |
|---------|--------|--------|
| 4.1 | Feature Engineering | 10 engineered features including lag, rolling stats, season encoding |
| 4.2 | Isolation Forest (per-unit) | Anomaly flags with dynamic contamination rates |
| 4.3 | Rule-Based Rolling Window | PF monitoring alert — Recall 0.99, Precision 1.00 |
| 4.4 | Regression (LR vs RF) | Real power prediction — RF R² > 0.95 |
| 5.1 | Unit status matrix | Per-unit health assessment and action plan |
| 5.2 | Scheduling recommendations | Peak/off-peak rotation, seasonal protocols |
| 5.3 | Energy cost estimation | kWh and INR cost by unit; PF repair savings |
| 5.4 | Priority action matrix | 8 actions ranked P1–P4 |

---

## Key Findings

### AC Unit Health at a Glance

| Unit | Status | PF Range | Priority |
|------|--------|----------|----------|
| AC01 | 🟢 Healthy | 0.95 – 0.99 | LOW |
| AC02 | 🟡 Degraded | 0.48 – 0.89 | HIGH |
| AC03 | 🔴 Severely Degraded | 0.37 – 0.55 | CRITICAL |

### Section 4.2 — Anomaly Detection
- Isolation Forest applied independently per unit using `current`, `voltage`, `power_factor`, `real_power`
- Contamination rate set dynamically per unit (union of high-current and PF-collapse signals)
- AC03 shows the highest anomaly concentration, peaking in dry_hot (Mar–May) and rainy (Jun–Sep) seasons
- AC01 anomaly rate is minimal — consistent with its healthy operating profile

### Section 4.3 — PF Monitoring Alert

> ⚠️ **Methodology note:** A Random Forest classifier was initially attempted.
> Investigation revealed that PF degradation follows a **burst pattern** —
> sudden, multi-month events driven by device-level faults, not environmental conditions.
> The ML model failed on time-based (Mote Carlo CV, TimeSeriesSplit CV) evaluation due to distribution shift between seasons.
>
> The final approach is a **rule-based rolling window alert**.
> This is **concurrent detection, not prediction** — it confirms sustained degradation
> after ~1 hour of onset. There is no advance warning component.
> High evaluation scores (Recall 0.99, Precision 1.00) reflect rule consistency
> with the label definition, not an independent learned signal.

| Unit | Recall | Precision | Threshold | Degraded % |
|------|--------|-----------|-----------|-----------|
| AC01 | — | — | None | 0.0% |
| AC02 | 0.955 | 1.000 | PF < 0.70 | 13.3% |
| AC03 | 0.999 | 1.000 | PF < 0.50 | 47.8% |

AC02 and AC03 require separate thresholds because their fault signatures differ:
AC02 shows intermittent moderate drops (PF 0.50–0.70); AC03 shows sustained severe collapse (PF < 0.50).

### Section 4.4 — Real Power Regression

| Model | MAE (W) | R² |
|-------|---------|-----|
| Linear Regression | higher | lower |
| Random Forest | lower | > 0.95 |

Random Forest captures the non-linear interactions between current, voltage, and power factor
that linear models cannot — particularly relevant given AC03's firmware-induced reading distortions.

### Section 5.3 — Energy Cost & PF Repair Savings

Estimated savings if AC02 and AC03 PF is restored to target (0.95):

| Unit | Avg PF | Estimated kWh Saved | Estimated INR Saved |
|------|--------|--------------------|--------------------|
| AC02 | 0.889 | 2,759 kWh | INR 22,073 |
| AC03 | 0.620 | 17,656 kWh | INR 141,247 |
| **Combined** | — | **20,415 kWh** | **INR 163,320** |

---

## Seasonal Framework

This project uses Goa's three-season climate model throughout:

| Season | Months | Characteristics |
|--------|--------|----------------|
| dry_hot | Mar – May | High external temp; peak cooling load |
| rainy | Jun – Sep | High humidity; AC02/AC03 fault-prone |
| cool | Oct – Feb | Moderate load; lowest degradation rates |

---

## Feature Engineering Summary

| Feature | Logic | Purpose |
|---------|-------|---------|
| `pf_degraded` | PF < 0.85 during active operation | Binary alert target |
| `rolling_pf_24h` | 144-reading rolling mean per unit | Trend smoothing |
| `ext_temp_lag6h` | External temp shifted 6 readings | Heat accumulation proxy |
| `ext_temp_rise` | Current temp minus lag6h temp | Temperature change rate |
| `ext_temp_median_72h` | 432-reading rolling median | Sustained heat baseline |
| `humidity_std_24h` | 144-reading rolling std | Weather volatility |
| `humidity_median_72h` | 432-reading rolling median | Sustained humidity baseline |
| `season_enc` | dry_hot=0, rainy=1, cool=2 | Season as ML input |
| `time_block` | Hour binned into 6 activity slots | Facility usage alignment |
| `temp_delta` | room_temp − external_temp | Cooling load pressure |

> **Deployment note:** Features with 72-hour windows require at least 72 hours of warm-up data.
> The monitoring rule should not be applied to the first 72 hours of a new unit's data stream.

---

## Priority Action Matrix

| Priority | Action | Unit | Timing |
|----------|--------|------|--------|
| P1 CRITICAL | Reflash / update firmware | AC03 | Immediate |
| P1 CRITICAL | Verify CT sensor wiring on-site | AC02 | Immediate |
| P2 HIGH | Pre-rainy-season preventive maintenance | AC02/AC03 | Annually — May |
| P2 HIGH | Pre-dry-hot capacitor inspection | AC03 | Annually — Feb |
| P2 HIGH | Implement peak-load rotation schedule | All | Immediate |
| P3 MEDIUM | Weekly PF monitoring report | AC02/AC03 | Ongoing |
| P3 MEDIUM | Quarterly filter cleaning | AC01 | Quarterly |
| P4 LOW | Evaluate PF correction capacitor install | AC02/AC03 | Next fiscal year |

---

## Project Steps

| Step | Topic | Status |
|------|-------|--------|
| 1 | ETL & Data Cleaning | ✅ Complete |
| 2 | Exploratory Data Analysis | ✅ Complete |
| 3 | BI Dashboard (Power BI + Streamlit) | ✅ Complete |
| **4** | **Data Science Modeling** | ✅ **Complete** |
| **5** | **Maintenance Recommendations** | ✅ **Complete** |

---

## Tools & Environment

- **Python 3.12** — pandas, numpy, scikit-learn, matplotlib, seaborn
- **Google Colab** — primary execution environment
- **GitHub** — dataset and notebook hosting

---

## Limitations & Honest Notes

- Dataset spans only 17 months (Mar 2020 – Aug 2021); multi-year patterns are not captured
- Section 4.3 alert is concurrent detection, not predictive — see methodology note above
- Energy cost figures use estimated INR rates and assume 10-minute sampling intervals
- AC01's significantly higher record count suggests AC02/AC03 may have had later IoT installation or data gaps
