import streamlit as st
import password

# /Users/roger/.virtualenvs/streamlit-rd/bin/streamlit run /Users/roger/PycharmProjects/streamlit-rd/web.py

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
    st.title("Rog's Password Generator")

    st.code(password.create_password(length=display_value()))

    st.slider(
        "Length", min_value=4, max_value=64, value=default_length, step=1, key="length", on_change=display_value
    )

    st.button('Refresh')
    if st.button('Information'):
        st.info(info)

show_page()