import streamlit as st
import pandas as pd

# streamlit run pages/Media_List.py

PAGE_TITLE = "Rog's Media List"
st.title(PAGE_TITLE)

df = pd.read_pickle("data/plex_df.pkl")

search = st.text_input("search", value="", max_chars=None, key="search", type="default",
              help="Enter Search Text Here", autocomplete=None, on_change=None, args=None,
              kwargs=None, placeholder="Search for title, actor, director, genre, etc.", disabled=False, label_visibility="hidden")

if search:
    df = df[df['search'].str.contains(search, case=False)]
    df['year'] = df['year'].astype('str') # fix for bug where year would become int

def clear_text():
    st.session_state["search"] = ""

df2 = df.drop(columns=['search'])
st.dataframe(data=df2, width=None, height=None, use_container_width=True)
if search: st.button('Clear search', on_click=clear_text)

years = df.copy()
years = years['year'].fillna(0).replace('', 0).astype('int64').value_counts().sort_index()
st.header('Titles by year')
st.bar_chart(years, x=None, y=None)

quality = df['quality'].value_counts().sort_index()
st.header('Titles by quality')
st.bar_chart(quality, x=None, y=None)


