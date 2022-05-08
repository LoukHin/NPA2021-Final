import requests

host = "10.0.15.112"
username = "admin"
password = "cisco"
student_id = "62070184"
loopback_name = f"Loopback{student_id}"

access_token = ""
webex_endpoint = "https://webexapis.com/v1/messages"
webex_room_id = ""

def get_last_webex_message(room_id):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    res = requests.get(f"{webex_endpoint}?roomId={room_id}", headers=headers)
    return res.json().get("items", [{}])[0].get("text", "")

def get_interface_oper_status(interface_name):
    headers = {
        "Accept": "application/yang-data+json",
        "Content-type":"application/yang-data+json"
    }

    restconf_endpoint = f"https://{host}/restconf/data/ietf-interfaces:interfaces-state/interface={interface_name}/"
    res = requests.get(restconf_endpoint, auth=(username, password), headers=headers, verify=False)
    interface_info = res.json().get("ietf-interfaces:interface", {})
    return interface_info.get("oper-status")

