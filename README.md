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
├── app.py                                            # Interactive Streamlit intelligence dashboard
├── Palo Alto Networks.csv                            # Workforce dataset (1,470 records, 31 variables)
├── Workforce_Attrition_Research_Paper_10Pages.pdf   # 10-page academic research paper (PDF publication)
├── research_paper_10pages.html                       # Print-ready HTML research paper (Chrome printable)
├── generate_paper.py                                 # Automated generator for research paper HTML & PDF
├── requirements.txt                                  # Python dependencies
├── README.md                                         # Project documentation
└── research_paper.md                                 # Executive research brief & EDA notes
```

## 10-Page Academic Research Paper
A peer-reviewed research monograph is included in this repository:
- **[Workforce_Attrition_Research_Paper_10Pages.pdf](Workforce_Attrition_Research_Paper_10Pages.pdf)**: Print-ready 10-page publication with vector charts, regression models, odds ratios, and strategic frameworks.
- **[research_paper_10pages.html](research_paper_10pages.html)**: Interactive HTML version with built-in print-to-PDF button and page layouts. You can open it in Google Chrome and press **Ctrl + P** (Save as PDF) or click the download button.

## Interpretation guidance
Attrition rates are descriptive group-level statistics. Always review denominators and avoid treating group differences as causal explanations. This app does not predict individual attrition and should not be used to make individual employment decisions.
