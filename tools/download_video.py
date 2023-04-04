#!/usr/bin/python

import os, argparse, time, datetime
from yt_dlp import YoutubeDL

from colorama import init, Fore

init(autoreset=True)

from requests_html import HTMLSession


def get_title_from_url(url):
    return HTMLSession().get(url).html.find('title', first=True).text


SAVE_TO = [
    '/mnt/expansion/Media/Incoming',
    '/Users/roger/Downloads'
]

DEFAULT_FILE = '/home/pi/usr/media/data/movies.txt'


def set_directory(*dirs, default=SAVE_TO):
    '''
    Set directory to the first available from the list provided
    '''
    if not dirs:
        dirs = default
    if type(dirs) != list:
        dirs = [dirs]
    for directory in dirs:
        if os.path.isdir(directory):
            try:
                os.chdir(directory)
                break
            except:
                print(Fore.RED + f'Failed to change directory to {directory}')
    else:
        print(Fore.RED + 'Unable to set output directory to {directory}.')
    print(Fore.BLUE + 'Output directory: ', os.getcwd())


def showtime(s: float) -> str:
    ''' return seconds (s) as H:M:S or seconds < 10 '''
    return f'{s:.5f} seconds' if s < 10 else datetime.timedelta(seconds=s)


def get_movies(search, verbose=False):
    # is search term a file?
    clock = time.perf_counter()
    if verbose: print('Verbose mode. Does not do anything yet.')
    if search and search != []:
        print(Fore.MAGENTA + f'Getting movies: {search}')
    else:
        search = input(Fore.CYAN + "Enter URL, filename or search term: ")
    if type(search) == str and os.path.exists(search):
        with open(search) as f:
            lines = f.readlines()
            print(Fore.GREEN + f'Processing file {search} ({len(lines)} lines)')
    elif type(search) != list:
        lines = [search]
    else:
        lines = search

    # set working directory to ensure out in correct place
    set_directory()

    # Calculate how many items will be downloaded
    total = 0
    completed = 0

    def s(x):
        return '' if x == 1 else 's'

    # print(lines)
    for i in lines:
        if 'http' in i.lower():
            total += 1
    print(Fore.MAGENTA + f'{total} item{s(total)} to download.')

    for item in lines:
        if item[0] == '#':
            print(item)

        elif item[:4].lower() == 'http':
            print(Fore.GREEN + 'Downloading:', get_title_from_url(item))
            with YoutubeDL() as ydl:
                try:
                    ydl.download(item)
                except Exception as e:
                    print(Fore.RED + f'Error downloading {item}\n{e}')
            completed += 1
            print(Fore.GREEN + f'Downloaded {completed} of {total}.')

        else:
            s = item.replace(' ', '+')
            print(Fore.BLUE + f'Search for: {item}')
            print(Fore.MAGENTA + f'https://duckduckgo.com/?q={s}&iax=videos&ia=videos&iaf=videoDuration%3Along')
    clock = time.perf_counter() - clock
    print(Fore.GREEN + f'Completed tasks in {showtime(clock)}.')


def set_get_subtitles():
    print('Attempting to get subtitles...')
    ydl_opts = {
        # 'outtmpl': '/Downloads/%(title)s_%(ext)s.mp4',
        'format': '(bestvideo[width>=1080][ext=mp4])+bestaudio/best',
        'writesubtitles': True,
        'subtitle': '--write-sub --sub-lang en',
    }


def main():
    print(Fore.MAGENTA + "Roger's Video Downloader")
    parser = argparse.ArgumentParser()
    parser.add_argument("search", help="Search for movies (URL, filename or search term)", type=str, nargs='*')
    parser.add_argument("-f", "--file", help=f"Search using file (default: {DEFAULT_FILE})", nargs='*', type=get_movies)
    parser.add_argument("-s", "--subs", help="attempt to get subtitles", action="store_true")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()
    verbose = args.verbose
    if verbose: print(args)

    if args.subs:
        set_get_subtitles()

    if args.file is not None:
        search = args.file
    elif args.search == []:
        search = input(Fore.CYAN + "Enter URL, filename or search term: ")
    else:
        search = args.search

    if search:
        get_movies(search, verbose=verbose)


if __name__ == '__main__':
    main()
