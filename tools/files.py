import os.path
from dataclasses import dataclass

from tools.utils import warn, info, show_file_size, sort_by_attrib_value, save_data, load_data
from settings import FILE_OBJECTS
from tools.remote import remote_command
import datetime

@dataclass(order=True)
class FileObject:
    """ An object for media titles """
    path: str
    size: int = 0
    info: str = None
    updated: datetime = None

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
        return f'{s:>10}  {self.path}'


def process_remote_results(results):
    if type(results)==str: results = results.split('\n')
    object_list = []
    for info in results:
        if not '\t' in info or not '.' in info: continue
        ending = info[info.rfind('.')+1:]
        if len(ending)>5: continue
        size, path = info.split('\t',1)
        object = FileObject(path=path, size=int(size)*1024, info=info)
        object_list.append(object)
    return object_list


def get_file_objects(path=FILE_OBJECTS, update=True):
    info('Getting file records...')
    if not update:
        file_objects = load_data(path)
    if not update and file_objects:
        return file_objects
    location_info = files_info()
    if 'remote_directory' in location_info and os.path.exists(location_info['remote_directory']):
        warn(location_info['remote_directory']+' found locally! Please process directly')
        results = []
    # else
    results = remote_command(command="du -a /mnt/expansion/media")
    ip = location_info['hostname']
    dir = location_info['remote_directory']
    info(f'Got {len(results):,} results from {ip}:{dir}.')
    file_objects = process_remote_results(results)
    save_data(path, file_objects)
    return file_objects


def check_incoming():
    results = remote_command(command='/home/pi/usr/media/incoming.py')
    print(results)


def process_files(update=False, search=None, number=5, reverse=False):
    """ get file objects, search if necessary """

    check_incoming()

    file_objects = get_file_objects(update=update)
    total_size = sum([x.size for x in file_objects])
    info(f'Found {len(file_objects):,} files totalling {show_file_size(total_size)}.')

    if search:
        if type(search)==list: search = ' '.join(search)
        lower = search.lower()
        matches = [ x for x in file_objects if lower in x.search ]
        [ print(x) for x in matches ]
        s = show_file_size(sum([x.size for x in matches]))
        info(f'Found {len(matches):} matches in {len(file_objects):,} paths for "{search}", totalling ({s}).')
    else:
        sort_by_size = sort_by_attrib_value(file_objects, 'size', display=True, number=5, reverse=True)

    return


def main():
    info("Rog's file processor.")

    check_incoming()
    process_files()

if __name__== "__main__" :
    main()