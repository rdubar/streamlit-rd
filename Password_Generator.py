import streamlit as st
from tools.password import create_password

# streamlit run Password_Generator.py

PAGE_TITLE = "Rog's Password Generator"
st.set_page_config(page_title=PAGE_TITLE, page_icon=':fish:', layout="centered",
                       initial_sidebar_state="auto", menu_items=None)
default_length = 20

def display_value():
    """ return length from the slider, or the default value """
    if 'length' in st.session_state:
        length = st.session_state.length
    else:
        length = default_length
    return length

info = """
Passwords are cryptographically secure, and contain at least one uppercase, one 
lowercase, one digit, and one special character. Nothing is stored here, 
but beware of public computers.
"""

def show_page():
    st.title(PAGE_TITLE)

    st.code(create_password(length=display_value()))

    st.slider(
        "Length", min_value=4, max_value=64, value=default_length, step=1, key="length", on_change=display_value
    )

    st.button('Refresh')
    if st.button('Information'):
        st.info(info)

show_page()
