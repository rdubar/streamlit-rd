import time

import paramiko

from tools.utils import read_toml, warn, success, info, show_time
from settings import TOML_PATH

def remote_info():
    return read_toml(TOML_PATH, section ='remote')

def remote_command(command=None, credentials=remote_info(), display=True, secret=False):
    """ Execute command remotely at site in credentials """
    try:
        hostname, port, username, password, private = credentials.values()
    except Exception as e:
        warn(f'remote_connect failure: {credentials}\n{e}')
        return

    if command and secret:
        command = command + ' ' + private
    elif secret:
        command = private

    print(f'Executing "{command}" at {hostname}...')

    # create SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # connect to server
    ssh.connect(hostname, port, username, password)

    # execute command remotely
    stdin, stdout, stderr = ssh.exec_command(command)

    # print output of command
    results = stdout.read().decode()

    # close SSH connection
    ssh.close()

    if display: print(results)

    return results


def main():
    print(remote_command('ls'))

if __name__== "__main__" :
    main()