import time

from plexapi.server import PlexServer
from tqdm import tqdm

from settings import MEDIA_RECORDS_PATH, DATAFRAME_PATH, TOML_PATH
from tools.utils import read_toml, save_data, load_data, show_time, warn
from tools.media_record import MediaRecord

PLEX_INFO = read_toml(TOML_PATH, section ='plex')

MEDIA_OBJECTS = []
def media_objects(update=False, reset=False):
    global MEDIA_OBJECTS
    if update or reset or not MEDIA_OBJECTS:
        MEDIA_OBJECTS = get_plex_info(update=update, reset=reset)
    return MEDIA_OBJECTS


def connect_to_plex(    server_ip = None,
                        port = 32400,
                        token = None,
                        secrets = PLEX_INFO,
                        url = False):
    if not server_ip:
        if 'server_ip' not in secrets:
            warn('Plex Connect: server ip not found.')
            return None
        server_ip = secrets['server_ip']
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
    media_objects = load_data(MEDIA_RECORDS_PATH)
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
    save_data(MEDIA_RECORDS_PATH, new_media_list)
    if updated: print(f'Updated {len(updated)} items : {updated}')
    clock = time.perf_counter() - clock
    print(f'Plex info updated in {show_time(clock)}.')
    return new_media_list

def main():
    plex = connect_to_plex()

    print('HELLO!',plex)
    title = 'Jaws'  # Replace with the title you want to search for

    search_results = plex.search(title)

    for result in search_results:
        if result.type == 'movie':
            print(result.title)
            print(result.summary)
            print(result.year)
            # Add any other attributes you want to print or use

if __name__ == '__main__':
    main()
