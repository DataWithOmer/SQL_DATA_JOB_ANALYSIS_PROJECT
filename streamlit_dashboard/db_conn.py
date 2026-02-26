import streamlit as st

def get_connection():
    # This automatically looks for [connections.postgresql] in secrets.toml
    conn = st.connection("aiven_db", type="sql")
    return conn

