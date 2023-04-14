import os.path
import time
from dataclasses import dataclass, field

from tools.utils import warn, info, success, show_file_size, display_objects, show_time, save_data, load_data
from settings import FILE_OBJECTS_PATH, IGNORE_LIST
from tools.remote import remote_command, remote_info
from datetime import datetime

FILE_OBJECTS = []


def file_objects(update=False):
    global FILE_OBJECTS
    if update or not FILE_OBJECTS:
        FILE_OBJECTS = get_file_objects(update=update)
    return FILE_OBJECTS


@dataclass(order=True)
class FileObject:
    """ An object for media titles """
    path: str
    size: int = 0
    info: str = None
    date: datetime = None

    def __post_init__(self):
        self.search = self.path.lower()
        if '/' not in self.path:
            return
        parts = self.path.split('/')
        self.group = parts[4]  # e.g. incoming or movies
        self.title = parts[5]  # e.g. artist or movie title
        self.filename = self.path[self.path.rfind('/') + 1:]
        self.filetype = self.filename[self.filename.rfind('.') + 1:]

    def __str__(self):
        s = show_file_size(self.size)
        # "%Y-%m-%d
        return f'{s:>8}  {self.path}'


@dataclass(order=True)
class MediaObject:
    """ A Media folder and its contents """
    title: str
    paths: list = field(default_factory=list)
    size: int = 0

    def __str__(self):
        s = show_file_size(self.size)
        n = len(self.paths)
        return f'{s:>8} {n:>5}  {self.title}'


def get_file_objects(path=FILE_OBJECTS_PATH, update=True):
    if update:
        file_obj = []
    else:
        file_obj = load_data(path)
    if not update and file_obj:
        return file_obj
    location_info = remote_info()
    if 'remote_directory' in location_info and os.path.exists(location_info['remote_directory']):
        warn(location_info['remote_directory']+' found locally! Please process directly')
    file_obj = get_remote_files()
    save_data(path, file_obj)
    return file_obj


def check_incoming():
    results = remote_command(command='/home/pi/usr/media/incoming.py', display=False)
    print(results)


def get_remote_files(ignore=IGNORE_LIST):
    print('Getting remote files...')
    clock = time.perf_counter()
    file_obj = []
    ignored_count = 0
    ignored_size = 0
    output = remote_command(command='ls -lR /mnt/expansion/media', display=False)
    directory = ''
    current_year = datetime.now().strftime("%Y")
    for line in output.split('\n'):

        """ line format: xr-x 1 pi pi 242984628 Jul 16  2019 Veep S04E10.mp4 """
        if len(line) > 0 and line[0] == '/':
            directory = line[:-1]
            continue
        else:
            parts = line.split()
            if len(parts) < 9:
                continue
        size = int(parts[4])
        if size == 262144:
            continue  # hack to ignore folders
        name = ' '.join(parts[8:])
        path = directory+'/'+name

        ignore_flag = False
        for check in ignore:
            if check in path:
                ignore_flag = True
                ignored_count += 1
                ignored_size += size
                break
        if ignore_flag:
            continue

        if ':' in parts[7]:  # the file's date is this year
            parts[7] = current_year
        date_str = ' '.join(parts[5:8])
        date_obj = datetime.strptime(date_str, "%b %d %Y")
        obj = FileObject(path=path, size=int(size), info=str(info), date=date_obj)
        file_obj.append(obj)
    clock = time.perf_counter() - clock
    success(f'Got {len(file_obj):,} remote paths in {show_time(clock)}.')
    if ignored_count:
        print(f'Ignored {ignored_count:,} files totalling {(show_file_size(ignored_size))}.')
    return file_obj


def show_folders(obj=None, number=5, search=None, reverse=False):
    if obj is None:
        obj = file_objects()
    folders = {}
    for x in obj:
        title = x.title
        if title not in folders:
            m = MediaObject(title=title)
            folders[title] = m
        folders[title].size += x.size
        folders[title].paths.append(x.path)
    media_objects = sorted(list(folders.values()), key=lambda y: y.size, reverse=reverse)
    total = len(media_objects)
    info(f'Showing largest {number:,} of {total:,} folders:')
    if number > total:
        number = total
    if search:
        if type(search) is list:
            search = ' '.join(search)
        lower = search.lower()
        matches = []
        for x in media_objects:
            if lower in x.title.lower():
                matches.append(x)
        info(f'Showing {len(matches)} of {total:,} folders:')
        [print(x) for x in matches]
        return matches
    else:
        for i in range(number):
            print(media_objects[i])
        return media_objects

def show_large_others(obj=None, verbose=False, minimum=500 * 1000 * 1000):
    if obj is None:
        obj = file_objects()
    # looking for large 'other' files
    matches = [x for x in obj if 'other' in x.path and x.size > minimum]
    total = show_file_size(sum([x.size for x in matches]))
    output = f"Found {len(matches):,} 'other' files larger than {show_file_size(minimum)} (totalling {total})."
    print(output)
    if verbose:
        [print(x) for x in matches]
        print(output)
    return matches


def process_files(update=False):
    """ get file objects, search if necessary """
    check_incoming()
    file_obj = get_file_objects(update=update)
    total_size = sum([x.size for x in file_obj])
    info(f'Found {len(file_obj):,} files totalling {show_file_size(total_size)}.')
    return file_objects


def show_files(obj=None, search=None, number=5, sort='size', reverse=False):
    if obj is None:
        obj = file_objects()
    display_objects(obj, search=search, number=number, sort=sort, reverse=reverse)


def main():
    process_files(update=True)


if __name__ == "__main__":
    main()
