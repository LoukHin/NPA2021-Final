from netmiko import ConnectHandler

host = "10.0.15.112"
username = "admin"
password = "cisco"

target_interface = "loop6207"
target_ip = "192.168.1.1"
target_subnet = "255.255.255.0"
target_slash_notation = "24"

with ConnectHandler(device_type="cisco_ios", ip=host, username=username, password=password) as ssh:
    interface_result = ssh.send_command(f"sh int {target_interface}", use_textfsm=True)[0]
    try:
        configured_ip, configured_subnet = interface_result["ip_address"].split("/")
        print(f"Interface {target_interface} exist.")
        if configured_ip == target_ip and configured_subnet == target_slash_notation:
            print(f"Interface {target_interface} configured correctly.")
            remove_interface(ssh, target_interface)
        else:
            print(f"Interface {target_interface} configured incorrectly.")
            config_interface_ip(ssh, target_interface, target_ip, target_subnet)

    except:
        print(f"Interface {target_interface} does not exist.")
        config_interface_ip(ssh, target_interface, target_ip, target_subnet)
