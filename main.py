import argparse
import time

from tools.utils import show_time, display_objects, warn, success, info, show_file_size
from tools.plex import get_plex_info
from tools.library import get_library_records
from tools.password import create_password
# from tools.dataframe import get_dataframe
from tools.files import process_files
from tools.download_video import get_movies


def main():
    clock = time.perf_counter()
    info("Rog's Plex Media Processor.")

    parser = argparse.ArgumentParser()
    p = parser.add_argument
    p("search", help="search the library", type=str, nargs='*')
    p("-a", "--all", help="show all matching", action="store_true")
    p("-f", "--files", help="search files instead of plex info", action="store_true")
    p('-H', '--height', help="sort by height", action="store_true")
    p("-d", "--dvd", help="show uncompressed DVD rips", action="store_true")
    p("-p", "--password", help="generate a secure password", action="store_true")
    p("-r", "--reverse", help="reverse ordering", action="store_true")
    p("-s", "--size", help="show total file sizes", action="store_true")
    p("-u", "--update", help="update the library", action="store_true")
    p("-v", "--verbose", help="verbose mode", action="store_true")
    p("--reset", help="reset the library", action="store_true")
    p("--video", help="download video", action="store_true")
    p("-A", '--attrib', help="sort by [attrib]", type=str, nargs='?', const="updated")
    p("-n", '--number', help="show [5] items", type=int, nargs='?', const=5)

    args = parser.parse_args()
    update = args.update
    reset = args.reset
    search = args.search
    verbose = args.verbose
    size = args.size
    number = args.number
    reverse = False if args.reverse else True
    sort_by = []

    if args.password:
        print(create_password(length=20))

    if args.attrib:
        sort_by.append(args.attrib)

    if args.video:
        get_movies(search)
        return

    if args.files:
        process_files(update=update, search=search)
        return
    elif update:
        process_files(update=update, number=number, reverse=reverse)

    media_records = get_plex_info(update=update, reset=reset)
    library_records = get_library_records()

    records = sorted(media_records + library_records, key=lambda x: x.entry)
    # df = get_dataframe(records)

    if not records:
        warn('No Records Found. Aborting.')
        return

    if args.dvd:
        dvds = [x for x in records if 'mpeg2video' in x.search]
        print(f"Found {len(dvds):,} uncompressed dvd titles in {len(records):,} records.")
        records = dvds

    if args.height:
        sort_by.append('height')

    if args.size:
        sort_by.append('size')

    if args.all:
        number = len(records)

    if not sort_by and search == []:
        sort_by = 'added'

    if search and not number:
        number = 20
    elif not number and not search:
        number = 5

    display_objects(records, search=search, sort=sort_by, number=number,
                    verbose=verbose, reverse=reverse, display='search')

    if size:
        filter_ = [x for x in records if type(x.size) == int]
        total = sum([x.size for x in filter_])
        print(f'Known size for {len(filter_):,} of {len(records):,} records: {show_file_size(total)}.')

    success(f'Completed in {show_time(clock)}.')


if __name__ == '__main__':
    main()
