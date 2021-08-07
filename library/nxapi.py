import json
import requests
import urllib3
from datetime import datetime
from library.napalm_ssh import napalm_ssh

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def nxapi_cli(node, cli_cmd, cli_type, username, password, mode):
    '''
    node_ip - ip address of the device to be accessed
    cli_cmd - cli command to be executed to the device
    cli_type - nxapi cli access type
    mode - log file type
    '''
    timestamp = datetime.now().strftime("%d%b%Y")
    url = 'https://{}/ins'.format(node[2])
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

        wr_file = open( 'logs/' + node[1] + '_' + node[2] + '_' + timestamp + '.' + mode, 'w' )
        if type(output) == list:
            for i in output:
                wr_file.write( output[i]['input'] + '\n' + output[i]['body'] + '\n')
        else:
            wr_file.write( output['input'] + '\n' + output['body'] + '\n')
        wr_file.close()
        return print(f'{node[1]} {mode} collection success!')
    
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as error:
        print('before napalm ssh')
        napalm_ssh('nxos_ssh',node,cli_cmd,username,password,mode)
        print('after napalm ssh')
        #wr_file = open( 'logs/' + node[1] + '_' + node[2] + '_' + timestamp + '.' + mode, 'w' )
        #wr_file.write(str(error))
        #wr_file.close()
        #return print(f'{node[1]} {mode} collection failed!')