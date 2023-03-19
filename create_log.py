#!/usr/bin/env python3
# -*- coding: utf-8 -*-
version = "2023-03-19"

# Imports
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
from getpass import getuser

# Global Variables
username = getuser()
conf_dir: str = ".config/email-log"


def get_config():
    settings = open_yaml(
        fname=f"{conf_dir}/emailog_set.yaml",
        fdest="home",
    )
    return settings


def create_file():
    config = get_config()
    logs = config["logs"]
    lines = config["lines"]

    for i in range(len(logs)):
        print(logs[i])
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
        body = f"File age: {age} hours \n{truncated_file}"
    return body


create_file()
