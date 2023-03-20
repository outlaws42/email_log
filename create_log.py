#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This creates a copy of a log file with only the last so many lines for sending
for sending with notifications.
"""

# Imports
from getpass import getuser

# Personal Imports
from tmod import (
    config_setup,
    open_file,
    save_file,
    open_yaml,
    check_file_age,
    last_n_lines,
    mail,
    check_dir,
)

__author__ = "Troy Franks"
__version__ = "2023-03-20"

# Global Variables
username = getuser()
conf_dir: str = ".config/email-log"


def get_config():
    settings = open_yaml(
        fname=f"{conf_dir}/emailog_set.yaml",
        fdest="home",
    )
    return settings


def create_file(config_setting):
    config = config_setting
    logs = config["logs"]
    lines = config["lines"]

    for i in range(len(logs)):
        body = file_body(filename=logs[i], lines=lines)
        save_file(
            fname=f"{logs[i]}.txt",
            content=body,
            fdest="home",
            mode="w",
        )


def file_body(
    filename: str,
    lines: int,
):
    age: int = check_file_age(filename, "home")
    if age >= 24:
        body: str = (
            f"The log file {filename} for "
            f"{username} is {age} hours old check backup"
        )
    else:
        truncated_file = last_n_lines(
            fname=filename,
            lines=lines,
            fdest="home",
        )
        body = f"File age: {age} hours for user {username}\n{truncated_file}"
    return body


if __name__ == "__main__":
    config = get_config()
    create_file(config)
