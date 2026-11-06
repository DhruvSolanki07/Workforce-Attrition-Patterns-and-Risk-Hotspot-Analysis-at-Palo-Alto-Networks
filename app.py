import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="NEXUS | Workforce Intelligence", page_icon="◈", layout="wide", initial_sidebar_state="expanded")

DATA_PATH = Path(__file__).parent / "Palo Alto Networks.csv"
NAVY = "#080D18"
CYAN = "#48D7E8"
PURPLE = "#9B8CFF"
PINK = "#FF6B91"
GREEN = "#5DE2A5"
MUTED = "#9AA9BE"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--bg:#080D18;--panel:#101827;--line:rgba(148,163,184,.15);--cyan:#48D7E8;--muted:#9AA9BE}
html,body,[class*="css"]{font-family:'Manrope',sans-serif}
.stApp{background:radial-gradient(ellipse at 15% 0%,rgba(36,91,130,.18),transparent 38%),linear-gradient(135deg,#080D18 0%,#0A1020 55%,#0B1020 100%);color:#E8F0FA}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0D1727,#0A1120);border-right:1px solid var(--line)}
[data-testid="stSidebar"] *{color:#DCE8F5}
.block-container{padding-top:1.7rem;padding-bottom:3rem;max-width:1500px}
h1,h2,h3{letter-spacing:-.04em}
.hero{padding:26px 30px;border:1px solid rgba(72,215,232,.24);border-radius:22px;background:linear-gradient(110deg,rgba(20,54,76,.68),rgba(24,24,53,.62));box-shadow:0 18px 60px rgba(0,0,0,.22);margin-bottom:22px;position:relative;overflow:hidden}
.hero:after{content:'◈';position:absolute;right:35px;top:-25px;font-size:150px;color:rgba(72,215,232,.07)}
.eyebrow{font:500 11px 'DM Mono';letter-spacing:.18em;color:var(--cyan);text-transform:uppercase}
.hero h1{font-size:34px;margin:8px 0 5px;color:#F5FAFF}
.hero p{color:#A9B9CC;margin:0;font-size:14px}
.metric{background:linear-gradient(145deg,rgba(20,31,49,.96),rgba(13,22,37,.96));border:1px solid var(--line);border-radius:17px;padding:17px 18px;min-height:118px;box-shadow:0 12px 35px rgba(0,0,0,.14)}
.metric-label{font-size:11px;letter-spacing:.12em;color:#9AA9BE;text-transform:uppercase;font-weight:700}
.metric-value{font-size:30px;font-weight:800;letter-spacing:-.05em;color:#F2F7FC;margin-top:7px}
.metric-sub{font-size:11px;color:#91A3B9;margin-top:2px}
.panel{background:rgba(16,24,39,.78);border:1px solid var(--line);border-radius:18px;padding:18px 20px}
.section-kicker{font:500 10px 'DM Mono';letter-spacing:.16em;color:var(--cyan);text-transform:uppercase;margin-bottom:4px}
.small-note{color:#91A3B9;font-size:12px}
div[data-testid="stSelectbox"]>label,div[data-testid="stSlider"]>label{color:#B8C7D8;font-size:12px;font-weight:700}
.stButton>button{background:linear-gradient(90deg,#147D91,#6457B8);color:white;border:0;border-radius:10px;font-weight:700}
.stDownloadButton>button{background:#14263A;color:#D9F8FC;border:1px solid rgba(72,215,232,.3);border-radius:10px}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:12px}
hr{border-color:var(--line)}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df.columns = [c.strip() for c in df.columns]
    if df["Attrition"].dtype == "object":
        df["Attrition"] = df["Attrition"].astype(str).str.strip().str.lower().map({"yes":1,"no":0})
    df["Attrition"] = pd.to_numeric(df["Attrition"], errors="coerce")
    df = df.dropna(subset=["Attrition","Department","JobRole","Age","YearsAtCompany"]).copy()
    df["Attrition"] = df["Attrition"].astype(int)
    df["AttritionLabel"] = df["Attrition"].map({1:"Exited",0:"Retained"})
    df["AgeGroup"] = pd.cut(df["Age"], bins=[0,25,35,45,55,100], labels=["Under 25","25–34","35–44","45–54","55+"])
    df["TenureBand"] = pd.cut(df["YearsAtCompany"], bins=[-1,1,3,5,10,100], labels=["0–1 years","2–3 years","4–5 years","6–10 years","10+ years"])
    df["ExperienceStage"] = pd.cut(df["TotalWorkingYears"], bins=[-1,3,10,100], labels=["Early career","Mid career","Experienced"])
    return df

df = load_data()
total = len(df)
st.sidebar.markdown("<div class='eyebrow'>NEXUS / PEOPLE ANALYTICS</div><h2 style='margin:4px 0 0'>◈ Workforce<br>Intelligence</h2><p style='font-size:11px;color:#8FA2B9'>ATTRITION MONITORING SYSTEM · v1.0</p>", unsafe_allow_html=True)
page = st.sidebar.radio("NAVIGATION", ["Command Center","Department & Role Hotspots","People & Demographics","Tenure & Workload","Data Explorer","Research Notes"], label_visibility="visible")
st.sidebar.markdown("---")
st.sidebar.markdown("<div class='eyebrow'>GLOBAL FILTERS</div>", unsafe_allow_html=True)
departments = sorted(df["Department"].dropna().unique())
roles = sorted(df["JobRole"].dropna().unique())
sel_dept = st.sidebar.multiselect("Department", departments, default=departments)
sel_role = st.sidebar.multiselect("Job role", roles, default=roles)
age_min, age_max = int(df.Age.min()), int(df.Age.max())
age_range = st.sidebar.slider("Age range", age_min, age_max, (age_min,age_max))
ten_min, ten_max = int(df.YearsAtCompany.min()), int(df.YearsAtCompany.max())
tenure_range = st.sidebar.slider("Tenure at company (years)", ten_min, ten_max, (ten_min,ten_max))
overtime_opt = st.sidebar.selectbox("Overtime", ["All","Yes","No"])
travel_opt = st.sidebar.selectbox("Business travel", ["All"] + sorted(df.BusinessTravel.dropna().unique().tolist()))
f = df[df.Department.isin(sel_dept) & df.JobRole.isin(sel_role) & df.Age.between(*age_range) & df.YearsAtCompany.between(*tenure_range)].copy()
if overtime_opt != "All": f = f[f.OverTime == overtime_opt]
if travel_opt != "All": f = f[f.BusinessTravel == travel_opt]
if f.empty:
    st.warning("No employees match the selected filters. Adjust the filters in the sidebar.")
    st.stop()

def metric(label, value, sub):
    st.markdown(f"<div class='metric'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div><div class='metric-sub'>{sub}</div></div>", unsafe_allow_html=True)

def chart_theme(fig, height=340):
    fig.update_layout(height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Manrope",color="#C7D4E4",size=11), margin=dict(l=12,r=12,t=38,b=12),
        legend=dict(bgcolor="rgba(0,0,0,0)",orientation="h",y=1.12),
        xaxis=dict(gridcolor="rgba(148,163,184,.10)",zerolinecolor="rgba(148,163,184,.12)"),
        yaxis=dict(gridcolor="rgba(148,163,184,.10)",zerolinecolor="rgba(148,163,184,.12)"))
    return fig

def header(kicker,title,desc):
    st.markdown(f"<div class='hero'><div class='eyebrow'>{kicker}</div><h1>{title}</h1><p>{desc}</p></div>",unsafe_allow_html=True)

header("WORKFORCE SIGNALS / LIVE ANALYTICS", {
"Command Center":"Attrition Command Center",
"Department & Role Hotspots":"Where talent is leaving",
"People & Demographics":"Who is most affected?",
"Tenure & Workload":"Career stage & workload signals",
"Data Explorer":"Explore the workforce dataset",
"Research Notes":"Methodology & decision brief"
}[page], {
"Command Center":"A high-level view of workforce exits, retention and the signals behind employee movement.",
"Department & Role Hotspots":"Compare attrition rates across organizational functions and job families.",
"People & Demographics":"Explore patterns across age, gender, education and marital status.",
"Tenure & Workload":"Understand how company tenure, overtime and travel relate to employee exits.",
"Data Explorer":"Inspect, filter and export the underlying employee-level records.",
"Research Notes":"Definitions, analytical assumptions, limitations and recommended next steps."
}[page])

exits=int(f.Attrition.sum()); retained=len(f)-exits; rate=exits/len(f)*100
if page=="Command Center":
    c=st.columns(4)
    with c[0]: metric("Employees in scope",f"{len(f):,}",f"of {total:,} records")
    with c[1]: metric("Attrition rate",f"{rate:.1f}%",f"{exits:,} exited employees")
    with c[2]: metric("Retention rate",f"{100-rate:.1f}%",f"{retained:,} retained employees")
    with c[3]: metric("Average tenure",f"{f.YearsAtCompany.mean():.1f} yrs","years at the organization")
    st.markdown("")
    left,right=st.columns([1,1.35])
    with left:
        st.markdown("<div class='panel'><div class='section-kicker'>01 / WORKFORCE OUTCOME</div><h3>Retained vs exited</h3></div>",unsafe_allow_html=True)
        fig=go.Figure(go.Pie(labels=["Retained","Exited"],values=[retained,exits],hole=.72,marker=dict(colors=[CYAN,PINK]),textinfo="label+percent",sort=False))
        fig.update_layout(height=330,paper_bgcolor="rgba(0,0,0,0)",font_color="#DCE8F5",showlegend=False,annotations=[dict(text=f"{rate:.1f}%",x=.5,y=.5,font_size=27,showarrow=False,font_color="#F5FAFF")],margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig,use_container_width=True)
    with right:
        st.markdown("<div class='panel'><div class='section-kicker'>02 / DEPARTMENT SIGNAL</div><h3>Attrition rate by department</h3></div>",unsafe_allow_html=True)
        d=f.groupby("Department",observed=False).agg(Employees=("Attrition","size"),Exits=("Attrition","sum")).reset_index()
        d["Attrition rate"]=d.Exits/d.Employees*100
        fig=px.bar(d,x="Department",y="Attrition rate",text=d["Attrition rate"].map(lambda x:f"{x:.1f}%"),color="Attrition rate",color_continuous_scale=["#287D91","#48D7E8","#FF6B91"])
        fig.update_traces(textposition="outside")
        chart_theme(fig,330); fig.update_layout(coloraxis_showscale=False,yaxis_title="Attrition rate (%)",xaxis_title="")
        st.plotly_chart(fig,use_container_width=True)
    a,b=st.columns(2)
    with a:
        st.markdown("<div class='section-kicker'>03 / EXIT PROFILE</div><h3>Age group distribution</h3>",unsafe_allow_html=True)
        ag=f.groupby("AgeGroup",observed=False).agg(Employees=("Attrition","size"),Exits=("Attrition","sum")).reset_index()
        ag["Rate"]=ag.Exits/ag.Employees*100
        fig=px.bar(ag,x="AgeGroup",y="Rate",color="Rate",color_continuous_scale=["#287D91","#9B8CFF","#FF6B91"])
        chart_theme(fig,300); fig.update_layout(coloraxis_showscale=False,yaxis_title="Attrition rate (%)",xaxis_title="")
        st.plotly_chart(fig,use_container_width=True)
    with b:
        st.markdown("<div class='section-kicker'>04 / CAREER STAGE</div><h3>Attrition by tenure band</h3>",unsafe_allow_html=True)
        tg=f.groupby("TenureBand",observed=False).agg(Employees=("Attrition","size"),Exits=("Attrition","sum")).reset_index()
        tg["Rate"]=tg.Exits/tg.Employees*100
        fig=px.line(tg,x="TenureBand",y="Rate",markers=True,line_shape="spline")
        fig.update_traces(line_color=PURPLE,marker=dict(size=9,color=CYAN))
        chart_theme(fig,300); fig.update_layout(yaxis_title="Attrition rate (%)",xaxis_title="")
        st.plotly_chart(fig,use_container_width=True)
    st.markdown("<div class='small-note'>Rates are calculated within the currently selected population. A small group can show a volatile rate; always consider the employee count alongside the percentage.</div>",unsafe_allow_html=True)

elif page=="Department & Role Hotspots":
    g=f.groupby(["Department","JobRole"],observed=False).agg(Employees=("Attrition","size"),Exits=("Attrition","sum")).reset_index()
    g["Attrition rate"]=g.Exits/g.Employees*100
    g=g[g.Employees>0]
    l,r=st.columns([1.25,1])
    with l:
        st.markdown("<div class='section-kicker'>ROLE × FUNCTION</div><h3>Attrition intensity map</h3>",unsafe_allow_html=True)
        piv=g.pivot(index="JobRole",columns="Department",values="Attrition rate").fillna(0)
        fig=px.imshow(piv,text_auto=".1f",aspect="auto",color_continuous_scale=["#12243A","#287D91","#48D7E8","#FF6B91"],labels=dict(color="Rate (%)"))
        chart_theme(fig,470); fig.update_layout(coloraxis_colorbar=dict(title="Rate (%)"))
        st.plotly_chart(fig,use_container_width=True)
    with r:
        st.markdown("<div class='section-kicker'>HIGHEST OBSERVED RATES</div><h3>Role-level hotspots</h3>",unsafe_allow_html=True)
        top=g.sort_values(["Attrition rate","Employees"],ascending=[False,False]).head(10)
        fig=px.bar(top.sort_values("Attrition rate"),x="Attrition rate",y="JobRole",orientation="h",color="Attrition rate",color_continuous_scale=["#287D91","#9B8CFF","#FF6B91"],hover_data=["Department","Employees","Exits"])
        chart_theme(fig,470); fig.update_layout(coloraxis_showscale=False,xaxis_title="Attrition rate (%)",yaxis_title="")
        st.plotly_chart(fig,use_container_width=True)
    st.markdown("### Department scorecard")
    dept=f.groupby("Department").agg(Employees=("Attrition","size"),Exits=("Attrition","sum")).reset_index()
    dept["Attrition rate (%)"]=(dept.Exits/dept.Employees*100).round(1)
    st.dataframe(dept.sort_values("Attrition rate (%)",ascending=False),use_container_width=True,hide_index=True)

elif page=="People & Demographics":
    col1,col2=st.columns(2)
    for col,field,title in [(col1,"AgeGroup","Age cohort"),(col2,"Gender","Gender")]:
        with col:
            x=f.groupby(field,observed=False).agg(Employees=("Attrition","size"),Exits=("Attrition","sum")).reset_index()
            x["Rate"]=x.Exits/x.Employees*100
            st.markdown(f"<div class='section-kicker'>DEMOGRAPHIC LENS</div><h3>{title}</h3>",unsafe_allow_html=True)
            fig=px.bar(x,x=field,y="Rate",color="Rate",color_continuous_scale=["#287D91","#48D7E8","#FF6B91"],hover_data=["Employees","Exits"])
            chart_theme(fig,320); fig.update_layout(coloraxis_showscale=False,yaxis_title="Attrition rate (%)",xaxis_title="")
            st.plotly_chart(fig,use_container_width=True)
    col1,col2=st.columns(2)
    for col,field,title in [(col1,"EducationField","Education field"),(col2,"MaritalStatus","Marital status")]:
        with col:
            x=f.groupby(field).agg(Employees=("Attrition","size"),Exits=("Attrition","sum")).reset_index()
            x["Rate"]=x.Exits/x.Employees*100
            st.markdown(f"<div class='section-kicker'>COMPOSITION SIGNAL</div><h3>{title}</h3>",unsafe_allow_html=True)
            fig=px.bar(x,x=field,y="Rate",color="Rate",color_continuous_scale=["#287D91","#9B8CFF","#FF6B91"])
            chart_theme(fig,320); fig.update_layout(coloraxis_showscale=False,yaxis_title="Attrition rate (%)",xaxis_title="")
            st.plotly_chart(fig,use_container_width=True)
    st.caption("Demographic differences are descriptive, not causal. Do not use protected or sensitive characteristics to make individual employment decisions.")

elif page=="Tenure & Workload":
    c1,c2=st.columns(2)
    with c1:
        st.markdown("<div class='section-kicker'>CAREER JOURNEY</div><h3>Attrition by company tenure</h3>",unsafe_allow_html=True)
        x=f.groupby("TenureBand",observed=False).agg(Employees=("Attrition","size"),Exits=("Attrition","sum")).reset_index()
        x["Rate"]=x.Exits/x.Employees*100
        fig=px.bar(x,x="TenureBand",y="Rate",color="Rate",color_continuous_scale=["#287D91","#48D7E8","#FF6B91"],hover_data=["Employees","Exits"])
        chart_theme(fig,340); fig.update_layout(coloraxis_showscale=False,yaxis_title="Attrition rate (%)",xaxis_title="")
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown("<div class='section-kicker'>WORKLOAD SIGNAL</div><h3>Overtime vs attrition</h3>",unsafe_allow_html=True)
        x=f.groupby("OverTime").agg(Employees=("Attrition","size"),Exits=("Attrition","sum")).reset_index()
        x["Rate"]=x.Exits/x.Employees*100
        fig=px.bar(x,x="OverTime",y="Rate",color="OverTime",color_discrete_map={"Yes":PINK,"No":CYAN},text=x["Rate"].map(lambda v:f"{v:.1f}%"))
        fig.update_traces(textposition="outside")
        chart_theme(fig,340); fig.update_layout(showlegend=False,yaxis_title="Attrition rate (%)",xaxis_title="")
        st.plotly_chart(fig,use_container_width=True)
    c1,c2=st.columns(2)
    with c1:
        st.markdown("<div class='section-kicker'>MOBILITY</div><h3>Business travel frequency</h3>",unsafe_allow_html=True)
        x=f.groupby("BusinessTravel").agg(Employees=("Attrition","size"),Exits=("Attrition","sum")).reset_index()
        x["Rate"]=x.Exits/x.Employees*100
        fig=px.bar(x,x="BusinessTravel",y="Rate",color="Rate",color_continuous_scale=["#287D91","#9B8CFF","#FF6B91"])
        chart_theme(fig,320); fig.update_layout(coloraxis_showscale=False,yaxis_title="Attrition rate (%)",xaxis_title="")
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.markdown("<div class='section-kicker'>CAREER PROGRESSION</div><h3>Years since last promotion</h3>",unsafe_allow_html=True)
        x=f.groupby("YearsSinceLastPromotion").agg(Employees=("Attrition","size"),Exits=("Attrition","sum")).reset_index()
        x["Rate"]=x.Exits/x.Employees*100
        fig=px.scatter(x,x="YearsSinceLastPromotion",y="Rate",size="Employees",color="Rate",color_continuous_scale=["#287D91","#FF6B91"],hover_data=["Employees","Exits"])
        chart_theme(fig,320); fig.update_layout(coloraxis_showscale=False,yaxis_title="Attrition rate (%)",xaxis_title="Years since last promotion")
        st.plotly_chart(fig,use_container_width=True)
    st.markdown("### Workload comparison")
    w=f.groupby(["OverTime","BusinessTravel"]).agg(Employees=("Attrition","size"),Exits=("Attrition","sum")).reset_index()
    w["Attrition rate (%)"]=(w.Exits/w.Employees*100).round(1)
    st.dataframe(w,use_container_width=True,hide_index=True)

elif page=="Data Explorer":
    st.markdown("<div class='section-kicker'>EMPLOYEE RECORDS</div><h3>Filtered data table</h3>",unsafe_allow_html=True)
    show_cols=[c for c in df.columns if c!="AttritionLabel"]
    st.caption(f"Showing {len(f):,} records after global filters.")
    st.dataframe(f[show_cols],use_container_width=True,hide_index=True,height=470)
    st.download_button("↓ Download filtered CSV",f[show_cols].to_csv(index=False).encode("utf-8"),"nexus_filtered_employee_data.csv","text/csv")
    st.markdown("### Data quality snapshot")
    q=pd.DataFrame({"Check":["Rows loaded","Columns loaded","Duplicate rows","Missing cells","Attrition values"],"Result":[len(df),len(df.columns),int(df.duplicated().sum()),int(df.isna().sum().sum()),", ".join(map(str,sorted(df.Attrition.unique()))) ]})
    st.dataframe(q,use_container_width=True,hide_index=True)

else:
    st.markdown("### Executive summary")
    st.write("This diagnostic analysis examines employee attrition across organizational, demographic, career-stage and workload dimensions. It is intended to help HR teams identify where further investigation may be valuable—not to infer why an individual employee leaves.")
    st.markdown("### KPI definitions")
    st.markdown("""
    - **Attrition rate:** employees with Attrition = 1 divided by all employees in the selected population.
    - **Department / role attrition:** exits within a group divided by all records in that group.
    - **Early-tenure attrition:** rate for employees in the first tenure band (0–1 years); adjust the band definition to match business policy.
    - **Workload comparison:** descriptive rate comparison across overtime and travel categories. It is not a causal workload index.
    """)
    st.markdown("### Recommended analysis workflow")
    st.markdown("""
    1. Validate source definitions, coding, missingness and duplicate records.
    2. Establish the overall attrition baseline and employee counts.
    3. Compare department and role rates while checking small sample sizes.
    4. Examine tenure, promotion and satisfaction patterns.
    5. Validate potential drivers through employee listening, exit interviews and manager-level context.
    6. Pilot targeted retention interventions and monitor outcomes over time.
    """)
    st.markdown("### Important limitations")
    st.warning("The supplied file has 1,470 rows and 31 fields and uses numeric Attrition values (0/1). Its structure resembles the public IBM HR Analytics Attrition dataset. The data does not establish that the records belong to Palo Alto Networks. Treat the company name as the project scenario unless source provenance is independently verified.")
    st.markdown("""
    - The data is cross-sectional and does not provide a time series of employee exits.
    - Correlation and group-rate differences do not prove causation.
    - Small groups can have unstable percentages; always show denominators.
    - Demographic fields should be used only for aggregate fairness auditing, never individual employment decisions.
    - This dashboard does not predict individual attrition or assign employee risk scores.
    """)
    st.markdown("### Suggested retention actions")
    st.markdown("""
    - Review workload allocation and overtime expectations with affected teams.
    - Strengthen onboarding and manager check-ins during the first 12 months.
    - Make career paths, internal mobility and promotion criteria more transparent.
    - Conduct structured stay interviews and analyze exit feedback.
    - Evaluate interventions using pre/post measures and appropriate comparison groups.
    """)

st.markdown("---")
st.markdown("<div style='display:flex;justify-content:space-between;color:#71839B;font-size:11px'><span>◈ NEXUS WORKFORCE INTELLIGENCE</span><span>DIAGNOSTIC ANALYTICS · NOT AN INDIVIDUAL RISK SYSTEM</span></div>",unsafe_allow_html=True)
