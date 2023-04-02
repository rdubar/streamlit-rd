import argparse, time

from tools.utils import showtime, sort_by_attrib_value, search_records, warn, success, info, show_file_size
from tools.plex import get_plex_info
from tools.library import get_library_records
from tools.password import create_password
from tools.dataframe import get_dataframe
from tools.files import process_files

def main():
    #plex.main()

    clock = time.perf_counter()
    info("Rog's Plex Media Processor.")

    parser = argparse.ArgumentParser()
    p = parser.add_argument
    p("search", help="search the library", type=str, nargs='*')
    p("-a", "--all", help="show all matching", action="store_true")
    p("-f", "--files", help="search files instead of plex info", action="store_true")
    p('-H', '--height', help="sort by height", action="store_true")
    p("-n", '--number', help="show [5] items", type=int, nargs='?', const=5)
    p("-d", "--dvd", help="show uncompressed DVD rips", action="store_true")
    p("-p", "--password", help="generate a secure password", action="store_true")
    p("-r", "--reverse", help="reverse ordering", action="store_true")
    p("-s", "--size", help="show total file sizes", action="store_true")
    p("-u", "--update", help="update the library", action="store_true")
    p("-v", "--verbose", help="verbose mode", action="store_true")
    p("--reset", help="reset the library", action="store_true")
    args = parser.parse_args()
    update = args.update
    reset = args.reset
    search = args.search
    verbose = args.verbose
    size = args.size
    number = args.number or 5
    reverse = False if args.reverse else True
    sort_by = 'added'

    if args.password:
        print(create_password(length=20))

    if args.files:
        process_files(update=update, search=search)
        return
    elif update:
        process_files(update=update)

    media_records = get_plex_info(update=update, reset=reset)
    library_records = get_library_records()

    records = sorted(media_records + library_records, key=lambda x: x.entry)

    if args.height:
        sort_by = 'height'

    if args.size:
        sort_by = 'size'

    if args.all:
        number = len(records)
        print('Showing all {number:,} records.')

    if not records:
        warn('No Records Found. Aborting.')
        return

    if args.dvd:
        dvds = [ x for x in records if 'mpeg2video' in x.search ]
        print(f"Found {len(dvds):,} uncompressed dvd titles in {len(records):,} records.")
        records = dvds

    if search:
        search_records(' '.join(search).lower(), records, display=True, verbose=verbose)
    else:
        records = sort_by_attrib_value(records, attrib=sort_by, number=number, reverse=reverse)

    if size:
        filter = [x for x in records if type(x.size)==int]
        total = sum([x.size for x in filter])
        print(f'Known size for {len(filter):,} of {len(records):,} records: {show_file_size(total)}.')

    df = get_dataframe(records)

    success(f'Completed in {showtime(clock)}.')

if __name__ == '__main__':
    main()