import streamlit as st
import password

# /Users/roger/.virtualenvs/streamlit-rd/bin/streamlit run /Users/roger/PycharmProjects/streamlit-rd/web.py

PAGE_TITLE = "Rog's Password Generator"
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

    st.set_page_config(page_title=PAGE_TITLE, page_icon=None, layout="centered",
                       initial_sidebar_state="auto", menu_items=None)

    st.title(PAGE_TITLE)

    st.code(password.create_password(length=display_value()))

    st.slider(
        "Length", min_value=4, max_value=64, value=default_length, step=1, key="length", on_change=display_value
    )

    st.button('Refresh')
    if st.button('Information'):
        st.info(info)

show_page()

from mysql.connector import connect, Error

print('Connecting to:',st.secrets.mysql.host)

try:
    with connect(
        host=st.secrets.mysql.host,
        user=st.secrets.mysql.user,
        password=st.secrets.mysql.password,
    ) as connection:
        print('Connection',connection)
except Error as e:
    print(e)
print('Program complete.')