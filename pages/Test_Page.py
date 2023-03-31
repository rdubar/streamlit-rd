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

from streamlit.components.v1 import html

javascript = """function number(e){var t=["one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve"];return e>0&&e<=t.length?t[e-1]:e}function bittime(e){return e<=7||e>53?"five minutes":e<=12||e>48?"ten minutes":e<=17||e>43?"quarter":e<=23||e>38?"twenty minutes":e<=28||e>33?"twenty-five minutes":e}function ishtime(e,t){var n;return(e=number(e),t<=3||t>57)?e+" o'clock":t<=33&&t>28?"half past "+e:(n=t<30?"past":"to",(t=bittime(t))+" "+n+" "+e)}function daytime(e){return!e||e>21?" at night":e<12?" in the morning":e<=17?" in the afternoon":" in the evening"}function ish(e,t,n){return e&&t||(e=(time=new Date).getHours(),t=time.getMinutes(),n=time.getSeconds()),n||(n=0),z=daytime(e),e%=12,t>57&&n>30&&t++,t>60&&(t=0),t>33&&e++,e>12&&(e=1),0==e&&(e=12),"It is about "+ishtime(e,t)+z+"."}ish());"""

html(f'''<script>{javascript}</script>''')

conn = init_connection()
conn


