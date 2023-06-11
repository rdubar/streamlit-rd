import streamlit as st

# streamlit run pages/RandomCase.py

text = "Strikethru"


def strike():
    text_ = st.session_state.text if 'text' in st.session_state and st.session_state.text else "Strikethru"
    result = ''
    for c in text_:
        result = result + c + '\u0336'
    return result


PAGETITLE = "Strikethru"


def clear_text():
    st.session_state["text"] = ""


st.title(PAGETITLE)

st.markdown(f'# :green[{strike()}]')

st.text_input("text", value="", max_chars=None, key="text", type="default",
              help="Enter Text Here", autocomplete=None, on_change=strike, args=None,
              kwargs=None, placeholder="Enter Text Here", disabled=False, label_visibility="hidden")

st.button('Strikethru')

st.button('Clear', on_click=clear_text)
