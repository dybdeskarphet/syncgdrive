import iwlib
import psutil
import yaml
import os
from termcolor import colored


def eprint(msg="unknown", code="OK"):
    color = "green"
    exit_code = 0

    match code:
        case "OK":
            color = "green"
        case "SUCCESS":
            color = "blue"
            exit_code = 0
        case "ERR":
            color = "red"
            exit_code = 1
        case "PERM":
            color = "red"
            exit_code = 126
        case _:
            color = "red"
            exit_code = 1

    print(colored("syncgdrive:", color), msg)
    if code != "OK":
        exit(exit_code)


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
            else:
                current_ssid = iwlib.get_iwconfig(up_interfaces[0])["ESSID"].decode(
                    "utf-8"
                )
                break
    else:
        eprint("ERR", "No interface available")

    eprint(current_ssid)

    return None


def main():
    get_current_ssid()


if __name__ == "__main__":
    main()
