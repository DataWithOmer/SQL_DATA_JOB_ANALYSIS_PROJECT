import streamlit as st
import pandas as pd
import plotly.express as px
from db_conn import get_connection

# STREAMLIT CONFIGURATION
st.set_page_config(
    page_title="LinkedInsights",
    page_icon="💼",
    layout="wide")

# Enhanced CSS styling
st.markdown(""" <style>
/* App Background */
.stApp { background-color: #020617; }

header[data-testid="stHeader"] {
            height: 0px !important;
            background: transparent !important;
            display: none;}

.block-container {padding-top: 2rem !important;}

/* Main Page Panel */
.stAppViewContainer { background-color: #020617; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #2c456b !important;
    border-right: 2.5px solid rgba(255, 255, 255, 0.1); }

/* Metrics Card */
[data-testid="stMetric"] {
    background-color: #ffffff !important;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    border-top: 5px solid #10b981 !important;
    text-align: center; }

/* Metric Heading */
[data-testid="stMetricLabel"] p {
    color: #000000 !important;
    font-size: 18px !important;
    font-weight: 700 !important; }

/* Metric Value */
[data-testid="stMetricValue"] div {
    color: #10b981 !important;
    font-size: 32px !important;
    font-weight: 900 !important; }

h1, h2, h3 {
    color: #ffffff !important;
    font-weight: 800; }

/* Custom Plotly Tooltip Styling */
.hoverlayer .hovertext {
    font-family: 'Inter', sans-serif !important; }

# Reduce Gap Bw "Selct Salary Basis" & filters
[data-testid="stMain"] div.stElementContainer:has(label[data-testid="stWidgetLabel"]) {
    margin-top: 25px !important; }

[data-testid="stMain"] label[data-testid="stWidgetLabel"] p {
    font-size: 18px !important; font-weight: 700 !important; margin-bottom: -30px !important; }

[data-testid="stMain"] .stRadio > div[role="radiogroup"] {
    margin-top: 30px !important; }
    
/* Reducing gap bw Skills Category & radio Buttons */
.tight-header {
    margin-top: 30px !important;
    margin-bottom: 0px !important;
    padding-bottom: 0px !important; }

[data-testid="stMain"] .stRadio {margin-top: -40px !important;}
    
/* Reduce gap bw Select Country & dropdown label */
[data-testid="stMain"] div[data-testid="stSelectbox"] label p {margin-bottom: -15px !important; font-size: 18px !important;}
    
 [data-testid="stMain"] div[data-testid="stSelectbox"] > div {margin-top: -3px !important;}   
</style> """, unsafe_allow_html=True)

# Database connection with caching
@st.cache_resource
def init_connection():
    return get_connection()

def load_data(query):
    """ Helper function to execute SQL query and return a DataFrame"""
    try:
        conn = init_connection()
        df = conn.query(query)
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()

# dynamic country fetching from db
@st.cache_data
def load_countries():
    """ Fetch all unique countries directly from the database """
    df = load_data("""
        SELECT DISTINCT job_country
        FROM job_postings_fact
        WHERE job_country IS NOT NULL
        ORDER BY job_country ASC
    """)
    return df['job_country'].tolist() if not df.empty else []

COUNTRY_LIST = load_countries()

# SIDEBAR: Discovery filters and navigation
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/LinkedIn_logo_initials.png/600px-LinkedIn_logo_initials.png", width=75)
st.sidebar.title("🔍 Discovery Filters")

job_filter = st.sidebar.selectbox(
    "**Select Job Category**", 
    ["All", "Data Analyst", "Data Scientist", "Data Engineer", "Business Analyst", "Machine Learning Engineer", "Senior Data Analyst",
     "Senior Data Engineer", "Senior Data Scientist", "Software Engineer", "Cloud Engineer"] )

location_filter = st.sidebar.radio(
    "**Location Type**",["Global", "Remote Only"] )

st.sidebar.markdown("<div style='margin-top:-30px;'></div>", unsafe_allow_html=True)
page = st.sidebar.selectbox( 
    "**Navigate To**",[  "📑 Project Overview", "📊 Market Overview", "💰 Salary Insights"  ,"🛠️ Skill Economics", "🏢 Top Hiring Companies" ])

# Dynamic SQL Where Clause
where_clause = "WHERE 1=1"
if job_filter != "All":
    where_clause += f" AND job_title_short = '{job_filter}'"
if location_filter == "Remote Only":
    where_clause += " AND job_work_from_home IS TRUE"
    
