import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
TOML_FILE = ROOT_DIR+'/.streamlit/secrets.toml'

MEDIA_RECORDS = ROOT_DIR+"/data/media_records.data"
DATAFRAME_FILE = ROOT_DIR+'/data/plex_df.pkl'