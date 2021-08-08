# Network Data Collector

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
        ```      

    - Command list

        Format: `{device type - ios|iosxr|nxos|junos},{logging mode - cfg|log},{cli command}`

        ```
        cat > command_list.txt
        ios,cfg,show run
        ```
    
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


