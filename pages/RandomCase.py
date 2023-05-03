import streamlit as st
from random import choice

# streamlit run pages/RandomCase.py

text = "Randomcase"

def randomcase():
    sentence = st.session_state.text if 'text' in st.session_state and st.session_state.text else "Randomcase"
    return ''.join(choice((str.upper, str.lower))(c) for c in sentence)

PAGETITLE = "RandomCase"

def clear_text():
    st.session_state["text"] = ""


st.title(PAGETITLE)

st.markdown(f'# :green[{randomcase()}]')

st.text_input("text", value="", max_chars=None, key="text", type="default",
              help="Enter Text Here", autocomplete=None, on_change=randomcase, args=None,
              kwargs=None, placeholder="Enter Text Here", disabled=False, label_visibility="hidden")

st.button('Randomcase')

st.button('Clear', on_click=clear_text)

