import json
import requests
import urllib3
from datetime import datetime
from library.napalm_ssh import napalm_ssh

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def nxapi_cli(node, cli_cmd, cli_type, username, password, mode, folder, custom):
    '''
    node_ip - ip address of the device to be accessed
    cli_cmd - cli command to be executed to the device
    cli_type - nxapi cli access type
    username - device login username
    password - device login password
    mode - file extension type
    custom - boolean indicator if custom mode network data collection
    '''
    if len(cli_cmd) == 0:
        return
    if custom:
        timestamp = datetime.now().strftime("%d%b%Y-%H%M")
        directory = f"{folder}/"
    else:
        timestamp = datetime.now().strftime("%d%b%Y")
        directory = 'logs/'
    url = 'https://{}/ins'.format(str(node.primary_ip4).split('/')[0])
    cli_cmd_str = ' ;'.join(cli_cmd)
    payload = {
        "ins_api":{
            "version": "1.0",
            "type": cli_type,
            "chunk": "0",
            "sid": "1",
            "input": cli_cmd_str,
            "output_format": "json"
        }
    }
    header = {'content-type':'application/json'}
    try:      
        response = requests.post(
            url,
            verify=False,
            timeout=10,
            data=json.dumps(payload),
            headers=header,
            auth=(username,password)
        ).json()
        output = response['ins_api']['outputs']['output']
        wr_file = open( directory + node.name + '_' + str(node.primary_ip4).split('/')[0] + '_' + timestamp + '.' + mode, 'w' )
        if type(output) == list:
            for i in range(len(output)):
                wr_file.write( output[i]['input'] + '\n' + output[i]['body'] + '\n')
        else:
            wr_file.write( output['input'] + '\n' + output['body'] + '\n')
        wr_file.close()
        return print(f'  {node.name} {mode} via nxapi data collection success!')
    
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as error:
        print(f'  {node.name} {mode} via nxapi data collection failed! Now trying via napalm ssh..')
        napalm_ssh('nxos_ssh', node, cli_cmd, username, password, mode, custom)
        return