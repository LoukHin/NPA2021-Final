from netmiko import ConnectHandler

host = "10.0.15.112"
username = "admin"
password = "cisco"

target_interface = "loopback 62070184"
target_ip = "192.168.1.1"
target_subnet = "255.255.255.0"
target_slash_notation = "24"

def config_interface_ip(ssh, target_interface, target_ip, target_subnet):
    print(f"Configuring interface {target_interface}.")
    commands = [
        f"int {target_interface}",
        f"ip addr {target_ip} {target_subnet}",
        "no shut",
    ]
    ssh.send_config_set(commands)
    ssh.save_config()

def remove_interface(ssh, target_interface):
    print(f"Removing interface {target_interface}.")
    commands = [
        f"no int {target_interface}",
    ]
    ssh.send_config_set(commands)
    ssh.save_config()

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

    except TypeError:
        print(f"Interface {target_interface} does not exist.")
        config_interface_ip(ssh, target_interface, target_ip, target_subnet)
