#!/usr/bin/env python3
# -*- coding: utf-8 -*-
version = "2023-03-19"

# Imports
from tmod import open_yaml

# from getpass import getuser
import requests

# Global Variables
# username = getuser()
conf_dir: str = ".config/email-log"


def get_config():
    settings = open_yaml(
        fname=f"{conf_dir}/emailog_set.yaml",
        fdest="home",
    )
    return settings


def send_file():
    config = get_config()
    logs = config["logs"]
    lines = config["lines"]
    topic = config["topic"]

    for i in range(len(logs)):
        print(logs[i])
        requests.put(
            f"https://ntfy.sh/{topic}",
            data=open(f"/home/troy/{logs[i]}.txt", "rb"),
            headers={"Filename": f"{logs[i]}.txt"},
        )


send_file()
