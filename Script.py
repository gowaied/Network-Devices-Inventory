from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException
from getpass import getpass
import ipaddress
import time

switches = {

    'SW1' : '192.168.81.140',
    'SW2' : '192.168.81.141'
}

routers = {

    'R1' : '192.168.81.139',
    'R2' : '192.168.81.134',
    'R3' : '192.168.81.137',
    'R4' : '192.168.81.138',
}

ospf_networks = {
    'R1' : ['192.168.81.139', '172.16.0.1', '10.0.0.1', '1.1.1.1'],
    'R2' : ['192.168.81.134', '172.16.0.2', '10.0.0.2', '2.2.2.2'],
    'R3' : ['192.168.81.137', '172.16.0.3', '10.0.0.3', '3.3.3.3'],
    'R4' : ['192.168.81.138', '172.16.0.4', '10.0.0.4', '4.4.4.4'],
}

password = getpass('Enter Password: ')
secret = getpass('Enter Secret: ')

for switch, ip in switches.items():

    device = {
        'device_type' : 'cisco_ios',
        'host' : ip,
        'username' : 'admin',
        'password' : password,
        'secret' : secret
    }

    try:
        print(f'Connecting to {switch}..........')
        time.sleep(1)
        ssh_switch = ConnectHandler(**device)
        ssh_switch.enable()

        while True:
            loopback_ip = input('Loopback IP: ')
            loopback_mask = input('Loopback Subnet Mask: ')

            try:
                ipaddress.IPv4Network(loopback_ip)
                break
            except ipaddress.AddressValueError:
                print(f'{loopback_ip} is not valid, please try another one!')
        
        commands = [
            'user gowaied priv 15 secret Mohamed',
            'int lo 0',
            f'ip address {loopback_ip} {loopback_mask}'
        ]
        config = ssh_switch.send_config_set(commands)
        print(config)
        verification = ssh_switch.send_command('sh ip int br | ex un')
        print(verification)
        ssh_switch.save_config()

    except NetMikoAuthenticationException:
        print(f'Failed to connect to {switch}, please check credintials!')
    except NetMikoTimeoutException:
        print(f'Failed to connect to {switch}, please check reachability!')


for router, ip in routers.items():

    device = {
        'device_type' : 'cisco_ios',
        'host' : ip,
        'username' : 'admin',
        'password' : password,
        'secret' : secret
    }

    try:
        print('**************************************************************************')
        print(f'Connecting to {router}..........')
        time.sleep(1)
        ssh_router = ConnectHandler(**device)
        ssh_router.enable()

        while True:
            loopback_ip = input('Loopback IP: ')
            loopback_mask = input('Loopback Subnet Mask: ')
            try:
                ipaddress.IPv4Network(loopback_ip)
                break
            except ipaddress.AddressValueError:
                print(f'{loopback_ip} is invalid, please try another one!')

        commands = [
            'user gowaied priv 15 secret Mohamed',
            'int lo 0',
            f'ip address {loopback_ip} {loopback_mask}',
            'router ospf 1',
            'passive-interface lo0'
        ]

        if router in ospf_networks:
            networks = ospf_networks[router]
            for network in networks:
                commands.append(f'network {network} 0.0.0.0 area 0')

        config = ssh_router.send_config_set(commands)
        print(config)
        loopback_verification = ssh_router.send_command('sh ip int br | ex un')
        print(loopback_verification)
        print('**************************************************************************')
        ospf_verification = ssh_router.send_command('sh ip proto | sec ospf')
        print(ospf_verification)

        ssh_router.save_config()
    except NetMikoAuthenticationException:
        print(f'Failed to connect to {router}, please check credintials!')
    except NetMikoTimeoutException:
        print(f'Failed to connect to {router}, please check reachability!')


