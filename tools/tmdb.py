#!/usr/bin/python
import sys, os

from settings import TOML_FILE, LIBRARY_LIST, DATA_DIR
from tools.utils import read_toml, load_data, save_data, show_time
from tools.media_record import MediaRecord
from tools.plex import get_plex_info

secrets = read_toml(TOML_FILE, section = 'tmdb')

# https://github.com/AnthonyBloomer/tmdbv3api

from tmdbv3api import TMDb, Movie
tmdb = TMDb()
tmdb.api_key = secrets['api_key']
tmdb.language = 'en'
tmdb.debug = True

movie = Movie()

TMDB_RAW_DATA = DATA_DIR + "tmdb_raw.data"


def search_tmdb(text, year=None):
    text = str(text).strip()
    # try for a specific ID
    if text.isdigit() and len(text) < 10:
        try:
            m = movie.details(text)
            return m
        except Exception as e:
            print(f'TMDB ID error: {e}')
            return None     

    # try for a name search
    if  (not year) and len(text) > 6 and text[-1]==')' and text[-6]=='(':
        year = text[-5:-2]
        title = text[:-6]
    else:
        year = year
        title = text
    
    try:
        search = movie.search(title)
    except Exception as e:
        print(f'TMDB error: {e}')
        return None

    if year: search = [x for x in search if year in x.release_date ]

    print(f'Found {len(search)} matches for "{text}".')
    
    if len(search) > 0:
        return search[0]
    else:
        return None
    
def add_media_list(path=TMDB_RAW_DATA, media=LIBRARY_LIST, update=False):

    tmdb_dict = load_data(path) or {}
    if not update: return tmdb_dict

    if type(media) == str and os.path.exists(media):
        with open(media, 'r') as f:
            lines = f.read().splitlines()
        media = [x.split('   ')[0] for x in lines]


    for item in media:
        title = item.title
        if title in tmdb_dict and tmdb_dict[title]: continue
        data = search_tmdb(title)
        tmdb_dict[title] = data

    save_data(path, tmdb_dict)
    
    return tmdb_dict

def main():
    print("Rog's TMDB Tool.")
    plex_data = get_plex_info()
    records = add_media_list(media=plex_data, update=True)
    

    if len(sys.argv) > 1:
        search = ' '.join(sys.argv[1:]).lower()
        print(f'Searching {len(records):,} records for "{search}".')
        for key, value in records.items():
            if search in key.lower() or (value and search in str(vars(value)).lower()):
                print(key)
                print(value)
                print()

if __name__== "__main__" :
    main()