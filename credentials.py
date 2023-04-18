import os
from getpass import getpass
from library.encrypt import generate_key,encrypt_message
from library.extract import extract

def main():
    try:
        extract('private/.secret.key')
        print('[INFO] Secret key located.')

    except (FileNotFoundError):
        print('[WARNING] Secret key not found.')
        print('[INFO] Generating secret key in private directory.')
        generate_key()
        print('[INFO] Secret key created.')

    netdev_user = encrypt_message(input('Network Device Username: ')).decode()
    netdev_pass = encrypt_message(getpass('Network Device Password: ')).decode()
    netbox_url = input('Netbox URL: ')
    netbox_token = encrypt_message(getpass('Netbox Token: ')).decode()

    credentials = f'{netdev_user},{netdev_pass},{netbox_token}'
    webportals = f'NETBOX={netbox_url}'

    with open("private/credentials.txt", "w") as key_file:
        key_file.write(credentials)

    with open("private/webportals.txt", "w") as key_file:
        key_file.write(webportals)

    print('Credential and web portal details updated.')

if __name__ == '__main__':
    LOCAL_PATHS = ['logs', 'private', 'custom_logs']
    for path in LOCAL_PATHS:
        if not os.path.exists(path):
            os.mkdir(path)
            print(f'[INFO] Created {path} local folder.')
    main()
