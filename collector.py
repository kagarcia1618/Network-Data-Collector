import concurrent
import argparse
from os import system, chdir, mkdir
from datetime import datetime
from collections import OrderedDict
from library.encrypt import decrypt_message
from library.nxapi import nxapi_cli
from library.napalm_ssh import napalm_ssh
from library.netbox_api import get_data
from library.extract import extract

def multitask(
    username: str,
    password: str,
    nxos_cmd_cfg: list,
    ios_cmd_cfg: list,
    iosxr_cmd_cfg: list,
    junos_cmd_cfg: list,
    nxos_cmd_log: list,
    ios_cmd_log: list,
    iosxr_cmd_log: list,
    junos_cmd_log: list,
    nxos_devices: list,
    ios_devices: list,
    iosxr_devices: list,
    junos_devices: list,
    folder: str = None,
    custom: bool = False,
) -> None:
    '''
    Function for multithreading task execution for different NOS platforms
    '''
    #Multithreading for NXOS
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=50)
    futures_nxos_cfg = [executor.submit(
        nxapi_cli, 
        node,
        nxos_cmd_cfg,
        'cli_show_ascii',
        username,
        password,
        'cfg',
        folder,
        custom) for node in nxos_devices]

    #Multithreading for IOS
    futures_ios_cfg = [executor.submit(
        napalm_ssh,
        'ios',
        node,
        ios_cmd_cfg,
        username,
        password,
        'cfg',
        folder,
        custom) for node in ios_devices]

    #Multithreading for IOS-XR
    futures_iosxr_cfg = [executor.submit(
        napalm_ssh,
        'iosxr',
        node,
        iosxr_cmd_cfg,
        username,
        password,
        'cfg',
        folder,
        custom) for node in iosxr_devices]

    #Multithreading for JUNOS
    futures_junos_cfg = [executor.submit(
        napalm_ssh,
        'junos',
        node,
        junos_cmd_cfg,
        username,
        password,
        'cfg',
        folder,
        custom) for node in junos_devices]
   
    futures_nxos_log = [executor.submit(
        napalm_ssh, 
        'nxos_ssh',
        node,
        nxos_cmd_log,
        username,
        password,
        'log',
        folder,
        custom) for node in nxos_devices]
    # futures_nxos_log = [executor.submit(
    #     nxapi_cli, 
    #     node,
    #     nxos_cmd_log,
    #     'cli_show_ascii',
    #     username,
    #     password,
    #     'log',
    #     custom) for node in nxos_devices]

    futures_junos_log = [executor.submit(
        napalm_ssh,
        'junos',
        node,
        junos_cmd_log,
        username,
        password,
        'log',
        folder,
        custom) for node in junos_devices]

    futures_ios_log = [executor.submit(
        napalm_ssh,
        'ios',
        node,
        ios_cmd_log,
        username,
        password,
        'log',
        folder,
        custom) for node in ios_devices]
    futures_iosxr_log = [executor.submit(
        napalm_ssh,
        'iosxr',
        node,
        iosxr_cmd_log,
        username,
        password,
        'log',
        folder,
        custom) for node in iosxr_devices]
    
    futures = futures_nxos_log + futures_junos_log +\
        futures_ios_log + futures_iosxr_log +\
        futures_nxos_cfg + futures_junos_cfg +\
        futures_ios_cfg + futures_iosxr_cfg
    
    concurrent.futures.wait(futures)

