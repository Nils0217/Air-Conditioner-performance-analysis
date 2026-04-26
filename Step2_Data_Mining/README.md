# Step 2: Exploratory Data Analysis

**Tools:** Python · pandas · seaborn · MySQL · Google Colab  
**Data:** 510,000 records · 3 AC units (AC01, AC02, AC03) · 2020–2021

---

## Structure

| Section | Topic |
|---------|-------|
| 2.1 | Energy Consumption Pattern (hourly / monthly / seasonal) |
| 2.2 | Equipment Health Analysis (PF fault diagnosis, operating rate) |
| 2.3 | Environmental Correlation (temp, humidity vs power) |
| 2.4 | Electricity Cost Estimation (ToU tariff simulation) |

## Key Findings

- **AC03** power factor collapses to 0.37–0.55 during Mar–Sep; recovers in cool season → intermittent hardware fault
- **AC02** shuts down entirely in November (0% operating rate) → reactive downtime after fault events
- **AC01** healthy baseline — PF ~0.97 year-round
- Environmental conditions identical across all units → faults are hardware-driven, not environment-driven

## Notebook
`Step2_EDA_AC_Performance.ipynb`

← [Back to Project Overview](../README.md)
