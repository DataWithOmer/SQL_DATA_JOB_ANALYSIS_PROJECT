import streamlit as st

def get_connection():
    """
    Initializes a connection to the PostgreSQL database 
    using the credentials in .streamlit/secrets.toml
    """
    # This automatically looks for [connections.postgresql] in secrets.toml
    conn = st.connection("aiven_db", type="sql")
    return conn
