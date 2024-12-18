import yaml
from utils import eprint
from os import environ, path, makedirs


def load_config():
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
        config = yaml.safe_load(file) or {}

    return config


def get_trusted_networks():
    cfg = load_config()
    return cfg.get("trusted_networks", [])


def get_selected_remote():
    cfg = load_config()
    return cfg.get("selected_remote")


def get_backup_list():
    cfg = load_config()
    return cfg.get("backup_list")


def get_sync_list():
    cfg = load_config()
    return cfg.get("sync_list")


def get_remote_root():
    cfg = load_config()
    target_root = cfg.get("target_root")
    if target_root is not None:
        if target_root.endswith("/"):
            return target_root.removesuffix("/")
    else:
        return None
