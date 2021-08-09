# Network Data Collector

Network data collector can be used for automated network devices config and logs collection which is then stored as a text files in your local enviroment. There are two data collection types which are `cfg` and `log` mode. You can specify your own set of commands base on  these two options. 

This tool is currently using two different modes of access which is via:
1. NXAPI/SSH for NXOS
2. SSH for IOS, IOS-XR and Junos network devices. 

[Napalm](https://github.com/napalm-automation/napalm) is used as backend library module for SSH access. The final output will then have two generated text files for each devices for the purpose of easier indexing and lookup. 

**Sample Use Case:**
- Scheduled configuration backup
- Scheduled device inventory and health checkup
- Dynamic lookup of hardware module serial number across all network devices using linux grep
- Dynamic lookup of endpoint mac address across all network devices using linux grep
- Dynamic lookup of change request ticket in interface descriptions across all network devices using linux grep

**How to use:**

1. Clone this git repository to your local linux environment.
2. Pip install the required modules.
3. Create a sub-directory under `network-data-collector/` named `logs` for storing collected config and log data.

   ```
   mkdir logs
   ```
4. Create a sub-directory under `network-data-collector/logs` named `archive` and `access_logs` for logs archive and collection task report.

   ```
   mkdir archive && mkdir access_logs
   ```

5. Create a sub-directory under `network-data-collector/` named `private` for local device list, command list, login credential and secret key. 

    - Device list 
    
        Format: `{device type - ios|iosxr|nxos|junos} {hostname} {ipv4 address}`

        ```
        cat > device_list.txt
        ios r1 192.168.0.1
        nxos leaf1 192.168.0.2
        ```      

    - Command list

        Format: `{device type - ios|iosxr|nxos|junos},{logging mode - cfg|log},{cli command}`

        ```
        cat > command_list.txt
        ios,cfg,show run
        ios,log,show version
        ios,log,show inventory
        nxos,cfg,show run
        nxos,log,show version
        nxos,log,show l2route evpn mac-ip all
        ```
        **Note:** Maximum of 10 command lines only for nxos device type
    
    - Secret Key

        Generate your own secret key using encrypt.py inside the `library` folder and save it as `.secret.key`.

        ```
        cat > .secret.key
        {Place here your generated secret key.}
        ```        

    - Login credential

        Generate a hash of your login credential across all your devices using  encrypt.py inside the `library` folder and save it as `login_credentials.txt`

        ```
        cat > login_credentials.txt
        {Place here your generated username hash.},{Place here your generated password hash.}
        ```    

6. Execute the collector python script using a virtual environment.
   ```
   source venv/bin/activate
   python collector.py
   ```

7. Verify that the collected cfg and log data has been stored in `logs` directory.

   Log file format:
   ```
   {hostname}_{ip address}_{ddmmmyyyy}.cfg
   {hostname}_{ip address}_{ddmmmyyyy}.log
   ```


