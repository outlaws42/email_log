#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script sends notifications with a section of backup log files through the
ntfy service. This will run at a specified time from the config.
"""
# Imports
from schedule import run_pending, every
from time import sleep
from getpass import getuser
import requests

# Personal Imports
from tmod import open_yaml, check_dir, config_setup
from create_log import create_file

__author__ = "Troy Franks"
__version__ = "2023-03-20"

# Global Variables
username = getuser()
conf_dir: str = ".config/email-log"


def runtime():
    settings = open_yaml(
        fname=f"{conf_dir}/emailog_set.yaml",
        fdest="home",
    )
    return settings["runtime"]


def get_config():
    settings = open_yaml(
        fname=f"{conf_dir}/emailog_set.yaml",
        fdest="home",
    )
    return settings


def send_file():
    config = get_config()
    create_file(config)
    logs = config["logs"]
    lines = config["lines"]
    topic = config["topic"]

    for i in range(len(logs)):
        requests.put(
            f"https://ntfy.sh/{topic}",
            data=open(f"/home/{username}/{logs[i]}.txt", "rb"),
            headers={"Filename": f"{logs[i]}.txt"},
        )


dir_exist = check_dir(conf_dir)
if dir_exist is False:
    config_setup(conf_dir)
every().day.at(str(runtime())).do(send_file)

if __name__ == "__main__":
    try:
        print("waiting on timer")
        while True:
            run_pending()
            sleep(1)
    except KeyboardInterrupt as e:
        print(e)
        print("Interrupted")
