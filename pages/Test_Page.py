# Streamlit.py

# streamlit run pages/Test_Page.py

import streamlit as st
import mysql.connector

from tools.password import create_password

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

st.code(create_password())

conn = init_connection()
conn


