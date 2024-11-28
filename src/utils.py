from termcolor import colored
from os import environ


def get_home():
    home = environ.get("HOME")
    if home is not None:
        return home
    else:
        eprint("User doesn't have a home directory.", "ERR")


def eprint(msg="unknown", code="OK"):
    color = "green"
    exit_code = 0

    match code:
        case "OK":
            color = "green"
        case "WARN":
            color = "yellow"
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
    if exit_code != 0:
        exit(exit_code)
