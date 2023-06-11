import streamlit as st

from mysql.connector import connect, Error

print('Connecting to:', st.secrets.mysql.host)

try:
    with connect(
            host=st.secrets.mysql.host,
            user=st.secrets.mysql.user,
            password=st.secrets.mysql.password,
    ) as connection:
        print('Connection', connection)
except Error as e:
    print(e)
print('Program complete.')
