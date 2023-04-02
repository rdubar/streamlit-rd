import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root

DATA_DIR = ROOT_DIR + '/data/'

MEDIA_RECORDS = DATA_DIR + 'media_records.data'

DATAFRAME_FILE = DATA_DIR + 'plex_df.pkl'

LIBRARY_LIST = DATA_DIR + 'library.txt'

FILE_OBJECTS = DATA_DIR + 'file_objects.pkl'

TOML_FILE = ROOT_DIR+'/.streamlit/secrets.toml'