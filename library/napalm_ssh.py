from datetime import datetime
from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from library.encrypt import decrypt_message

def napalm_ssh(driver,node,cli_cmd,username,password,mode):
    '''
    driver - device napalm network driver
    mgmt_ip - device management ip address
    cli_cmd - device cli_cmd to be executed
    '''
    timestamp = datetime.now().strftime("%d%b%Y")
    net_driver = get_network_driver(driver)
    device = net_driver(node[2], username, password)
    try:
        device.open()
        output = device.cli(cli_cmd)
        device.close()

        wr_file = open( 'logs/' + node[1] + '_' + node[2] + '_' + timestamp + '.' + mode, 'w' )
        for i in output:
            wr_file.write( i + '\n' + output[i] + '\n')
        wr_file.close()

    except (ConnectionException) as error:
        wr_file = open( 'logs/' + node[1] + '_' + node[2] + '_' + timestamp + '.' + mode, 'w' )
        wr_file.write(str(error))
        wr_file.close()
    return print( node[1] + 'completed' )