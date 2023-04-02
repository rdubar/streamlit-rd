import paramiko

from tools.utils import read_toml, warn, success, info
from settings import TOML_FILE

def files_info():
    return read_toml(TOML_FILE, section = 'remote')

def remote_command(credentials=files_info(), command=None):
    """ Execute command remotely at site in credentials """
    try:
        hostname, port, username, password, _ = credentials.values()
    except Exception as e:
        warn(f'remote_connect failure: {credentials}\n{e}')
        return
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

    print (results)

    return results


def main():
    remote_command(command='ls /mnt/expansion/media/Incoming')

if __name__== "__main__" :
    main()