import concurrent
from os import system
from datetime import datetime
from collections import OrderedDict
from library.encrypt import decrypt_message
from library.nxapi import nxapi_cli
from library.napalm_ssh import napalm_ssh

def extract(a):
    """
    a - exact filename of the data to be extracted
    """
    with open(a,'r') as i:
        return(i.read())

if __name__ == '__main__':
    start_time = datetime.now()
    print('\n**************** S T A R T  O F  T H E  S C R I P T ****************\n')
    #Extract login credentials
    username = decrypt_message(extract('private/login_credentials.txt').split(',')[0].encode())
    password = decrypt_message(extract('private/login_credentials.txt').split(',')[1].encode())

    #temporary storage of the raw data of cli commands
    cmd_raw = extract('private/command_list.txt')
    #temporary storage of the raw data of the nodes database
    node_raw = extract('private/device_list.txt')

    #parsed command lines
    cmd_list = [ i.split(',') for i in cmd_raw.splitlines() ]
    #parsed node list
    node_list = [ i.split(' ') for i in node_raw.splitlines() ]

    #Group same type of devices
    nxos_device = []
    ios_device = []
    iosxr_device = []
    junos_device = []

    #Group same type of commands
    nxos_cmd_cfg = []
    nxos_cmd_log = []
    ios_cmd_cfg = []
    ios_cmd_log = []
    iosxr_cmd_cfg = []
    iosxr_cmd_log = []
    junos_cmd_cfg = []
    junos_cmd_log = []

    for i in node_list:
        if i[0] == 'nxos':
            nxos_device.append(i)
        elif i[0] == 'ios':
            ios_device.append(i)
        elif i[0] == 'ios-xr':
            iosxr_device.append(i)
        elif i[0] == 'junos':
            junos_device.append(i)

    for i in cmd_list:
        if i[0] == 'nxos':
            if i[1] == 'cfg':
                nxos_cmd_cfg.append(i)
            else:
                nxos_cmd_log.append(i)
        elif i[0] == 'ios':
            if i[1] == 'cfg':
                ios_cmd_cfg.append(i)
            else:
                ios_cmd_log.append(i)
        elif i[0] == 'ios-xr':
            if i[1] == 'cfg':
                iosxr_cmd_cfg.append(i)
            else:
                iosxr_cmd_log.append(i)
        elif i[0] == 'junos':
            if i[1] == 'cfg':
                junos_cmd_cfg.append(i)
            else:
                junos_cmd_log.append(i)
    
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)
    futures = [
        executor.submit(
            nxapi_cli, 
            node,
            cli_cmd=nxos_cmd_cfg,
            cli_type='cli_show_ascii',
            username=username,
            password=password,
            mode='cfg'
        ) for node in nxos_device
    ]
    concurrent.futures.wait(futures)