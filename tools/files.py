import os.path, sys
from dataclasses import dataclass

import paramiko
from tools.utils import read_toml, warn, success, info, show_file_size, showtime, save_data, load_data
from settings import TOML_FILE, FILE_OBJECTS
import datetime, time

@dataclass(order=True)
class FileObject:
    """ An object for media titles """
    path: str
    size: int = 0
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


def files_info():
    return read_toml(TOML_FILE, section = 'remote')

def remote_connect(credentials=files_info(), command=None):
    try:
        hostname, port, username, password, remote_directory = credentials.values()
    except Exception as e:
        warn(f'remote_connect failure: {credentials}\n{e}')
        return
    print(f'Connecting to {hostname}. Please wait.')

    # create SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # connect to server
    ssh.connect(hostname, port, username, password)

    # execute command to list files in directory
    if command == None:
        command = 'du -a {}'.format(remote_directory)
    stdin, stdout, stderr = ssh.exec_command(command)

    # print output of command
    results = stdout.read().decode()

    # close SSH connection
    ssh.close()

    return results

def process_remote_results(results):
    if type(results)==str: results = results.split('\n')
    object_list = []
    for info in results:
        if not '\t' in info or not '.' in info: continue
        size, path = info.split('\t',1)
        object = FileObject(path=path, size=int(size))
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
    results = remote_connect(location_info)
    ip = location_info['hostname']
    dir = location_info['remote_directory']
    info(f'Got {len(results):,} results from {ip}:{dir}.')
    file_objects = process_remote_results(results)
    save_data(path, file_objects)
    return file_objects


def check_incoming():
    results = remote_connect(command='/home/pi/usr/media/incoming.py')
    print(results)

def process_files(update=False, search=None):
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

    return


def main():
    info("Rog's file processor.")

    check_incoming()
    process_files()

if __name__== "__main__" :
    main()