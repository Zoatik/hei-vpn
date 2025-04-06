import importlib
import json
import os
import sys
import requests

DEFAULT_CONFIG = {
    "gateway": "https://remote.hevs.ch",
    "timeout": 15
}

def get_base_path():
    # Si packagé avec PyInstaller
    if getattr(sys, 'frozen', False):
        return getattr(sys, '_MEIPASS', os.getcwd())
    # Si lancé depuis package whl
    try:
        return os.path.join(importlib.resources.files("hei_vpn"))
    except Exception:
        # Si lancé directement depuis le main
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_driver_path():
    return os.path.join(get_base_path(), "geckodriver")

def load_config():
    config_path = os.path.abspath(os.path.expanduser("~/.config/hei-vpn/config.json"))
    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)

    with open(config_path, "r") as f:
        return json.load(f)

def getPublicIp():
    return requests.head("https://wikipedia.org").headers["X-Client-IP"]
