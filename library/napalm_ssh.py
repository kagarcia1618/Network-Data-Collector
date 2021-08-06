from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from .encrypt import decrypt_message

def napalm_ssh(Driver,Mgmt_ip,Command):
    '''
    driver - device napalm network driver
    mgmt_ip - device management ip address
    command - device command to be executed
    '''
    driver = get_network_driver(Driver)
    credential = open('utilities/login_credentials.txt', 'r').read().splitlines()
    username = decrypt_message(credential[0].encode())
    password = decrypt_message(credential[1].encode())
    device = driver(Mgmt_ip, username, password)
    try:
        device.open()
        output = device.cli(Command)
        device.close()
    except (ConnectionException) as error:
        output = error    
    return