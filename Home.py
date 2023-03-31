# streamlit run pages/Home.py

import streamlit as st

from tools.password import create_password

PAGE_TITLE = "Rog's Streamlit Playground"
st.set_page_config(page_title=PAGE_TITLE, page_icon=':elephant:', layout="centered",
                       initial_sidebar_state="auto", menu_items=None)

st.title(PAGE_TITLE)

"""
A place to play with Streamlit's cool features.

Please enjoy this randomly generated password. 
"""
st.code(create_password(length=20))
st.button('Refresh')

