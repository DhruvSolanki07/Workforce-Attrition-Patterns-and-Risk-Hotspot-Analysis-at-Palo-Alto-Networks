# Workforce Attrition Patterns and Risk Hotspot Analysis
## NEXUS Workforce Intelligence — Research Paper / EDA Brief

### Abstract
This project develops a descriptive workforce analytics workflow to examine employee attrition across organizational functions, job roles, demographic cohorts, career tenure and workload indicators. A Streamlit dashboard provides interactive exploration and filtering. The analysis is diagnostic: it identifies patterns that warrant further investigation, but does not establish causality or predict individual employee exits.

### 1. Introduction
Employee attrition can create recruitment costs, knowledge loss, delivery disruption and pressure on remaining teams. Aggregate analysis can help HR leaders identify where attrition is concentrated and prioritize deeper qualitative investigation. This project frames the analysis around Palo Alto Networks as a cybersecurity-sector business case.

### 2. Dataset and provenance
The supplied CSV contains 1,470 records and 31 fields. Fields include Age, Attrition, BusinessTravel, Department, DistanceFromHome, Education, EducationField, EnvironmentSatisfaction, Gender, JobInvolvement, JobLevel, JobRole, JobSatisfaction, MaritalStatus, MonthlyIncome, NumCompaniesWorked, OverTime, TotalWorkingYears, TrainingTimesLastYear, WorkLifeBalance, YearsAtCompany, YearsInCurrentRole, YearsSinceLastPromotion and YearsWithCurrManager.

The file uses numeric Attrition values: 1 indicates exited and 0 indicates retained. Its structure and record count resemble the commonly circulated IBM HR Analytics Attrition dataset. The supplied file does not independently verify that the employees worked for Palo Alto Networks. Accordingly, company-specific conclusions must be treated as a scenario-based exercise unless data provenance is confirmed.

### 3. Research questions
1. Which departments and roles show the highest observed attrition rates?
2. How do rates vary across age and education cohorts?
3. Is attrition concentrated in early company tenure?
4. How do overtime and business travel categories compare?
5. Does time since last promotion show an association with attrition?

### 4. Methodology
- Load the CSV and standardize column names.
- Validate the attrition field and remove records missing core analysis fields.
- Derive age groups, company-tenure bands and experience stages.
- Calculate the overall attrition rate as exits divided by all included employee records.
- Calculate group attrition as exits within a group divided by all records in that group.
- Compare departments, roles, demographic groups, tenure bands and workload categories.
- Present results with interactive Plotly visualizations and a filtered data table.

### 5. KPI definitions
**Overall attrition rate (%)** = (number of exited employees / total employees) × 100.

**Department attrition rate (%)** = (exited employees in department / all employees in department) × 100.

**Role attrition rate (%)** = (exited employees in role / all employees in role) × 100.

**Early-tenure attrition rate (%)** = (exited employees in defined early-tenure band / all employees in that band) × 100.

Overtime and travel comparisons are presented as separate group rates. They are not combined into a proprietary workload index because no validated weighting scheme is supplied.

### 6. Dashboard modules
- Command Center: population size, attrition and retention rates, department and tenure comparisons.
- Department & Role Hotspots: role-by-department heatmap, high-rate role ranking and department scorecard.
- People & Demographics: age, gender, education-field and marital-status comparisons.
- Tenure & Workload: company tenure, overtime, travel and promotion timing.
- Data Explorer: filtered records, data-quality summary and CSV export.
- Research Notes: definitions, limitations and suggested actions.

### 7. Interpretation and limitations
Group-level differences are descriptive. They do not demonstrate that a characteristic causes an employee to leave. The dataset is cross-sectional and does not provide exit dates, longitudinal employee histories, manager context, exit-interview text or a verified company identifier. Rates in small groups may be unstable; denominators must accompany percentages. Demographic variables should only be used for aggregate fairness auditing and must not drive individual employment decisions. No individual risk scores or predictive model are included.

### 8. Recommendations for HR stakeholders
1. Investigate high-rate teams with sufficient sample sizes before acting.
2. Review overtime distribution, staffing levels and delivery pressure.
3. Improve onboarding, mentoring and manager check-ins in early tenure.
4. Make promotion criteria and internal career paths transparent.
5. Conduct structured stay interviews and categorize exit feedback.
6. Pilot interventions and monitor attrition, engagement and workload indicators over time.
7. Validate all findings with current, consented, organization-specific HR data.

### 9. Conclusion
NEXUS provides a practical foundation for workforce attrition exploration. Its interactive filters and visual summaries help identify where further investigation may be useful. The next stage should validate data provenance, combine quantitative signals with employee feedback, and evaluate targeted retention interventions using longitudinal organizational data.
