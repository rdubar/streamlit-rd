import streamlit as st
from random import choice

# streamlit run pages/RandomCase.py

text = "Strikethru"

def strike():
    text = st.session_state.text if 'text' in st.session_state and st.session_state.text else "Strikethru"
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result

PAGETITLE = "Strikethru"

def clear_text():
    st.session_state["text"] = ""

st.set_page_config(page_title=PAGETITLE, page_icon=None, layout="centered",
                       initial_sidebar_state="auto", menu_items=None)

st.title(PAGETITLE)

st.markdown(f'# :green[{strike()}]')

st.text_input("text", value="", max_chars=None, key="text", type="default",
              help="Enter Text Here", autocomplete=None, on_change=strike, args=None,
              kwargs=None, placeholder="Enter Text Here", disabled=False, label_visibility="hidden")

st.button('Strikethru')

st.button('Clear', on_click=clear_text)

