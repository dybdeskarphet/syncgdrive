import yaml
from internal import eprint
from network import get_current_ssid


def main():
    eprint(get_current_ssid()["ssid"])


if __name__ == "__main__":
    main()
