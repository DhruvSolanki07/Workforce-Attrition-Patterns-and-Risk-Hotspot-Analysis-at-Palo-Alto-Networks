# NEXUS | Workforce Intelligence

An interactive Streamlit analytics project for exploring workforce attrition patterns across departments, roles, demographics, tenure and workload factors.

## Features
- Premium dark cybersecurity-inspired interface
- Global filters for department, job role, age, tenure, overtime and business travel
- Overview KPIs and retained-vs-exited distribution
- Department / job-role attrition heatmap and hotspot ranking
- Demographic analysis by age, gender, education field and marital status
- Tenure, overtime, travel and promotion analysis
- Filtered employee data explorer and CSV export
- Research notes, KPI definitions, limitations and recommended next steps

## Dataset
Place `Palo Alto Networks.csv` in the same folder as `app.py`. The included file contains 1,470 rows and 31 columns. The provided data uses `Attrition` encoded as 0/1.

**Data provenance warning:** The schema and row count resemble the public IBM HR Analytics Attrition dataset. Do not represent these records as verified Palo Alto Networks employee data unless provenance is confirmed. The project therefore treats Palo Alto Networks as a business-case scenario.

## Run locally (Windows)
1. Install Python 3.10 or newer.
2. Open PowerShell in this project folder.
3. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

5. Launch:

```powershell
streamlit run app.py
```

The app opens in your browser, usually at `http://localhost:8501`.

## Project structure

```text
NEXUS_Workforce_Intelligence/
├── app.py
├── Palo Alto Networks.csv
├── requirements.txt
├── README.md
└── research_paper.md
```

## Interpretation guidance
Attrition rates are descriptive group-level statistics. Always review denominators and avoid treating group differences as causal explanations. This app does not predict individual attrition and should not be used to make individual employment decisions.
