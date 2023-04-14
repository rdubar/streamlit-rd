#!/usr/bin/python

import os
import time
import pickle
import toml
from datetime import datetime, timedelta

from settings import TOML_PATH

import timeago
from colorama import init, Fore
init(autoreset=True)


def warn(text):
    """
    :param text: Warning text to print
    :return: None
    """
    print(Fore.RED + text)


def success(text):
    print(Fore.GREEN + text)


def info(text):
    print(Fore.BLUE + text)


def log(text):
    print(text)


def time_ago(date):
    now = datetime.now()
    return timeago.format(date, now)


def clear_line(n=1):
    """ Clear [1] line(s) from console """
    line_up = '\033[1A'
    line_clear = '\x1b[2K'
    for i in range(n):
        print(line_up, end=line_clear)


def get_modified_time(path, text=False):
    """ return modified file time of path, or zero if file does not exist """
    if not os.path.exists(path):
        return 0
    t = os.path.getmtime(path)
    return time.ctime(t) if text else t


def get_all_files(root_dir: str, verbose=False, ignore=None, purge=None, quiet=False) -> list:
    """ Returns a list of paths for all files recursively at root_dir """
    clock = time.perf_counter()
    print(f'Getting all files from: "{root_dir}" ...Please wait...')
    path_list = []
    skipped_list = []
    purge_list = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            delete = False
            skip = False
            path = os.path.join(root, file)
            for i in ignore:
                if i in path:
                    skip = True
                    break
            if not skip:
                for p in purge:
                    if p in path:
                        delete = True
                        break
            if delete:
                purge_list.append(path)
            elif skip:
                skipped_list.append(path)
            else:
                path_list.append(path)
    for p in purge_list:
        print(f'Deleting: {p}')
        os.remove(p)
    clock = time.perf_counter() - clock
    clear_line()
    if not quiet:
        print(f'Got {len(path_list):,} and skipped {len(skipped_list):,} items in {show_time(clock)}.')
    if verbose:
        print(f'Skipped list: {skipped_list}')
    return path_list


def show_file_size(bytes_, r=1):
    """ Return human-readable file size """
    if not bytes_:
        return ''
    terabytes = bytes_ / (10 ** 12)
    if terabytes > 1:
        return f'{round(terabytes, r):,}TB'
    gigabytes = bytes_ / (10 ** 9)
    if gigabytes > 1:
        return f'{round(gigabytes, r):,}GB'
    megabytes = bytes_ / (10 ** 6)
    if megabytes > 1:
        return f'{round(megabytes, r):,}MB'
    kilobytes = bytes_ / (10 ** 3)
    if kilobytes > 1:
        return f'{round(kilobytes, r):,}kb'
    # else
    return f'{bytes_} bytes'


def show_time(s: float):
    """ return seconds (s) as seconds or H:M:S """
    if s < 0.1:
        return f'{s:.5f} seconds'
    elif s < 100:
        return f'{s:.2f} seconds'
    else:
        return timedelta(seconds=round(s))


def save_data(path, data):
    """ save data to path """
    if not path:
        warn('Save data - no path given')
        return False
    if not data or len(data) == 0:
        warn(f'No data to save to {path}')
        return False
    backup = path + '.bak'
    temp = path + '.tmp'
    if os.path.exists(temp):
        os.remove(temp)
    with open(temp, 'wb') as handle:
        pickle.dump(data, handle)
    if os.path.exists(backup):
        os.remove(backup)
    if os.path.exists(path):
        os.rename(path, backup)
    os.rename(temp, path)
    modified = get_modified_time(path, text=True)
    log(f'Saved {len(data):,} records to {path}, {modified}.')
    return True


def load_data(path):
    """ load data from path """
    if not os.path.exists(path):
        warn(f'No data file at {path}')
        return []
    modified = time_ago(get_modified_time(path, text=False))
    with open(path, 'rb') as handle:
        try:
            data = pickle.load(handle)
        except Exception as e:
            warn(f'FAILED TO LOAD: {path}: {e}')
            return []
    log(f'Loaded {len(data):,} records from {path}, last updated {modified}.')
    return data


def read_toml(path=TOML_PATH, section=None, debug=False):
    """ Read an TOML file, return a dictionary """
    if not os.path.exists(path):
        warn(f'read_toml: file not found: {path}')
        return {}
    data = toml.load(path)
    if section:
        if section in data:
            data = data[section]
        else:
            warn('Read TOML: {section} not found in {path}.')
    if debug:
        print(data)
    return data


def sort_by_attrib_value(objects, attrib='added', reverse=False, verbose=False):
    """
    Sort list of objects by attrib, with objects that have that attrib first,
    either in normal or reverse order, then objects where attrib is None, then objects without attrib.
    """
    list1 = []  # objects where attrib is not None
    list2 = []  # objects where attrib is None
    list3 = []  # objects without attrib
    for x in objects:
        if hasattr(x, attrib):
            if getattr(x, attrib) not in [None, '', 0]:
                list1.append(x)
            else:
                list2.append(x)
        else:
            list3.append(x)
    sorted_list = sorted(list1, key=lambda y: getattr(y, attrib), reverse=reverse) + list2 + list3
    l1 = len(list1)
    if verbose:
        l2 = len(list2)
        l3 = len(list3)
        print(f'sort_by_attrib_value: "{attrib}" has_attr({l1}), none_or_null({l2}), no_attr({l3}).')
    return sorted_list


def ss(x):
    """ for pluralising words """
    return '' if x == 1 else 's'


def display_objects(objects, search=None, sort=None, number=5,
                    verbose=False, reverse=False, display='title', maximum=1000):
    """ Universal function to show objects """
    total = len(objects)
    lower = ''
    if search:
        if type(search) == list:
            search = ' '.join(search)
        lower = search.lower()
        objects = [x for x in objects if search in str(vars(x)).lower()]
        matches = len(objects)
    else:
        matches = 0

    if sort:
        if type(sort) == str:
            sort = [sort]
        for attrib in sort:
            objects = sort_by_attrib_value(objects, attrib=attrib, verbose=verbose, reverse=reverse)
        sort_str = ','.join(sort)
    else:
        sort_str = None

    if display:
        n = len(objects)
        if number == 0 or number is None or number > n:
            number = n

        text = f'Showing {number:,} of '
        if matches:
            text += f'{matches:,} matches for "{lower}" in '
        text += f'{total:,} records'
        if sort:
            text += f' (sorted by: {sort_str})'
        text += '.'
        print(text)

        if number > maximum:
            print(f'Not displaying over {maximum:,} objects.')
            return objects

        for i in range(number):
            x = objects[i]
            print(x)
            if verbose and hasattr(x, display):
                print(getattr(x, display))

    return objects


def main():
    print("Rog's Tools.")

    # path_list = get_all_files('..')
    # get_size_of_files(path_list)
    # read_env()


if __name__ == "__main__":
    main()
