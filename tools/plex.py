import os.path
import time

from plexapi.server import PlexServer
from tqdm import tqdm

from settings import MEDIA_RECORDS, DATAFRAME_FILE, TOML_FILE
from tools.utils import read_toml, save_data, load_data, showtime, show_file_size, warn
from tools.media_record import MediaRecord

PLEX_INFO = read_toml(TOML_FILE, section = 'plex')


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

def main():
    pass

if __name__ == '__main__':
    main()
