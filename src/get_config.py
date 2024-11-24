import yaml
from internal import eprint
from os import environ

config_path = ""

if environ.get("HOME") is not None:
    config_path = environ.get("HOME") + "/.config/syncgdrive/config.yaml"
else:
    eprint("User doesn't have a home directory", "ERR")

if environ.get("XDG_CONFIG_HOME") is not None:
    config_path = environ.get("XDG_CONFIG_HOME")

print(config_path)
