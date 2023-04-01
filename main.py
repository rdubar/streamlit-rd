import argparse, time

from tools.utils import showtime, sort_records, search_records, warn
from tools.plex import get_dataframe, get_plex_info
from tools.library import get_library_records
from tools.password import create_password

import pandas


def main():
    #plex.main()

    clock = time.perf_counter()
    print("Rog's Plex Media Processor.")

    parser = argparse.ArgumentParser()
    p = parser.add_argument
    p("search", help="search the library", type=str, nargs='*')
    p("-a", "--all", help="show all matching", action="store_true")
    p("-n", '--number', help="show [5] items", type=int, nargs='?', const=5)
    p("-d", "--dvd", help="show uncompressed DVD rips", action="store_true")
    p("-p", "--password", help="generate a secure password", action="store_true")
    p("-u", "--update", help="update the library", action="store_true")
    p("-v", "--verbose", help="verbose mode", action="store_true")
    p("--reset", help="reset the library", action="store_true")
    args = parser.parse_args()
    update = args.update
    reset = args.reset
    search = args.search
    verbose = args.verbose
    number = args.number or 5

    if args.password:
        print(create_password(length=20))

    media_records = get_plex_info(update=update, reset=reset)
    library_records = get_library_records()

    records = sorted(media_records + library_records, key=lambda x: x.entry)

    if args.all:
        number = len(records)
        print('Showing all {number:,} records.')

    if not records:
        warn('No Records Found. Aborting.')
        return

    df = get_dataframe(records)

    if args.dvd:
        dvds = [ x for x in records if 'mpeg2video' in x.search ]
        print(f"Found {len(dvds):,} uncompressed dvds in {len(records):,} records.")
        records = dvds

    if search:
        search_records(' '.join(search).lower(), records, display=True, verbose=verbose)
    else:
        sort_records(records, attrib='added', number=number, reverse=True)

    print(f'Completed in {showtime(clock)}.')

if __name__ == '__main__':
    main()