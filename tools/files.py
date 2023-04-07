import os.path, time
from dataclasses import dataclass, field

from tools.utils import warn, info, success, show_file_size, display_objects, show_time, save_data, load_data
from settings import FILE_OBJECTS
from tools.remote import remote_command, remote_info
from datetime import datetime

@dataclass(order=True)
class FileObject:
    """ An object for media titles """
    path: str
    size: int = 0
    info: str = None
    date: datetime = None

    def __post_init__(self):
        self.search = self.path.lower()
        if '/' not in self.path: return
        parts = self.path.split('/')
        self.group = parts[4]  # e.g. incoming or movies
        self.title = parts[5]  # e.g. artist or movie title
        self.filename = self.path[self.path.rfind('/') + 1:]
        self.filetype = self.filename[self.filename.rfind('.') + 1:]

    def __str__(self):
        s = show_file_size(self.size)
        date_str = self.date.strftime("%Y-%m-%d")
        return f'{s:>8}  {self.path}'


@dataclass(order=True)
class MediaObject:
    """ A Media folder and its contents """
    title: str
    paths: list = field(default_factory=list)
    size: int = 0

    def __str__(self):
        s = show_file_size((self.size))
        n = len(self.paths)
        return f'{s:>8} {n:>5}  {self.title}'


def get_file_objects(path=FILE_OBJECTS, update=True):
    if not update:
        file_objects = load_data(path)
    if not update and file_objects:
        return file_objects
    location_info = remote_info()
    if 'remote_directory' in location_info and os.path.exists(location_info['remote_directory']):
        warn(location_info['remote_directory']+' found locally! Please process directly')
        results = []

    file_objects = get_remote_files()
    save_data(path, file_objects)
    return file_objects


def check_incoming():
    results = remote_command(command='/home/pi/usr/media/incoming.py', display=False)
    print(results)

def get_remote_files():
    print('Getting remote files...')
    clock = time.perf_counter()
    file_objects = []
    output = remote_command(command='ls -lR /mnt/expansion/media', display=False)
    directory = ''
    current_year = datetime.now().strftime("%Y")
    for line in output.split('\n'):
        # line format: -rwxr-xr-x 1 pi pi 242984628 Jul 16  2019 Veep S04E10.mp4
        if len(line) > 0 and line[0]=='/':
            directory = line[:-1]
            continue
        else:
            parts = line.split()
            if len(parts) < 9:
                continue
        size = int(parts[4])
        if size == 262144: continue # hack to ignore folders
        name = ' '.join(parts[8:])
        path = directory+'/'+name
        if ':' in parts[7]: # the file's date is this year
            parts[7] = current_year
        date_str = ' '.join(parts[5:8])
        date_obj = datetime.strptime(date_str, "%b %d %Y")
        object = FileObject(path=path, size=int(size), info=info, date=date_obj)
        file_objects.append(object)
    clock = time.perf_counter() - clock
    success(f'Got {len(file_objects):,} remote paths in {show_time(clock)}.')
    return file_objects


def show_folders(file_objects, number=5):
    folders = {}
    for x in file_objects:
        title = x.title
        if not title in folders:
            m = MediaObject(title=title)
            folders[title] = m
        folders[title].size += x.size
        folders[title].paths.append(x.path)
    media_objects = sorted(list(folders.values()), key=lambda x: x.size, reverse=True)
    total = len(media_objects)
    if number > total: number = total
    info(f'Showing largest {number:,} of {total:,} folders:')
    for i in range(number):
        print(media_objects[i])

def process_files(update=False, search=None, number=5, reverse=False):
    """ get file objects, search if necessary """
    check_incoming()
    file_objects = get_file_objects(update=update)
    total_size = sum([x.size for x in file_objects])
    info(f'Found {len(file_objects):,} files totalling {show_file_size(total_size)}.')

    display_objects(file_objects, search=search, number=number,
                    reverse=reverse)

    show_folders(file_objects)

    print('Looking for files to purge...')
    files_to_remove = []
    for x in file_objects:
        path = x.path
        for check in [ '/www.YTS', '/RARBG_DO_NOT_MIRROR.exe', '/RARBG.txt', '/WWW.YIFY-TORRENTS']:
            if check in path:
                files_to_remove.append(path)
                continue
    text = "rm "
    for p in files_to_remove:
        text += f'"{p}" '
    print(text)


    return file_objects


def main():
    process_files(update=True)

if __name__== "__main__" :
    main()