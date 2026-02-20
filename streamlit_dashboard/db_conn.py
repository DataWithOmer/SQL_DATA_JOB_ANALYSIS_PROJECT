import streamlit as st
import pyodbc

def get_connection():
    # Retrieve credentials from .streamlit/secrets.toml
    creds = st.secrets["connections"]["sqlserver"]
    
    conn_str = (
        f"DRIVER={{{creds['driver']}}};"
        f"SERVER={creds['server']};"
        f"DATABASE={creds['database']};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;" 
    )
    return pyodbc.connect(conn_str)