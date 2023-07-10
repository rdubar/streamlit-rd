import mysql.connector
import toml

SECRETS = toml.load('../.streamlit/secrets.toml')

mydb = None
try:
    mydb = mysql.connector.connect(**SECRETS['mysql'])
except Exception as e:
    print('Connection Error: {e}')

print(mydb)

