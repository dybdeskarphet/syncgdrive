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
