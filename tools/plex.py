from plexapi.server import PlexServer
import time, argparse

from tools.utils import read_toml, TOML_FILE, save_data, load_data, showtime
from tools.media_record import MediaRecord
from tools.library import get_library_records
import pandas
import numpy as np

from tqdm import tqdm

MEDIA_RECORDS = "/Users/roger/PycharmProjects/streamlit-rd/data/media_records.data"
PLEX_INFO = read_toml(TOML_FILE, section = 'plex')
DATAFRAME_FILE = '/Users/roger/PycharmProjects/streamlit-rd/data/plex_df.pkl'

def connect_to_plex(    server_ip = None,
                        port = 32400,
                        token = None,
                        secrets = PLEX_INFO,
                        url = False):
    if not server_ip: server_ip = secrets['server_ip']
    if not port: port = secrets['port']
    if not token: token = secrets['token']
    if url: print(f'Plex URL: http://{server_ip}:{port}{12}?X-Plex-Token={token}')

    """Connect to the Plex server and return a list of Plex Objects """
    if not (token and port and server_ip):
        print(f'Plex server info missing: {server_ip}:{port}?{token}. Unable to connect.')
        return None
    baseurl = f'http://{server_ip}:{port}'
    print(f'Connecting to Plex server at {server_ip}:{port}. Please wait...')
    clock = time.perf_counter()
    try:
        plex = PlexServer(baseurl, token)
    except Exception as e:
        print('Failed to connect to Plex: {e}')
        return None
    print(f'Connected in {clock:.2f} seconds.')
    return plex

def get_plex_media():
    plex = connect_to_plex()
    if not plex: return
    clock = time.perf_counter()
    print(f'Getting plex library, please wait...')
    try:
        plex_media = plex.library.all()
    except Exception as e:
        print(f'Failed to get data from Plex: {e}')
        return []
    clock = time.perf_counter() - clock
    print(f'Received {len(plex_media):,} objects from Plex in {clock:.2f} seconds.')
    return plex_media

def get_plex_info(update=False, reset=False):
    media_objects = load_data(MEDIA_RECORDS)
    if not (update or reset): return media_objects
    clock = time.perf_counter()
    plex_records = get_plex_media()
    if reset:
        print('RESETTING ALL RECORDS.')
        media_objects = []
    media_dict = { str(x.plex):x for x in media_objects }
    new_media_list = []
    updated = []
    for p in tqdm(plex_records, desc='Getting plex media info'):
        index = p.ratingKey
        if index in media_dict:
            if p.addedAt < media_dict[index].added:
                new_media_list.append(media_dict[index])
                continue
            else:
                updated.append(media_dict[index].entry)
        m = MediaRecord(title = p.title)
        m.set_plex_info(p)
        new_media_list.append(m)
    save_data(MEDIA_RECORDS, new_media_list)
    print(f'Updated {len(updated)} items : {updated}')
    clock = time.perf_counter() - clock
    print(f'Plex info updated in {showtime(clock)}.')
    return new_media_list

def search_records(text, data, display=False):
    matches = []
    for object in data:
        if text in object.search:
            matches.append(object)
    if display:
        output = f'Found {len(matches):,} matches in {len(data):,} entries for "{text}".'
        print(output)
        [ print(x.display()) for x in matches ]
        if len(matches) > 10:
            print(output)
    return matches


def get_quality(x):
    if type(x) == int:
        x = int(x)
        if x > 1500:
            x = '4K'
        elif x >= 800:
            x = 'HD'
        elif x > 400:
            x = 'SD'
        else:
            x = 'ZD'
    if not x or x == None or x == '':
        return 'UQ'
    return x.upper()

def get_dataframe(data, path=DATAFRAME_FILE):
    df = pandas.DataFrame([vars(s) for s in data])
    #df = df.sort_values(by=['added'])
    df = df[['title', 'year', 'quality', 'source','added','search']].astype(np.int64, errors='ignore')
    df['added'] = pandas.to_datetime(df["added"]).dt.date
    df['quality'] = df['quality'].apply(get_quality)
    df.set_index('title', inplace=True)
    df = df.fillna('')
    df.to_pickle(path)
    print(f'Saved dataframe to: {path}')
    return df

def main():
    clock = time.perf_counter()
    print("Rog's Streamlit Plex Processor.")

    parser = argparse.ArgumentParser()
    p = parser.add_argument
    p("search", help="search the library", type=str, nargs='*')
    p("-u", "--update", help="update the library", action="store_true")
    p("--reset", help="reset the library", action="store_true")
    args = parser.parse_args()
    update = args.update
    reset = args.reset
    search = args.search

    media_records = get_plex_info(update=update, reset=reset)
    library_records = get_library_records()

    records = sorted(media_records + library_records, key=lambda x: x.entry())

    if not records:
        print('No Records Found. Aborting.')
        return

    df = get_dataframe(records)

    if search:
        search_records(' '.join(search).lower(), records, display=True)
    else:
        sorted_list = sorted(records, key=lambda x: x.added if x.added is not None else datetime.min, reverse=True)
        for i in range(5):
            print(sorted_list[i].display())

    print(f'completed in {showtime(clock)}.')


if __name__ == '__main__':
    main()
