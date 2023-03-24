# -*- coding: utf-8 -*-
version = '2021-05-01'

# Personal Imports
from tmod import (
  config_setup, open_file, 
  open_yaml, check_file_age, last_n_lines,
  decrypt_login, mail, check_dir
  )
from schedule import run_pending, every
from smtplib import SMTP
from time import sleep
from getpass import getuser
from datetime import datetime, time

username = getuser()
conf_dir = ".config/email-log"

def runtime():
  settings = open_yaml(
  fname = f"{conf_dir}/emailog_set.yaml",
  fdest = "home",
  )
  return settings['runtime']

def  call_funtion():  
  settings = open_yaml(
  fname = f"{conf_dir}/emailog_set.yaml",
  fdest = "home",
  )
  kf = f"{conf_dir}/.info.key"
  ef = f"{conf_dir}/.cred_en.yaml"
  st = settings['sendto']
  log = settings['logs']
  lines = settings['lines']
  for i in range(len(log)):
    body = mail_body(log[i], lines)
    sub = f'Backup Log: for {username} (Log file: {log[i]})'
    key = open_file(
      fname = kf, 
      fdest = "home",
      mode ="rb"
      )
    login = decrypt_login(
      key = key, 
      e_fname = ef, 
      fdest = "home"
      )
    mail(
      body = body, 
      subject = sub, 
      send_to = st,
      login = login
        )

def mail_body(filename, lines):
  age =  check_file_age(filename, 'home')
  if age >= 24:
    con = (
      f"The log file {filename} for " 
      f"{username} is {age} hours old check backup")
  else:
    fcon = last_n_lines(
      fname = filename, 
      lines=lines,
      fdest = "home"
      )
    con = f'File age: {age} hours \n{fcon}'
  return con

dir_exist = check_dir(conf_dir)
if dir_exist == False:
  config_setup(conf_dir)
every().day.at(str(runtime())).do(call_funtion)

if __name__ == "__main__":
  try:
    print('waiting on timer')
    while True:
      run_pending()
      sleep(1)
  except KeyboardInterrupt as e:
    print(e)
    print('Interrupted')
