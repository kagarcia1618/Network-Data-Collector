from datetime import datetime
from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException

def napalm_ssh(driver,node,cli_cmd,username,password,mode):
    '''
    driver - device napalm network driver
    mgmt_ip - device management ip address
    cli_cmd - device cli_cmd to be executed
    '''
    timestamp = datetime.now().strftime("%d%b%Y")
    net_driver = get_network_driver(driver)
    device = net_driver(str(node.primary_ip4).split('/')[0], username, password, optional_args={'global_delay_factor': 2})
    try:
        device.open()
        output = device.cli(cli_cmd)
        device.close()
        wr_file = open( 'logs/' + node.name.split(":")[0] + '_' + str(node.primary_ip4).split('/')[0] + '_' + timestamp + '.' + mode, 'w' )
        for i in output:
            wr_file.write( i + '\n' + output[i] + '\n')
        wr_file.close()
        return print(f'  {node.name.split(":")[0]} {mode} via napalm ssh data collection success!')
    except (ConnectionException) as error:
        wr_file = open( 'logs/' + node.name.split(":")[0] + '_' + str(node.primary_ip4).split('/')[0] + '_' + timestamp + '.' + mode, 'w' )
        wr_file.write(str(error))
        wr_file.close()
        return print(f'  {node.name.split(":")[0]} {mode} via napalm ssh data collection failed!')
