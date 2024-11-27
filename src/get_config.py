import yaml
from internal import eprint
from os import environ, path, makedirs

config_home = ""
config_path = ""

# Check if config home exist
if environ.get("HOME") is not None and environ.get("XDG_CONFIG_HOME") is not None:
    config_home = environ.get("XDG_CONFIG_HOME")
elif environ.get("HOME") is not None:
    config_home = environ.get("HOME") + "/.config"
else:
    eprint("User doesn't have a config directory.", "ERR")

# Create the config path if doesn't exist
if config_home != "":
    config_path = config_home + "/syncgdrive/config.yaml"
    if not path.exists(config_path):
        makedirs(path.dirname(config_path), exist_ok=True)
        with open(config_path, "a") as f:
            pass
else:
    eprint("User doesn't have a config directory.", "ERR")

with open(config_path, "r") as file:
    config = yaml.safe_load(file)


def get_trusted_networks():
    return config["trusted_networks"]
