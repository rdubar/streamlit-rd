#!/usr/bin/python

import os, time, pickle, toml
import timeago
from datetime import datetime

from settings import TOML_FILE

from colorama import init, Fore

init(autoreset=True)


def warn(text):
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
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)


def get_modified_time(path, str=False):
    ''' return modified file time of path, or zero if file does not exist '''
    if not os.path.exists(path):
        return 0
    t = os.path.getmtime(path)
    return time.ctime(t) if str else t


def get_all_files(root_dir: str, verbose=False, ignore=[], purge=[], quiet=False) -> dict:
    ''' Returns a list of paths for all files recursively at root_dir '''
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
    if not quiet: print(f'Got {len(path_list):,} and skipped {len(skipped_list):,} items in {showtime(clock)}.')
    if verbose: print(f'Skipped list: {skipped_list}')
    return path_list


def show_file_size(bytes, r=1):
    if not bytes: return ''
    terabytes = bytes / (10 ** 12)
    if terabytes > 1: return f'{round(terabytes, r):,}TB'
    gigabytes = bytes / (10 ** 9)
    if gigabytes > 1: return f'{round(gigabytes, r):,}GB'
    megabytes = bytes / (10 ** 6)
    if megabytes > 1: return f'{round(megabytes, r):,}MB'
    kilobytes = bytes / (10 ** 3)
    if kilobytes > 1: return f'{round(kilobytes, r):,}kb'
    # else
    return f'{bytes} bytes'


def get_size_of_files(path_list):
    try:
        size = sum(os.path.getsize(path) for path in path_list)
    except Exception as e:
        print(f'Failed to get size of path_list: {e}')
        return
    print(show_file_size(size))
    return size


def showtime(s: float) -> str:
    """ return seconds (s) as H:M:S or seconds < 10 """
    if s < 0.1:
        return f'{s:.5f} seconds'
    elif s < 100:
        return f'{s:.2f} seconds'
    else:
        return datetime.timedelta(seconds=round(s))


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
    if os.path.exists(temp): os.remove(temp)
    with open(temp, 'wb') as handle:
        pickle.dump(data, handle)
    if os.path.exists(backup): os.remove(backup)
    if os.path.exists(path): os.rename(path, backup)
    os.rename(temp, path)
    modified = get_modified_time(path, str=True)
    log(f'Saved {len(data):,} records to {path}, {modified}.')
    return True


def load_data(path):
    if not os.path.exists(path):
        warn(f'No data file at {path}')
        return []
    modified = time_ago(get_modified_time(path, str=False))
    with open(path, 'rb') as handle:
        try:
            data = pickle.load(handle)
        except Exception as e:
            warn(f'FAILED TO LOAD: {path}: {e}')
            return []
    log(f'Loaded {len(data):,} records from {path}, last updated {modified}.')
    return data


def read_toml(path=TOML_FILE, section=None, debug=False):
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
    if debug: print(data)
    return data


def custom_key(obj, attr_name):
    """ ChatGPT derived function to enable sorting of list of objects of mixed types by an attribute """
    elem = getattr(obj, attr_name, None)
    if elem is None:
        return (0, None)
    elif isinstance(elem, int):
        return (1, elem)
    elif isinstance(elem, str):
        return (2, elem.lower())
    elif isinstance(elem, datetime):
        return (3, elem)
    else:
        return (4, str(elem))


def sort_records(records, attrib='added', reverse=True, display=True, number=5, verbose=False):
    """ Sort list of objects by attribute, with display option: can be mixed types """
    r = f' (reversed)' if reverse else ''
    count = len(records)
    if number > count: number = count
    if display or verbose: print(f'Showing {number:,} of {count:,} records sorted by "{attrib}"{r}.')
    sorted_list = sorted(records, key=lambda x: custom_key(x, attrib), reverse=reverse)
    if number > count or verbose: number = count
    if display or verbose:
        for i in range(number):
            print(sorted_list[i])
    return sorted_list


def search_records(text, data, display=True, verbose=False, attrib=None, match=None):
    """
    :param text: text to search for
    :param data: list of items to search
    :param display: if True, print items
    :param verbose: if True, print full info about result
    :param attrib: if present, filter results by attrib
    :param match: if present, only show results matcching this text
    :return:
    """

    if attrib:
        filtered = [x for x in data if hasattr(x, attrib)]
        if match: filtered = [x for x in filtered if getattr((x, attrib)) == match]
        if display:
            m = f'="{match}"' if match else ''
            print(f'Filtered {len(filtered)} of len(data) objects for "attrib"{m}')
        data = filtered

    matches = []
    for object in data:
        if text in object.search:
            matches.append(object)

    if display:
        output = f'Found {len(matches):,} matches in {len(data):,} entries for "{text}".'
        print(output)
        for x in matches:
            print(x.display())
            if verbose: print(x.search)
        if len(matches) > 10:
            print(output)
    return matches


def sort_by_attrib_value(objects, attrib='added', reverse=False, number=0, display=True, verbose=False):
    """"
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
    sorted_list = sorted(list1, key=lambda x: getattr(x, attrib), reverse=reverse) + list2 + list3
    l1 = len(list1)
    total = len(sorted_list)
    if verbose:
        l2 = len(list2)
        l3 = len(list3)
        print(f'sort_by_attrib_value: "{attrib}" has_attr({l1}), none_or_null({l2}), no_attr({l3}).')
    if display or verbose:
        r = f' (reversed)' if reverse else ''
        if number > total: number = total
        print(f'Showing {number:,} of {total:,} items sorted by "{attrib}"{r}.')
        for i in range(number):
            print(sorted_list[i])
    return sorted_list


def main():
    print("Rog's Tools.")

    # path_list = get_all_files('..')
    # get_size_of_files(path_list)
    # read_env()


if __name__ == "__main__":
    main()
