import streamlit as st
import pandas as pd
import plotly.express as px
from db_conn import get_connection

# STREAMLIT CONFIGURATION
st.set_page_config(
    page_title="LinkedIn Data Jobs Analysis",
    page_icon="💼",
    layout="wide"
)

# Enhanced CSS styling
st.markdown("""
<style>
/* App Background */
.stApp { background-color: #020617; }

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

# SIDEBAR: Discovery filters and navigation
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/LinkedIn_logo_initials.png/600px-LinkedIn_logo_initials.png", width=75)
st.sidebar.title("🔍 Discovery Filters")

job_filter = st.sidebar.selectbox(
    "Select Job Category", 
    ["All", "Data Analyst", "Data Scientist", "Data Engineer", "Business Analyst", "Machine Learning Engineer", "Senior Data Analyst",
     "Senior Data Engineer", "Senior Data Scientist"] )
location_filter = st.sidebar.radio(
    "Location Type", 
    ["Global", "Remote Only"] )
st.sidebar.markdown("---")
page = st.sidebar.selectbox( 
    "Navigate To",
    [  "📑 Project Overview", "📊 Market Overview", "💰 Salary Insights"  ,"🛠️ Skill Economics", "🏢 Top Hiring Companies" ])

# Dynamic SQL Where Clause
where_clause = "WHERE 1=1"
if job_filter != "All":
    where_clause += f" AND job_title_short = '{job_filter}'"
if location_filter == "Remote Only":
    where_clause += " AND job_work_from_home IS TRUE"
    
# PAGE 1: Project Overview 
if page == "📑 Project Overview":
    st.title("💼 LinkedIn Data Jobs Analysis")
    st.markdown("---")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📌 Project Concept")
        st.info("""
        This project explores the LinkedIn job market for data professionals. By utilizing a **Star Schema** database architecture, we can analyze the intersection of company demands, salary benchmarks, and technical skill requirements.
        """)
        
        st.markdown("### 🛠️ Technical SQL Implementation")
        st.write("This application demonstrates a high level of SQL proficiency through:")
        st.markdown("""
        <ul class="overview-list">
            <li><b>DDL (Data Definition Language):</b> Creating relational schema with proper primary/foreign key constraints.</li>
            <li><b>DML (Data Manipulation Language):</b> Populating and cleaning raw LinkedIn data.</li>
            <li><b>Complex Analytics:</b> Usage of <b>Aggregates</b>, <b>Subqueries</b>, and <b>Multi-table JOINS</b>.</li>
        </ul>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 🎓 Developer Knowledge")
        st.success("""
        - **Basics:** SELECT, WHERE, Aliases, GROUP BY
        - **Aggregates & Joins:** Multi-Table Relational Analysis
        - **CASE Statements:** Dynamic Data Categorization
        - **CTEs/Subqueries:** Modular & Nested Query Logic
        - **Window Functions:** Ranking & Analytical Partitioning
        """)
        
        st.markdown("<div style='padding-top: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("<b>👤 Developed by:</b>", unsafe_allow_html=True)
        st.markdown('<p class="dev-names" style="margin-top: -15px;">Muhammad Omer Faisal</p>', unsafe_allow_html=True)
        st.markdown("---")

# PAGE 2: Analytcis Dashboard
elif page == "📊 Market Overview":
    st.title("📊 Market Dashboard")
    # Card Visuals 
    kpi_query = f"""
        SELECT 
            COUNT(job_id) as total, 
            ROUND(AVG(salary_year_avg), 0) as sal,
            ROUND(SUM(CASE WHEN job_work_from_home IS TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(job_id), 1) as remote_pct
        FROM job_postings_fact
        {where_clause} """
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
        {where_clause}
        GROUP BY skills
        ORDER BY total_jobs DESC
        LIMIT 10 """
                
    df_skills = load_data(skills_sql)
    if not df_skills.empty:
        df_skills['label'] = (df_skills['total_jobs'] / 1000).map('{:,.1f}K'.format)
        # Use this scale for a modern, high-contrast look
        emerald_scale = [[0.0, '#064e3b'], [0.5, '#10b981'], [1.0, '#34d399']]
        
        fig_bar = px.bar( df_skills, x='skills', y='total_jobs', text='label', color='total_jobs', 
                          color_continuous_scale=emerald_scale,
                          labels={'skills': 'Skills', 'total_jobs': 'Job Demand'} )
        
        fig_bar.update_traces(textposition='outside')
        fig_bar.update_layout(font=dict(weight='bold'), margin=dict(t=30, b=10), coloraxis_showscale=True)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    col_header, col_switch = st.columns([4, 1])
    # Scatter Plot with Market Average 
    with col_header:
        st.subheader("🎯 Salary Benchmarking vs Market Average")
        
    with col_switch:    
        salary_type = st.radio(
        "**Select Salary Basis**:",
        ["Yearly", "Hourly"],
        horizontal=True,
        key="salary_switch" )
        
    col_to_use = "salary_year_avg" if salary_type == "Yearly" else "salary_hour_avg"
    label_text = "Avg Yearly Salary" if salary_type == "Yearly" else "Avg Hourly Salary"
    tick_format = "$~s" if salary_type == "Yearly" else "$0"

    scatter_sql = f"""
        SELECT 
        job_title_short, 
        {col_to_use},
        (SELECT AVG({col_to_use}) FROM job_postings_fact WHERE {col_to_use} IS NOT NULL) AS market_avg
        FROM job_postings_fact
        {where_clause} AND {col_to_use} IS NOT NULL """

    df_scatter = load_data(scatter_sql)
    
    if not df_scatter.empty:

        emerald_scale = [[0.0, '#064e3b'], [0.5, '#10b981'], [1.0, '#34d399']]
        fig_scatter = px.scatter(df_scatter, x=col_to_use, y="job_title_short", 
                                 color=col_to_use, size=col_to_use, 
                                 color_continuous_scale=emerald_scale,
                                 labels={col_to_use: label_text, 'job_title_short': 'Job Title'} )
              
        m_avg = df_scatter['market_avg'].iloc[0] or 0
        avg_text = f"${m_avg/1000:,.0f}K" if salary_type == "Yearly" else f"${m_avg:,.2f}"
        if m_avg > 0:
            fig_scatter.add_vline( x=m_avg, line_dash="dash", line_color="#ef4444", annotation_text=f"Market Avg: {avg_text}", annotation_position="top right" )
            
        fig_scatter.update_layout( font=dict(weight='bold'), xaxis=dict(tickformat=tick_format),
                                   xaxis_title=label_text, yaxis_title="Job Title",
                                   coloraxis_showscale=False, margin=dict(t=10) )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
        
elif page == "💰 Salary Insights":
    st.title("💰 Salary Insights")
    st.write("💸 High-Value Data Roles & Skills")
    
# PAGE 3: Skill Economics
elif page == "Skill Economics":
    st.title("💡 Skill Economics")
    st.write("💡 Skill Insights: Demand, Salary & Synergy")

# PAGE 4: Top Hiring Companies
elif page == "Top Hiring Companies":
    st.title("🏢 Top Hiring Companies")
    st.write("🏢 Market Leaders: Top Hiring Companies")













