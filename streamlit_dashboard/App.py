import streamlit as st
import pandas as pd
import plotly.express as px
from db_conn import get_connection

# STREAMLIT CONFIGURATION
st.set_page_config(
    page_title="LinkedIn Data Jobs ",
    page_icon="💼",
    layout="wide"
)

# ENHANCED UI WITH CSSx 
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
        border-top: 4px solid #0073b1;
    }
    .sql-code { 
        background-color: #262730; 
        color: #ffeb3b; 
        padding: 15px; 
        border-radius: 8px; 
        font-family: 'Courier New', monospace; 
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #004182; font-weight: 800; }
    .dev-names { color: #0073b1; font-weight: bold; font-size: 18px; }
    .overview-list { list-style-type: none; padding-left: 0; }
    .overview-list li::before { content: "• "; color: #28a745; font-weight: bold; margin-right: 5px; }
    </style>
    """, unsafe_allow_html=True)

# # --- DATABASE CONNECTION WITH CACHING ---
@st.cache_resource
def init_connection():
    return get_connection()

def load_data(query):
    """Helper function to execute SQL and return a DataFrame"""
    try:
        conn = init_connection()
        # for simple reads, but we use the cached connection here.
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()

# SIDEBAR: DISCOVERY FILTERS
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/LinkedIn_logo_initials.png/600px-LinkedIn_logo_initials.png", width=100)
st.sidebar.title("🔍 Discovery Filters")

# Updated filter: Swapped Machine Learning for Business Analyst
job_filter = st.sidebar.selectbox(
    "Select Job Category", 
    ["All", "Data Analyst", "Data Scientist", "Data Engineer", "Business Analyst"]
)
location_filter = st.sidebar.radio(
    "Location Type", 
    ["Global", "Remote Only"]
)
st.sidebar.markdown("---")

page = st.sidebar.selectbox(
    "Navigate To",
    [   "🏠 Project Overview", 
        "📊 Market Dashboard", 
        "📄 Job Postings", 
        "🛠️ Skills Job Dim", 
        "📚 Skills Dim", 
        "🏢 Company Dim" ] )

# DYNAMIC SQL WHERE CLAUSE
where_clause = "WHERE 1=1"
if job_filter != "All":
    where_clause += f" AND job_title_short = '{job_filter}'"
if location_filter == "Remote Only":
    where_clause += " AND job_work_from_home = 1"
    
# 🏠 PAGE 1: PROJECT OVERVIEW
if page == "🏠 Project Overview":
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

#  📊 PAGE 2: ANALYTICS DASHBOARD 
elif page == "📊 Market Dashboard":
    st.title("📊 Market Dashboard")
    
    # DYNAMIC KPI QUERY (Fixes Remote Availability and handles Nulls)
    kpi_query = f"""
        SELECT 
            COUNT(job_id) as total, 
            AVG(CAST(salary_year_avg AS FLOAT)) as sal,
            SUM(CASE WHEN job_work_from_home = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(job_id) as remote_pct
        FROM job_postings_fact
        {where_clause}
    """
    kpi_data = load_data(kpi_query)
    
    # Safe data extraction to prevent NoneType formatting errors
    if not kpi_data.empty:
        total_val = kpi_data['total'].iloc[0] or 0
        sal_val = kpi_data['sal'].iloc[0] if pd.notnull(kpi_data['sal'].iloc[0]) else 0
        remote_val = kpi_data['remote_pct'].iloc[0] if pd.notnull(kpi_data['remote_pct'].iloc[0]) else 0
    else:
        total_val, sal_val, remote_val = 0, 0, 0

    c1, c2, c3 = st.columns(3)
    c1.metric("📝 Total Postings", f"{total_val:,}")
    
    # Fix for TypeError: If sal_val is 0/None, we show N/A instead of trying to format
    if sal_val > 0:
        c2.metric("💰 Avg Yearly Salary", f"${sal_val:,.0f}")
    else:
        c2.metric("💰 Avg Yearly Salary", "N/A")
        
    c3.metric("🏠 Remote Availability", f"{remote_val:.1f}%") 
    st.divider()

    # ROW 1: BAR AND DONUT ---
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("🏆 Top 10 Demanded Skills")
        skills_sql = f"""
            SELECT TOP 10 s.skills, COUNT(sjd.job_id) as Demand
            FROM skills_dim s
            INNER JOIN skills_job_dim sjd ON s.skill_id = sjd.skill_id
            INNER JOIN job_postings_fact jpf ON sjd.job_id = jpf.job_id
            {where_clause}
            GROUP BY s.skills ORDER BY Demand DESC
        """
        df_skills = load_data(skills_sql)
        if not df_skills.empty:
            df_skills['label'] = (df_skills['Demand'] / 1000).map('{:,.1f}K'.format)
            # Custom Scale: Starts at light-medium blue (#D0E1F9) and ends at LinkedIn blue (#0073b1)
            # This ensures even low values remain clearly visible
            custom_blue_scale = [
                [0.0, '#D0E1F9'],  # Light but visible blue for the lowest bars
                [1.0, '#0073b1']   # Dark LinkedIn blue for the highest bars
            ]
            fig_bar = px.bar(df_skills, x='skills', y='Demand', text='label', color='Demand', 
                            color_continuous_scale=custom_blue_scale)
            
            fig_bar.update_traces(textposition='outside')
            fig_bar.update_layout(
                font=dict(weight='bold'), 
                margin=dict(t=30, b=10),
                coloraxis_showscale=True 
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    with col_r:
        st.markdown("<h3 style='text-align: center;'>🔝 Top 5 Job Schedules</h3>", unsafe_allow_html=True)
        donut_sql = f"""
            WITH ScheduleCounts AS (
                SELECT job_schedule_type, COUNT(*) as Total
                FROM job_postings_fact
                {where_clause}
                GROUP BY job_schedule_type
            ),
            RankedSchedules AS (
                SELECT job_schedule_type, Total,
                       ROW_NUMBER() OVER (ORDER BY Total DESC) as Rank
                FROM ScheduleCounts
            )
            SELECT 
                CASE WHEN Rank <= 5 THEN job_schedule_type ELSE 'Others' END as [Type],
                SUM(Total) as [Total]
            FROM RankedSchedules
            GROUP BY CASE WHEN Rank <= 5 THEN job_schedule_type ELSE 'Others' END
            ORDER BY [Total] DESC
        """
        df_donut = load_data(donut_sql)
        if not df_donut.empty:
            fig_donut = px.pie(df_donut, names='Type', values='Total', hole=0.5,
                               color_discrete_sequence=px.colors.sequential.Blues_r)
            fig_donut.update_traces(textinfo='percent+label', textfont=dict(weight='bold'))
            fig_donut.update_layout(font=dict(weight='bold'), showlegend=False)
            st.plotly_chart(fig_donut, use_container_width=True)

    # ROW 2: SHADED AREA CHART
    st.subheader("📈 Yearly Salary Trend")
    line_sql = f"""
        SELECT job_posted_year, AVG(salary_year_avg) as avg_sal
        FROM job_postings_fact
        {where_clause} AND salary_year_avg IS NOT NULL
        GROUP BY job_posted_year
        ORDER BY job_posted_year
    """
    df_line = load_data(line_sql)
    if not df_line.empty:
        df_line['job_posted_year'] = df_line['job_posted_year'].astype(str)
        fig_area = px.area(df_line, x='job_posted_year', y='avg_sal')
        fig_area.update_traces(line_color='#0073b1', line_width=4, fillcolor='rgba(0, 115, 177, 0.2)')
        fig_area.update_layout(
            font=dict(weight='bold'),
            xaxis_title="Posted Year",
            yaxis_title="Avg Salary ($)",
            yaxis=dict(tickformat='$~s')
        )
        st.plotly_chart(fig_area, use_container_width=True)
    
    # ROW 3: SCATTER CHART
    st.subheader("🎯 Salary Benchmarking vs Market Average")
    scatter_sql = f"""
        SELECT job_title_short, salary_year_avg,
               (SELECT AVG(salary_year_avg) FROM job_postings_fact WHERE salary_year_avg IS NOT NULL) AS market_avg
        FROM job_postings_fact
        {where_clause} AND salary_year_avg IS NOT NULL """
    df_scatter = load_data(scatter_sql)
    
    if not df_scatter.empty:
        custom_blue_scale = [
            [0.0, '#D0E1F9'], 
            [1.0, '#0073b1']
        ]
        fig_scatter = px.scatter(
            df_scatter, 
            x="salary_year_avg", 
            y="job_title_short", 
            color="salary_year_avg", 
            size="salary_year_avg",
            color_continuous_scale=custom_blue_scale 
        )
        
        m_avg = df_scatter['market_avg'].iloc[0] if pd.notnull(df_scatter['market_avg'].iloc[0]) else 0
        if m_avg > 0:
            fig_scatter.add_vline(x=m_avg, line_dash="dash", line_color="red", 
                               annotation_text=f"Market Avg: ${m_avg/1000:,.0f}K")
        
        fig_scatter.update_layout(
            font=dict(weight='bold'), 
            xaxis=dict(tickformat='~s'),
            coloraxis_showscale=True
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with st.expander("🛠️ View SQL Logic"):
        st.code(
            f"-- 1. KPI Metrics (Total Jobs, Avg Salary, Remote %)\n{kpi_query}\n\n"
            f"-- 2. Top 10 Demanded Skills (Bar Chart)\n{skills_sql}\n\n"
            f"-- 3. Top 5 Job Schedules (Donut Chart)\n{donut_sql}\n\n"
            f"-- 4. Yearly Salary Trend (Area Chart)\n{line_sql}\n\n"
            f"-- 5. Salary Benchmarking (Scatter Plot)\n{scatter_sql}", 
            language="sql"
        )

# 📑 DATA TABLES
else:
    table_map = {
        "📄 Job Postings": "job_postings_fact",
        "🛠️ Skills Job Dim": "skills_job_dim",
        "📚 Skills Dim": "skills_dim",
        "🏢 Company Dim": "company_dim"
    }
    target = table_map[page]
    st.subheader(f"Data Preview: {target}")
    
    # Filtered preview for the main fact table
    if target == "job_postings_fact":
        df_raw = load_data(f"SELECT TOP 100 * FROM {target} {where_clause}")
    else:
        df_raw = load_data(f"SELECT TOP 100 * FROM {target}")
        
    st.dataframe(df_raw, use_container_width=True)