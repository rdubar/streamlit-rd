import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # Project Root
DATA_DIR = os.path.join(ROOT_DIR, 'data')
MEDIA_RECORDS_PATH = os.path.join(DATA_DIR, 'media_records.data')
DATAFRAME_PATH = os.path.join(DATA_DIR, 'plex_df.pkl')
LIBRARY_PATH = os.path.join(DATA_DIR, 'library.txt')
FILE_OBJECTS_PATH = os.path.join(DATA_DIR, 'file_objects.pkl')
TOML_PATH = os.path.join(ROOT_DIR, '.streamlit/secrets.toml')
IGNORE_LIST = ['/Incoming/']

