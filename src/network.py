import psutil
import iwlib
from utils import eprint
from get_config import get_trusted_networks


def get_current_ssid():
    network_stats = psutil.net_if_stats()
    up_interfaces = []
    ignored_interfaces = ["lo"]
    current_ssid = ""
    ethernet_patterns = ("eno", "ens", "enp", "enx", "eth")

    # NOTE: Get the currently up network interfaces and push them to an array
    for interface_name, snic_stats in network_stats.items():
        if snic_stats.isup:
            up_interfaces.append(interface_name)

    # NOTE: Remove interfaces like lo
    for interface in ignored_interfaces:
        if interface in up_interfaces:
            up_interfaces.remove(interface)

    # NOTE: Check if connected with ethernet, if not, get the current SSID
    if up_interfaces:
        for interface in up_interfaces:
            if interface.lower().startswith(ethernet_patterns):
                eprint("Ethernet is connected")
                return {"connection_type": "ethernet", "ssid": current_ssid}
            else:
                current_ssid = iwlib.get_iwconfig(up_interfaces[0])["ESSID"].decode(
                    "utf-8"
                )
                break
    else:
        eprint("ERR", "No interface available")

    return {"connection_type": "wireless", "ssid": current_ssid}


def is_trusted_network():
    if (
        get_current_ssid()["ssid"] in get_trusted_networks()
        or get_current_ssid()["connection_type"] == "ethernet"
    ):
        return True
    else:
        return False
