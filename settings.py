import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
DATA_DIR = ROOT_DIR + '/data/'
MEDIA_RECORDS_PATH = DATA_DIR + 'media_records.data'
DATAFRAME_PATH = DATA_DIR + 'plex_df.pkl'
LIBRARY_PATH = DATA_DIR + 'library.txt'
FILE_OBJECTS_PATH = DATA_DIR + 'file_objects.pkl'
TOML_PATH = ROOT_DIR + '/.streamlit/secrets.toml'
IGNORE_LIST = ['/Incoming/']

