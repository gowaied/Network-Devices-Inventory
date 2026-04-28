from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException
from getpass import getpass
import os

all_devices = {
    'SW1' : '192.168.81.140',
    'SW2' : '192.168.81.141',
    'R1' : '192.168.81.139',
    'R2' : '192.168.81.134',
    'R3' : ' 192.168.81.137',
    'R4' : '192.168.81.138'
}

password = getpass('Enter Password": ')
secret = getpass('Enter Secret": ')

for host, ip in all_devices.items():
    try:
        device = {
            'device_type' : 'cisco_ios',
            'host' : ip,
            'username' : 'admin',
            'password' : password,
            'secret' : secret
        }

        print(f'Connecting to {host}..........')

        ssh = ConnectHandler(**device)
        print(f'Gathering {host}\'s data.........')
    
        show_ip = ssh.send_command('show ip int br | ex un')
        show_version = ssh.send_command('show version')
        start_config = ssh.send_command('show start')

        os.makedirs(rf'E:\Cisco Devices Inventory\{host}', exist_ok=True)
        device_interfaces = open(rf'E:\Cisco Devices Inventory\{host}\Active_Interface.txt','x')
        device_interfaces.write(show_ip)
        device_version = open(rf'E:\Cisco Devices Inventory\{host}\Version.txt','x')
        device_version.write(show_version)
        device_config = open(rf'E:\Cisco Devices Inventory\{host}\config.txt','x')
        device_config.write(start_config)

        print(f'{host} has been added to the inventory!')
    

    except NetMikoAuthenticationException:
        print(f'Failed to connect to {host}, please check credintials!')

    except NetMikoTimeoutException:
        print(f'Failed to connect to {host}, please check reachability!')
