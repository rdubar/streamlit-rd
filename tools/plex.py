import time

from plexapi.server import PlexServer
from tqdm import tqdm

from settings import MEDIA_RECORDS_PATH, TOML_PATH
from tools.utils import read_toml, save_data, load_data, show_time, warn, info
from tools.media_record import MediaRecord

PLEX_INFO = read_toml(TOML_PATH, section='plex')

MEDIA_OBJECTS = []


def media_objects(update=False, reset=False, verbose=False):
    global MEDIA_OBJECTS
    if update or reset or not MEDIA_OBJECTS:
        MEDIA_OBJECTS = get_plex_info(update=update, reset=reset, verbose=verbose)
    return MEDIA_OBJECTS


def connect_to_plex(server_ip=None, port=32400, token=None, secrets=PLEX_INFO, url=False):
    if not server_ip:
        if 'server_ip' not in secrets:
            warn('Plex Connect: server ip not found.')
            return None
        server_ip = secrets['server_ip']
    if not port:
        port = secrets['port']
    if not token:
        token = secrets['token']
    if url:
        print(f'Plex URL: https://{server_ip}:{port}{12}?X-Plex-Token={token}')

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
        print(f'Failed to connect to Plex: {e}')
        return None
    clock = time.perf_counter() - clock
    print(f'Connected in {clock:.2f} seconds.')
    return plex


def get_plex_media():
    plex = connect_to_plex()
    if not plex:
        return
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


def get_plex_info(update=False, reset=False, verbose=False):
    media__objects = load_data(MEDIA_RECORDS_PATH)
    if not (update or reset):
        return media__objects
    clock = time.perf_counter()
    plex_records = get_plex_media()
    if reset:
        print('--reset: Resetting all records.')
        media__objects = []
    media_dict = {str(x.plex): x for x in media__objects}
    unchanged = []
    updated = []
    new = []
    if not plex_records:
        warn('No Plex records found.')
        return media__objects
    for p in plex_records:
        index = str(p.ratingKey)
        if index in media_dict:
            if p.addedAt <= media_dict[index].added:
                # print(f'Not changed {p.title}, last updated {media_dict[index].added}')
                unchanged.append(media_dict[index])
                continue
            else:
                if verbose:
                    print(f'Updating {p.title}, last updated {media_dict[index].added}')
                updated.append(media_dict[index].entry)
        else:
            if verbose:
                print(f'New entry {p.title} ({index})')
            new.append(p)
    c = len(media_dict)
    if not reset:
        info(f'Checked {c:,} records. Found {len(unchanged):,} unchanged, {len(updated):,} updated, {len(new):,} new.')
    new_media_list = unchanged
    to_check = updated + new
    if to_check:
        for p in tqdm(to_check, desc='Updating Plex Info'):
            m = MediaRecord(title=p.title)
            m.set_plex_info(p)
            new_media_list.append(m)
    save_data(MEDIA_RECORDS_PATH, new_media_list)
    if updated:
        print(f'Updated {len(updated)} items : {updated}')
    clock = time.perf_counter() - clock
    print(f'Plex info updated in {show_time(clock)}.')
    return new_media_list


def main():
    plex = connect_to_plex()

    print('HELLO!', plex)
    title = 'alien'  # Replace with the title you want to search for

    search_results = plex.search(title)

    for result in search_results:
        if result.type == 'movie':
            print(result.title)
            print(result.summary)
            print(result.year)
            # Add any other attributes you want to print or use


if __name__ == '__main__':
    main()