# PAGE 1: Project Overview 
if page == "📑 Project Overview":
    st.title("💼 LinkedIn Job Market Dashboard – 2023")
    st.markdown('<hr style="margin-top:10px; margin-bottom:25px; border: 1px solid rgba(255,255,255,0.1)">', unsafe_allow_html=True)

    # About the Project
    st.markdown("#### 🎯 About This Project")
    st.markdown("""
    <div style='background-color:#0f172a; border-left: 4px solid #10b981; padding: 18px 22px; border-radius: 8px; margin-bottom: 20px;'>
        <p style='color:#e2e8f0; font-size:15px; line-height:1.8; margin:0;'>
        This dashboard analyzes over <b style='color:#10b981;'>700,000+ LinkedIn job postings</b> from 2023 to uncover
        data-driven insights about the job market for data professionals. It explores salary benchmarks,
        in-demand skills, skill combinations, and top-paying employers — helping job seekers and analysts
        make smarter career decisions. Each page comes with filters for job category, location type,
        and country so you can slice the data most relevant to you.
        <br>
        This project was inspired by the course <b style='color:#10b981;'>SQL For Data Analytics</b> course by
        <b style='color:#10b981;'>Luke Barousse</b> — a huge shoutout to him for the dataset,
        the guidance, and providing these kinds of courses for free of cost.
        </p> </div> """, unsafe_allow_html=True)

    # What You Can Explore
    st.markdown("#### 🗺️ What You Can Explore")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style='background-color:#0f172a; border-top: 3px solid #10b981; padding:20px; border-radius:8px; height:140px;'>
            <h5 style='color:#10b981; margin-top:0;'>📊 Market Overview</h4>
            <p style='color:#94a3b8; font-size:14.5px;'>Top demanded skills, job volume, remote availability, and salary benchmarking across roles.</p>
        </div> """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background-color:#0f172a; border-top: 3px solid #10b981; padding:20px; border-radius:8px; height:140px;'>
            <h5 style='color:#10b981; margin-top:0;'>💰 Salary Insights</h4>
            <p style='color:#94a3b8; font-size:14.5px;'>Highest-paying skills and roles, filterable by country, job type, and salary basis.</p>
        </div> """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        <div style='background-color:#0f172a; border-top: 3px solid #10b981; padding:20px; border-radius:8px; height:140px;'>
            <h5 style='color:#10b981; margin-top:0;'>🛠️ Skill Economics</h4>
            <p style='color:#94a3b8; font-size:14.5px;'>Optimal skills by demand vs salary, and skill co-occurrence patterns to guide learning paths.</p>
        </div> """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div style='background-color:#0f172a; border-top: 3px solid #10b981; padding:20px; border-radius:8px; height:140px;'>
            <h5 style='color:#10b981; margin-top:0;'>🏢 Top Employers</h4>
            <p style='color:#94a3b8; font-size:14.5px;'>Companies offering the highest average salaries, filterable by country and salary type.</p>
        </div> """, unsafe_allow_html=True)

    # Dataset & Tech Stack 
    st.markdown("<div style='margin-top:25px;'></div>", unsafe_allow_html=True)
    st.markdown("#### 🗄️ Dataset & Tech Stack")
    col_data, col_tech = st.columns([1, 1])

    with col_data:
        st.markdown("""
        <div style='background-color:#0f172a; border-left: 4px solid #10b981; padding:18px; border-radius:8px;'>
            <p style='color:#10b981; font-weight:700; font-size:15.5px; margin-bottom:10px;'>📦 Dataset</p>
            <p style='color:#94a3b8; font-size:14.5px; line-height:1.8; margin:0;'>
            • <b style='color:#e2e8f0;'>Source:</b> Luke Barousse Jobs Data 2023<br>
            • <b style='color:#e2e8f0;'>Volume:</b> 700,000+ job postings<br>
            • <b style='color:#e2e8f0;'>Coverage:</b> Global, across multiple industries<br>
            • <b style='color:#e2e8f0;'>Schema:</b> Star Schema (PostgreSQL)
            </p> </div> """, unsafe_allow_html=True)

    with col_tech:
        st.markdown("""
        <div style='background-color:#0f172a; border-left: 4px solid #10b981; padding:18px; border-radius:8px;'>
            <p style='color:#10b981; font-weight:700; font-size:15.5px; margin-bottom:10px;'>⚙️ Tech Stack</p>
            <p style='color:#94a3b8; font-size:14.5px; line-height:1.8; margin:0;'>
            • <b style='color:#e2e8f0;'>Frontend:</b> Python Streamlit<br>
            • <b style='color:#e2e8f0;'>Visualizations:</b> Plotly Express<br>
            • <b style='color:#e2e8f0;'>Database:</b> PostgreSQL (Avien.io)<br>
            • <b style='color:#e2e8f0;'>Queries:</b> Advanced SQL (CTEs, Joins, Window Functions)<br>
            • <b style='color:#e2e8f0;'>AI-Augmented Development:</b> Python, Streamlit & Plotly
            </p> </div> """, unsafe_allow_html=True)

    # Developer & Instructor
    st.markdown("<div style='margin-top:-10px;'></div>", unsafe_allow_html=True)
    st.markdown('<hr style="border: 1px solid rgba(255,255,255,0.1)">', unsafe_allow_html=True)
    col_dev, col_inst = st.columns(2)

    with col_dev:
        st.markdown("""
        <div style='text-align:left; padding:15px 0 10px 0;'>
            <p style='color:#94a3b8; font-size:15.5px; margin-bottom:6px;'>Built by</p>
            <p style='color:#10b981; font-size:18px; font-weight:800; margin:0 0 12px 0;'>Muhammad Omer Faisal</p>
            <a href='https://www.linkedin.com/in/omer-faisal876/' target='_blank'
               style='display:inline-flex; align-items:center; gap:8px; background-color:#0a66c2;
                      color:white; text-decoration:none; padding:8px 18px; border-radius:6px;
                      font-size:14px; font-weight:600;'>
                🔗 Connect on LinkedIn
            </a> </div> """, unsafe_allow_html=True)

    with col_inst:
        st.markdown("""
        <div style='padding:15px 0 10px 0; width:fit-content; margin-left:auto;'>
            <p style='color:#94a3b8; font-size:15.5px; margin-bottom:6px;'>Course Instructor</p>
            <p style='color:#10b981; font-size:18px; font-weight:800; margin:0 0 12px 0;'>Luke Barousse</p>
            <a href='https://www.lukebarousse.com/' target='_blank'
               style='display:inline-flex; align-items:center; gap:8px; background-color:#0f172a;
                      color:#10b981; text-decoration:none; padding:8px 18px; border-radius:6px;
                      font-size:14px; font-weight:600; border: 1px solid #10b981;'>
                🌐 Visit Website
            </a> </div> """, unsafe_allow_html=True)
        
    st.markdown("<div style='margin-top:0px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:left; padding:15px 0 5px 0;'>
        <a href='https://youtu.be/7mz73uXD9DA?si=KnEMVkzxMWeMLSX2' target='_blank'
           style='display:inline-flex; align-items:center; gap:10px; background-color:#ff0000;
                  color:white; text-decoration:none; padding:10px 24px; border-radius:6px;
                  font-size:15px; font-weight:600;'>
            ▶ Watch the Course on YouTube
        </a> </div> """, unsafe_allow_html=True)
        
# PAGE 2: Analytcis Dashboard
elif page == "📊 Market Overview":
    col_title, col_filter = st.columns([4,1])

    with col_title:
        st.title("📊 Market Dashboard")
        st.markdown('<hr style="margin-top:10px; margin-bottom:10px; border: 1px solid rgba(255,255,255,0.1)">', unsafe_allow_html=True)
        
    with col_filter:
        st.markdown("<div style='font-size:18px; margin-bottom:-12px; margin-top:0px;'>🌍 Select Country</div>", unsafe_allow_html=True)
        market_country = st.selectbox("", ["Select All"] + COUNTRY_LIST, key="market_country")
        
    market_where = where_clause
    if market_country != "Select All":
        market_where += f" AND job_country = '{market_country}'"
    
    # Card Visuals 
    kpi_query = f"""
        SELECT 
            COUNT(job_id) as total, 
            ROUND(AVG(salary_year_avg), 0) as sal,
            ROUND(SUM(CASE WHEN job_work_from_home IS TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(job_id), 1) as remote_pct
        FROM job_postings_fact
        {market_where} """
    kpi_data = load_data(kpi_query)
    
    # Safe handling of potential NULL values in KPIs
    if not kpi_data.empty:
        total_val = kpi_data['total'].iloc[0] or 0
        sal_val = kpi_data['sal'].iloc[0] or 0
        remote_val = kpi_data['remote_pct'].iloc[0] or 0
    else:
        total_val, sal_val, remote_val = 0, 0, 0

    c1, c2, c3 = st.columns(3)
    c1.metric("📝 Total Postings", f"{total_val:,}")
    c2.metric("💰 Avg Yearly Salary", f"${sal_val:,.0f}" if sal_val > 0 else "N/A")
    c3.metric("🏠 Remote Availability", f"{remote_val}%") 
    st.divider()

    # Bar Chat: Top 10 Demanded Skills
    st.subheader("🏆 Top 10 Demanded Skills")
    skills_sql = f"""
        SELECT
            skills,
            COUNT(skill_to_job.job_id) AS total_jobs
        FROM job_postings_fact AS jobs
        INNER JOIN skills_job_dim AS skill_to_job ON jobs.job_id = skill_to_job.job_id
        INNER JOIN skills_dim AS skills ON skill_to_job.skill_id = skills.skill_id
        {market_where}
        GROUP BY skills
        ORDER BY total_jobs DESC
        LIMIT 10 """
                
    df_skills = load_data(skills_sql)
    if not df_skills.empty:
        df_skills['skills'] = df_skills['skills'].str.title()
        df_skills['label'] = (df_skills['total_jobs'] / 1000).map('{:,.1f}K'.format)
        
        # Emerald scale for higher intensity
        emerald_scale = [[0.0, '#064e3b'], [0.5, '#10b981'], [1.0, '#34d399']]
        
        fig_bar = px.bar( df_skills, x='skills', y='total_jobs', text='label', color='total_jobs', 
                          color_continuous_scale=emerald_scale,
                          labels={'skills': 'Skills', 'total_jobs': 'Job Demand'} )
        
        fig_bar.update_traces(
            textposition='outside', textfont=dict(color='white', size=13),
            hovertemplate='<b>%{x}</b><br>Job Demand: <b>%{y:,}</b><extra></extra>')
        
        fig_bar.update_layout(font=dict(weight='bold'), margin=dict(t=30, b=10), coloraxis_showscale=True, bargap=0.4,
                              hoverlabel=dict(
                                    bgcolor='#1e293b', bordercolor='#10b981', 
                                    font=dict(color='white', size=13)), 
                              modebar=dict(
                                bgcolor='rgba(0,0,0,0)', color='#94a3b8',
                                activecolor='#10b981', orientation='h'))
        
        fig_bar.update_xaxes(showgrid=False, tickfont=dict(size=14), title_font=dict(size=16))
        fig_bar.update_yaxes(showgrid=False, tickfont=dict(size=14))
        
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
    st.markdown('<hr style="margin-top:0px; margin-bottom:40px; border: 1px solid rgba(255,255,255,0.1)">', unsafe_allow_html=True)
    
      # Scatter Plot with Market Average 
    col_header, col_switch = st.columns([4, 1])
    with col_header:
        st.subheader("🎯 Salary Benchmarking vs Market Average")
        
    # Salary Type Switch
    with col_switch:    
        st.markdown("<p style='font-size:17px; font-weight:600; margin-bottom:-15px; color:white;'>Select Salary Basis:</p>", unsafe_allow_html=True)
        salary_type = st.radio("", ["Yearly", "Hourly"], horizontal=True, key="role_salary_switch")
        
    col_to_use = "salary_year_avg" if salary_type == "Yearly" else "salary_hour_avg"
    label_text = "Avg Yearly Salary ($)" if salary_type == "Yearly" else "Avg Hourly Salary ($)"
    tick_format = "$~s" if salary_type == "Yearly" else "$0"

    scatter_sql = f"""
        SELECT 
        job_title_short, 
        {col_to_use},
        (SELECT AVG({col_to_use}) FROM job_postings_fact WHERE {col_to_use} IS NOT NULL) AS market_avg
        FROM job_postings_fact
        {market_where} AND {col_to_use} IS NOT NULL """

    df_scatter = load_data(scatter_sql)
    
    if not df_scatter.empty:
        emerald_scale = [[0.0, '#064e3b'], [0.5, '#10b981'], [1.0, '#34d399']]
        fig_scatter = px.scatter(df_scatter, x=col_to_use, y="job_title_short",
                                 color=col_to_use, size=col_to_use,
                                 color_continuous_scale=emerald_scale,
                                 custom_data=['job_title_short', col_to_use],
                                 labels={col_to_use: label_text, 'job_title_short': 'Job Title'} )
        
        fig_scatter.update_traces(
            hovertemplate='<b>%{customdata[0]}</b><br>' + label_text + ': <b>%{customdata[1]:$,.0f}</b><extra></extra>')
              
        m_avg = df_scatter['market_avg'].iloc[0] or 0
        avg_text = f"${m_avg/1000:,.0f}K" if salary_type == "Yearly" else f"${m_avg:,.2f}"
        
        if m_avg > 0:
            fig_scatter.add_vline(x=m_avg, line_dash="dash", line_color="#ef4444", annotation_text=f"Market Avg: {avg_text}", annotation_position="top right" )
            
        fig_scatter.update_layout(font=dict(weight='bold'), xaxis=dict(tickformat=tick_format),
                                  hoverlabel=dict(
                                      bgcolor='#1e293b', bordercolor='#10b981',
                                      font=dict(color='white', size=13)
                                   ),
                                  xaxis_title=label_text, yaxis_title="Job Title",
                                  coloraxis_showscale=False, margin=dict(t=10), 
                                  modebar=dict(
                                      bgcolor='rgba(0,0,0,0)', color='#94a3b8',
                                      activecolor='#10b981', orientation='h'))
        
        fig_scatter.update_xaxes(showgrid=False, tickfont=dict(size=14), title_font=dict(size=16))
        fig_scatter.update_yaxes(showgrid=False, tickfont=dict(size=14), title_font=dict(size=16))
        
        st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': False})
          
# Page 3: Salary Insights
elif page == "💰 Salary Insights":  
    st.markdown("""<style>[data-testid="stMain"] .stRadio > div { margin-top: -25px !important;} </style>""", unsafe_allow_html=True)
    
    col_title, col_filter = st.columns([4,1])
    with col_title:
        st.title("💰 Global Salary Overview")
        st.markdown('<hr style="margin-top:10px; margin-bottom:10px; border: 1px solid rgba(255,255,255,0.1)">', unsafe_allow_html=True)
    
    with col_filter:
        st.markdown("<div style='font-size:18px; margin-bottom:-12px; margin-top:0px;'>🌍 Select Country</div>", unsafe_allow_html=True)
        country_filter = st.selectbox("", ["Select All"] + COUNTRY_LIST, key="salary_country")
        
    st.subheader("🛠️ Highest-Paying Skills – 2023")
    st.markdown('<h6 class="tight-header">Skills Categories :</h5>', unsafe_allow_html=True)
    
    # Skill Type Filter
    skill_type_ui = st.radio(
        "", 
        ["All", "Languages", "Tools", "Databases", "Cloud", "Libraries", "Frameworks"], 
        horizontal=True, key="salary_skill_type" )
    
    # Mapping UI labels to original database values
    skill_mapping = {
        "All": "All",
        "Languages": "programming",
        "Tools": "analyst_tools",
        "Databases": "Databases",
        "Cloud": "Cloud",
        "Libraries": "Libraries",
        "Frameworks": "webframeworks" }
    selected_db_val = skill_mapping[skill_type_ui]
    
    # Dynamic Salary Where Clause
    salary_where = where_clause
    if country_filter != "Select All":
        salary_where += f" AND job_country = '{country_filter}'"

    if selected_db_val != "All":
        salary_where += f" AND LOWER(skills.type) = '{selected_db_val.lower()}'"
        
    # Dynamic Role Where Clause for Role Salary Chart
    role_where = where_clause
    if country_filter != "Select All":
        role_where += f" AND job_country = '{country_filter}'"
    
     # 10 Highest Paying Skills Query
    salary_skills_sql = f"""
    WITH ranking AS (
        SELECT
            skills.skills,
            ROUND(AVG(salary_year_avg), 0) AS avg_salary,
            DENSE_RANK() OVER (ORDER BY AVG(salary_year_avg) DESC) AS rnk
        FROM job_postings_fact AS jobs
        INNER JOIN skills_job_dim ON jobs.job_id = skills_job_dim.job_id
        INNER JOIN skills_dim AS skills ON skills_job_dim.skill_id = skills.skill_id
        {salary_where} AND salary_year_avg IS NOT NULL
        GROUP BY skills.skills
    )
    SELECT * FROM ranking
    WHERE rnk <= 10 
    ORDER BY avg_salary DESC; """
    
    df_salary_skills = load_data(salary_skills_sql)
    if not df_salary_skills.empty:
        df_salary_skills['skills'] = df_salary_skills['skills'].str.title()
        
        # Sorting for horizontal bar chart
        df_salary_skills = df_salary_skills.sort_values(by='avg_salary', ascending=True)
        df_salary_skills['label'] = df_salary_skills['avg_salary'].apply(lambda x: f"${x:,.0f}")

        emerald_scale = [[0.0, '#064e3b'], [0.5, '#10b981'], [1.0, '#34d399']]

        fig_salary = px.bar(df_salary_skills, x='avg_salary', y='skills',
                            orientation='h', text='label', color='avg_salary',
                            color_continuous_scale=emerald_scale,
                            custom_data=['skills', 'avg_salary'],
                            labels={'avg_salary': 'Avg Salary', 'skills': 'Skills'})
        
        fig_salary.update_traces(
            hovertemplate='<b>%{customdata[0]}</b><br>Avg Salary: <b>$%{customdata[1]:,.0f}</b><extra></extra>')

        fig_salary.update_traces(textposition='inside', insidetextanchor='end', texttemplate='%{text}   ',
                                 textfont=dict(color='white', size=16), cliponaxis=False)

        fig_salary.update_layout(xaxis_title="Average Salary ($)", yaxis_title="", font=dict(weight='bold'),
                                 hoverlabel=dict(
                                    bgcolor='#1e293b', bordercolor='#10b981',
                                    font=dict(color='white', size=13)
                                 ), 
                                 margin=dict(t=20, b=20), coloraxis_showscale=False,
                                 plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                 modebar=dict(
                                    bgcolor='rgba(0,0,0,0)', color='#94a3b8',
                                    activecolor='#10b981', orientation='h'))

        fig_salary.update_xaxes(showgrid=False, tickfont=dict(size=14), title_font=dict(size=16))
        fig_salary.update_yaxes(showgrid=False, tickfont=dict(size=14))
        
        st.plotly_chart(fig_salary, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info(f"No salary data available for selected filters.")
    st.markdown('<hr style="margin-top:0px; margin-bottom:40px; border: 1px solid rgba(255,255,255,0.1)">', unsafe_allow_html=True)
        
    # Chart: Highest Average Salaries By Role
    col_header, col_switch = st.columns([4, 1])
    with col_header:
        st.subheader("💼 Highest Average Salaries By Role")
    
    with col_switch:
        st.markdown("<p style='font-size:17px; font-weight:600; margin-bottom:-15px; color:white;'>Select Salary Basis:</p>", unsafe_allow_html=True)
        salary_type = st.radio("", ["Yearly", "Hourly"], horizontal=True, key="role_salary_switch")

    col_to_use = "salary_year_avg" if salary_type == "Yearly" else "salary_hour_avg"
    label_text = "Avg Yearly Salary ($)" if salary_type == "Yearly" else "Avg Hourly Salary"
    tick_format = "$~s" if salary_type == "Yearly" else "$0"

    salary_where_sql = role_where

    # Query for top 10 highest average salaries by role
    role_salary_sql = f"""
        SELECT 
            job_title_short AS role,
            ROUND(AVG({col_to_use}), 0) AS avg_salary
        FROM job_postings_fact
        {salary_where_sql} AND {col_to_use} IS NOT NULL
        GROUP BY job_title_short
        ORDER BY avg_salary DESC
        LIMIT 10 """

    df_role_salary = load_data(role_salary_sql)

    if not df_role_salary.empty:
        df_role_salary = df_role_salary.sort_values(by='avg_salary', ascending=True)
        df_role_salary['label'] = df_role_salary['avg_salary'].apply(lambda x: f"${x:,.0f}")

        emerald_scale = [[0.0, '#064e3b'], [0.5, '#10b981'], [1.0, '#34d399']]
        
        fig_role_salary = px.bar(df_role_salary, x='avg_salary', y='role',
                                 orientation='h', text='label', color='avg_salary',
                                 color_continuous_scale=emerald_scale,
                                 custom_data=['role', 'avg_salary'],
                                 labels={'avg_salary': label_text, 'role': 'Role'})
        
        fig_role_salary.update_traces(
            hovertemplate='<b>%{customdata[0]}</b><br>' + label_text + ': <b>$%{customdata[1]:,.0f}</b><extra></extra>')

        fig_role_salary.update_traces(textposition='inside', insidetextanchor='end', texttemplate='%{text}   ',
                                      textfont=dict(color='white', size=16), cliponaxis=False)

        fig_role_salary.update_layout(xaxis_title=label_text, yaxis_title="", font=dict(weight='bold'),
                                      hoverlabel=dict(
                                        bgcolor='#1e293b', bordercolor='#10b981',
                                        font=dict(color='white', size=13)
                                      ),
                                      margin=dict(t=20, b=20), coloraxis_showscale=False,
                                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                      modebar=dict(
                                            bgcolor='rgba(0,0,0,0)', color='#94a3b8', 
                                            activecolor='#10b981', orientation='h'))

        fig_role_salary.update_xaxes(showgrid=False, tickfont=dict(size=14), title_font=dict(size=16))
        fig_role_salary.update_yaxes(showgrid=False, tickfont=dict(size=14))

        st.plotly_chart(fig_role_salary, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("No salary data available for selected filters.")
    
# Page 4: Skill Economics
elif page == "🛠️ Skill Economics":

    col_title, col_filter = st.columns([4,1])
    with col_title:
        st.title("🛠️ Skills Intelligence")
        st.markdown('<hr style="margin-top:10px; margin-bottom:10px; border: 1px solid rgba(255,255,255,0.1)">', unsafe_allow_html=True)

    with col_filter:
        st.markdown("<div style='font-size:18px; margin-bottom:-12px; margin-top:0px;'>🌍 Select Country</div>", unsafe_allow_html=True)
        skill_country = st.selectbox("", ["Select All"] + COUNTRY_LIST, key="skill_country")

    skill_where = where_clause
    if skill_country != "Select All":
        skill_where += f" AND job_country = '{skill_country}'"

    st.subheader("💎 Most Optimal Skills — Demand vs Salary 🧠")
    st.markdown("<p style='color:#ffdb58; font-size:15px; margin-top:-10px;'>💡 <b>Tip:</b> Use the <b>green slider</b> at the bottom to slide across the x-axis. Click the <b>pan (↔) button</b> in the toolbar, then drag the chart to set your view. Use the <b>full screen</b> icon to expand, and <b>reset axes</b> to return to the default view.</p>", unsafe_allow_html=True)
    
    scatter_sql = f"""
    WITH skill_demand AS (
        SELECT
            skill_to_job.skill_id,
            skills.skills AS skill,
            COUNT(skill_to_job.job_id) AS total_jobs
        FROM job_postings_fact AS jobs
        INNER JOIN skills_job_dim AS skill_to_job ON jobs.job_id = skill_to_job.job_id
        INNER JOIN skills_dim AS skills ON skill_to_job.skill_id = skills.skill_id
        {skill_where} AND salary_year_avg IS NOT NULL
        GROUP BY skill_to_job.skill_id, skills.skills
    ),
    average_salary AS (
        SELECT
            skill_to_job.skill_id,
            skills.skills AS skill,
            ROUND(AVG(salary_year_avg), 0) AS avg_salary
        FROM job_postings_fact AS jobs
        INNER JOIN skills_job_dim AS skill_to_job ON jobs.job_id = skill_to_job.job_id
        INNER JOIN skills_dim AS skills ON skill_to_job.skill_id = skills.skill_id
        {skill_where} AND salary_year_avg IS NOT NULL
        GROUP BY skill_to_job.skill_id, skills.skills
    )
    SELECT
        skill_demand.skill,
        skill_demand.total_jobs,
        average_salary.avg_salary
    FROM skill_demand
    INNER JOIN average_salary ON skill_demand.skill_id = average_salary.skill_id
    WHERE skill_demand.total_jobs > 50
    ORDER BY average_salary.avg_salary DESC, skill_demand.total_jobs DESC
    LIMIT 15 """

    df_skill_scatter = load_data(scatter_sql)
    if not df_skill_scatter.empty:

        df_skill_scatter['skill'] = df_skill_scatter['skill'].str.title()
        df_skill_scatter = df_skill_scatter.reset_index(drop=True)

        emerald_scale = [[0.0, '#064e3b'], [0.5, '#10b981'], [1.0, '#34d399']]
        
        x_mid = df_skill_scatter["total_jobs"].median()
        y_mid = df_skill_scatter["avg_salary"].median()

        def get_position(row):
            on_right = row["total_jobs"] >= x_mid
            on_top   = row["avg_salary"] >= y_mid
            if on_right and on_top:
                return "top right"
            elif on_right and not on_top:
                return "bottom right"
            elif not on_right and on_top:
                return "top left"
            else:
                return "bottom left"

        text_positions = df_skill_scatter.apply(get_position, axis=1).tolist()
        
        fig_skill = px.scatter(df_skill_scatter, x="total_jobs", y="avg_salary",
                               size="total_jobs", color="avg_salary", text="skill",
                               color_continuous_scale=emerald_scale,
                               labels={"total_jobs": "Job Demand", "avg_salary": "Average Salary ($)"})

        # Set per-point text positions as a tuple on the trace
        fig_skill.data[0].textposition = tuple(text_positions)
        
        fig_skill.update_traces(marker=dict(opacity=0.85), textfont=dict(size=12.5),
            hovertemplate='<b>%{text}</b><br>Job Demand: <b>%{x:,}</b><br>Avg Salary: <b>$%{y:,.0f}</b><extra></extra>')

        fig_skill.update_layout(font=dict(weight='bold'), margin=dict(t=20, l=80, b=50),
            hoverlabel=dict(bgcolor='#1e293b', bordercolor='#10b981', font=dict(color='white', size=13)),
            coloraxis_showscale=True,
            coloraxis_colorbar=dict(title='Avg Salary', tickformat='$~s'),
            xaxis_title="Skill Demand (Job Count)", yaxis_title="Average Salary ($)",
            xaxis=dict(title_font=dict(size=16)), yaxis=dict(title_font=dict(size=16)),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            modebar=dict(
                bgcolor='rgba(0,0,0,0)', color='#94a3b8', activecolor='#10b981', orientation='h'))

        fig_skill.update_xaxes(showgrid=False, tickfont=dict(size=13), title_font=dict(size=16),
            rangeslider=dict(
                visible=True, thickness=0.02, borderwidth=1, yaxis=dict(rangemode='fixed'),
                bgcolor='#0f172a', bordercolor='#10b981'))

        fig_skill.update_yaxes(showgrid=False, tickformat="$~s", fixedrange=False, tickfont=dict(size=13))

        st.plotly_chart(fig_skill, use_container_width=True, config={'displayModeBar': True})
    else:
        st.info("No data available for selected filters.")
    st.markdown('<hr style="margin-top:0px; margin-bottom:10px; border: 1px solid rgba(255,255,255,0.1)">', unsafe_allow_html=True)
    
    # Skill Co-occurrence Chart
    st.subheader("🔗 Skill Co-occurrence — What Skills Appear Together?")
    st.markdown("<p style='color:#ffdb58; font-size:15px; margin-top:-10px;'>💡 Use the <b>skill dropdown below</b> to select a primary skill. The chart shows the top 10 skills that most frequently appear alongside it in the same job posting.</p>", unsafe_allow_html=True)

    # Skills dropdown
    skills_list_sql = """SELECT skills FROM skills_dim ORDER BY skills ASC """

    df_skills = load_data(skills_list_sql)

    if not df_skills.empty:
        skill_options = sorted([s.title() for s in df_skills['skills'].tolist()])
        default_idx = skill_options.index('Python')

        if 'cooc_skill' not in st.session_state:
            st.session_state['cooc_skill'] = skill_options[default_idx]

        col_skill, _ = st.columns([1, 3])
        with col_skill:
            st.markdown("<div style='font-size:16px; font-weight:700; color:white; margin-bottom:-35px;'>Select Skill</div>", unsafe_allow_html=True)
            selected_skill = st.selectbox("", skill_options, index=default_idx, key="cooc_skill")

        # Co-occurrence SQL
        cooc_sql = f"""
            SELECT
                s2.skills AS co_skill,
                COUNT(*) AS co_occurrences
            FROM skills_job_dim AS sj1
            INNER JOIN skills_job_dim AS sj2
                ON sj1.job_id = sj2.job_id
                AND sj1.skill_id != sj2.skill_id
            INNER JOIN skills_dim AS s1 ON sj1.skill_id = s1.skill_id
            INNER JOIN skills_dim AS s2 ON sj2.skill_id = s2.skill_id
            INNER JOIN job_postings_fact AS jobs ON sj1.job_id = jobs.job_id
            WHERE LOWER(s1.skills) = LOWER('{selected_skill}')
            {skill_where.replace("WHERE 1=1", "").strip()}
            GROUP BY s2.skills
            ORDER BY co_occurrences DESC
            LIMIT 10 """

        df_cooc = load_data(cooc_sql)

        if not df_cooc.empty:
            df_cooc['co_skill'] = df_cooc['co_skill'].str.title()
            df_cooc = df_cooc.sort_values(by='co_occurrences', ascending=True)
            df_cooc['label'] = df_cooc['co_occurrences'].apply(lambda x: f"{x:,}")

            emerald_scale = [[0.0, '#064e3b'], [0.5, '#10b981'], [1.0, '#34d399']]

            fig_cooc = px.bar(df_cooc, x='co_occurrences', y='co_skill', orientation='h',
                              text='label', color='co_occurrences',
                              color_continuous_scale=emerald_scale,
                              custom_data=['co_skill', 'co_occurrences'],
                              labels={'co_occurrences': 'Co-occurrence Count', 'co_skill': 'Skill'})
            
            fig_cooc.update_traces(
                hovertemplate='<b>%{customdata[0]}</b><br>Co-occurrences: <b>%{customdata[1]:,}</b><extra></extra>')

            fig_cooc.update_traces(textposition='inside', insidetextanchor='end', texttemplate='%{text}   ',
                                   textfont=dict(color='white', size=16), cliponaxis=False)

            fig_cooc.update_layout(font=dict(weight='bold'),
                    hoverlabel=dict(
                        bgcolor='#1e293b', bordercolor='#10b981',
                        font=dict(color='white', size=13)
                    ), 
                    margin=dict(t=20, b=55), coloraxis_showscale=False,
                    xaxis=dict(title=dict(text=f"No. of Job Postings Requiring {selected_skill} + Skills", standoff=25, font=dict(size=15))),
                    yaxis_title="", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    bargap=0.3, modebar=dict(
                                    bgcolor='rgba(0,0,0,0)', color='#94a3b8',
                                    activecolor='#10b981', orientation='h'))

            fig_cooc.update_xaxes(showgrid=False, tickfont=dict(size=14), title_font=dict(size=16))
            fig_cooc.update_yaxes(showgrid=False, tickfont=dict(size=15))

            st.plotly_chart(fig_cooc, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info(f"No co-occurrence data found for '{selected_skill}' with the current filters.")
    else:
        st.info("No skills data available for selected filters.")

# Page 5: Top Hiring Companies
elif page == "🏢 Top Hiring Companies":
    st.title("🏢 Most Active Hiring Companies")
    st.markdown('<hr style="margin-top:10px; margin-bottom:10px; border: 1px solid rgba(255,255,255,0.1)">', unsafe_allow_html=True)

    st.subheader("💸 Highest Paying Employers — 2023")
    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

    col_country, col_basis, col_spacer = st.columns([1, 1, 1.5])
    with col_country:
        st.markdown("<div style='font-size:16px; font-weight:500; margin-bottom:-10px;'>🌍 Select Country</div>", unsafe_allow_html=True)
        company_country = st.selectbox("", ["Select All"] + COUNTRY_LIST, key="company_country")

    with col_basis:
        st.markdown("<div style='font-size:16px; font-weight:500; margin-bottom:-10px;'>💰 Salary Basis</div>", unsafe_allow_html=True)
        company_salary_basis = st.selectbox("", ["Yearly", "Hourly"], key="company_basis")

    st.markdown("<div style='padding-top: 15px;'></div>", unsafe_allow_html=True)

    col_to_use = "salary_year_avg" if company_salary_basis == "Yearly" else "salary_hour_avg"
    label_text = "Avg Yearly Salary ($)" if company_salary_basis == "Yearly" else "Avg Hourly Salary ($)"
    
    company_where = where_clause
    if company_country != "Select All":
        company_where += f" AND job_country = '{company_country}'"

    company_sql = f"""
        SELECT 
            name AS company,
            ROUND(AVG({col_to_use}), 0) AS avg_salary
        FROM job_postings_fact AS jobs
        INNER JOIN company_dim AS companies ON jobs.company_id = companies.company_id
        {company_where} AND {col_to_use} IS NOT NULL
        GROUP BY name
        ORDER BY avg_salary DESC
        LIMIT 12 """

    df_company = load_data(company_sql)

    if not df_company.empty:
        df_company = df_company.sort_values(by='avg_salary', ascending=True)
        df_company['label'] = df_company['avg_salary'].apply(lambda x: f"${x:,.0f}")
        
        emerald_scale = [[0.0, '#064e3b'], [0.5, '#10b981'], [1.0, '#34d399']]
        
        fig_company = px.bar(df_company, x='avg_salary', y='company',
                             orientation='h', text='label', color='avg_salary',
                             color_continuous_scale=emerald_scale,
                             custom_data=['company', 'avg_salary'],
                             labels={'avg_salary': label_text, 'company': 'Company'})

        fig_company.update_traces(textposition='inside', insidetextanchor='end', texttemplate='%{text}  ',
                                    hovertemplate='<b>%{customdata[0]}</b><br>Avg Salary: <b>$%{customdata[1]:,.0f}</b><extra></extra>', 
                                  textfont=dict(color='white', size=15))

        fig_company.update_layout(xaxis_title=label_text, yaxis_title="", font=dict(weight='bold'),
                                    hoverlabel=dict(bgcolor='#1e293b', bordercolor='#10b981', font=dict(color='white', size=13)),
                                  margin=dict(t=10, b=20),  coloraxis_showscale=False,
                                  plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                  modebar=dict(bgcolor='rgba(0,0,0,0)', color='#94a3b8', activecolor='#10b981', orientation='h'))

        fig_company.update_xaxes(showgrid=False, tickfont=dict(size=14), title_font=dict(size=16))
        fig_company.update_yaxes(showgrid=False, tickfont=dict(size=14))

        st.plotly_chart(fig_company, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info(f"No hiring data available for the current selection.")