def main(username, password) -> None:
    '''
    Main function to collect network data
    '''
    start_time = datetime.now()
    print('\n**************** S T A R T  O F  T H E  S C R I P T ****************\n')

    #temporary storage of the raw data of cli commands
    cmd_raw = extract('private/command_list.txt')

    #parsed command lines
    cmd_list = [ i.split(',') for i in cmd_raw.splitlines() ]

    #Get device list from netbox
    devices = get_data()

    #Group same type of devices
    nxos_devices = []
    ios_devices = []
    iosxr_devices = []
    junos_devices = []

    #Group same type of commands
    nxos_cmd_cfg = []
    nxos_cmd_log = []
    ios_cmd_cfg = []
    ios_cmd_log = []
    iosxr_cmd_cfg = []
    iosxr_cmd_log = []
    junos_cmd_cfg = []
    junos_cmd_log = []

    for i in devices:
        if type(i.primary_ip) != type(None) and str(i.status) == 'Active':
            if str(i.platform) == 'Cisco NXOS':
                nxos_devices.append(i)
            elif str(i.platform) == 'Cisco IOS':
                ios_devices.append(i)
            elif str(i.platform) == 'Cisco IOS-XR':
                iosxr_devices.append(i)
            elif str(i.platform) == 'Juniper JunOS':
                junos_devices.append(i)

    for i in cmd_list:
        if i[0] == 'nxos':
            if i[1] == 'cfg':
                nxos_cmd_cfg.append(i[2])
            else:
                nxos_cmd_log.append(i[2])
        elif i[0] == 'ios':
            if i[1] == 'cfg':
                ios_cmd_cfg.append(i[2])
            else:
                ios_cmd_log.append(i[2])
        elif i[0] == 'ios-xr':
            if i[1] == 'cfg':
                iosxr_cmd_cfg.append(i[2])
            else:
                iosxr_cmd_log.append(i[2])
        elif i[0] == 'junos':
            if i[1] == 'cfg':
                junos_cmd_cfg.append(i[2])
            else:
                junos_cmd_log.append(i[2])

    #Zip the config files and move to archive folder
    system('zip -R $(echo cfg_backup_$(date +%d%b%Y)) logs/*.cfg && mv *.zip logs/archive/')
    #Zip the logs files and move to archive folder
    system('zip -R $(echo log_backup_$(date +%d%b%Y)) logs/*.log && mv *.zip logs/archive/')
    #Deletes all config and log files
    system('rm logs/*.cfg && rm logs/*.log')

    multitask(
        username = username,
        password = password,
        nxos_cmd_cfg = nxos_cmd_cfg,
        ios_cmd_cfg = ios_cmd_cfg,
        iosxr_cmd_cfg = iosxr_cmd_cfg,
        junos_cmd_cfg = junos_cmd_cfg,
        nxos_cmd_log = nxos_cmd_log,
        ios_cmd_log = ios_cmd_log,
        iosxr_cmd_log = iosxr_cmd_log,
        junos_cmd_log = junos_cmd_log,
        nxos_devices = nxos_devices,
        ios_devices = ios_devices,
        iosxr_devices = iosxr_devices,
        junos_devices = junos_devices,
    )

    end_time = datetime.now()
    total_time = (end_time - start_time).seconds
    print('\n****************** E N D  O F  T H E  S C R I P T ******************\n')
    print('  Start time : ' + start_time.strftime("%d %b %Y - %H:%M:%S"))
    print('  End time : ' + end_time.strftime("%d %b %Y - %H:%M:%S"))
    print('  Total time : ' + str(total_time//60) + ' minute/s and ' + str(total_time%60) + ' second/s')
    print('\n********************************************************************\n')

def custom(username, password, cmd_list, host_list, folder) -> None:
    #Get device list from netbox
    devices = get_data()
    hosts = list()
    for device in devices:
        if device.name in host_list:
            hosts.append(device)
            host_list.remove(device.name)
    
    if len(host_list) > 0:
        for host in host_list:
            print(f"{host} not found in NetBox record.")
        return

    #Group same type of devices
    nxos_devices = []
    ios_devices = []
    iosxr_devices = []
    junos_devices = []

    #Group same type of commands
    nxos_cmd_cfg = []
    nxos_cmd_log = []
    ios_cmd_cfg = []
    ios_cmd_log = []
    iosxr_cmd_cfg = []
    iosxr_cmd_log = []
    junos_cmd_cfg = []
    junos_cmd_log = []

    for i in hosts:
        if type(i.primary_ip) != type(None) and str(i.status) == 'Active':
            if str(i.platform) == 'Cisco NXOS':
                nxos_devices.append(i)
            elif str(i.platform) == 'Cisco IOS':
                ios_devices.append(i)
            elif str(i.platform) == 'Cisco IOS-XR':
                iosxr_devices.append(i)
            elif str(i.platform) == 'Juniper JunOS':
                junos_devices.append(i)

    for i in cmd_list:
        if i[0] == 'nxos':
            if i[1] == 'cfg':
                nxos_cmd_cfg.append(i[2])
            else:
                nxos_cmd_log.append(i[2])
        elif i[0] == 'ios':
            if i[1] == 'cfg':
                ios_cmd_cfg.append(i[2])
            else:
                ios_cmd_log.append(i[2])
        elif i[0] == 'ios-xr':
            if i[1] == 'cfg':
                iosxr_cmd_cfg.append(i[2])
            else:
                iosxr_cmd_log.append(i[2])
        elif i[0] == 'junos':
            if i[1] == 'cfg':
                junos_cmd_cfg.append(i[2])
            else:
                junos_cmd_log.append(i[2])

    multitask(
        username = username,
        password = password,
        nxos_cmd_cfg = nxos_cmd_cfg,
        ios_cmd_cfg = ios_cmd_cfg,
        iosxr_cmd_cfg = iosxr_cmd_cfg,
        junos_cmd_cfg = junos_cmd_cfg,
        nxos_cmd_log = nxos_cmd_log,
        ios_cmd_log = ios_cmd_log,
        iosxr_cmd_log = iosxr_cmd_log,
        junos_cmd_log = junos_cmd_log,
        nxos_devices = nxos_devices,
        ios_devices = ios_devices,
        iosxr_devices = iosxr_devices,
        junos_devices = junos_devices,
        folder = folder,
        custom = True,
    )

if __name__ == '__main__':
    #Extract login credentials
    username = decrypt_message(extract('private/credentials.txt').split(',')[0].encode())
    password = decrypt_message(extract('private/credentials.txt').split(',')[1].encode())

    parser = argparse.ArgumentParser(description='Network Data Collect Script')
    parser.add_argument(
        '--command_list',
        '-cl',
        help = 'Command list file',
        type = open,
    )
    parser.add_argument(
        '--host_list',
        '-hl',
        help='Host list file',
        type = open,
    )
    parser.add_argument(
        '--folder',
        '-f',
        help='Folder name',
    )
    args = parser.parse_args()

    if args.command_list and args.host_list and args.folder:
        host_list = args.host_list.read().splitlines()
        command_list = [ i.split(',') for i in args.command_list.read().splitlines() ]
        chdir('custom_logs')
        mkdir(args.folder)
        custom(username, password, command_list, host_list, args.folder)
    else:
        main(username, password)