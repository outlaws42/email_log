# -*- coding: utf-8 -*-
version = '2021-04-21'

from tmod import (
  open_file, open_yaml, check_file_age, last_n_lines,
   decrypt_login, mail)
from schedule import run_pending, every
from smtplib import SMTP
from time import sleep
from getpass import getuser

default: dict = open_yaml(
  fname = 'default.yaml',
  fdest = 'relative',
  )

username = getuser()
settings = open_yaml(
  fname = '.config/emailog_set.yaml',
  fdest = 'home',
  def_content = default,
  )

def  call_funtion():
  kf = ".config/info.key"
  ef = ".config/.cred_en.yaml"
  st = settings['sendto']
  if username == 'cara':
    log = ['Logs/net_backup.log', 'Logs/backupUSB.log']
    for i in range(len(log)):
      body = mail_body(log[i], 30)
      sub = f'Backup Log: for {username} (Log file: {log[i]})'
      key = open_file(
        fname = kf, 
        fdest = "home",
        mode ="rb")
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

  elif username == 'troy':
    log = 'Logs/net_backup.log'
    body = mail_body(log, 30)
    sub = f'Backup Log: for {username} (Log file: {log})'
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
  else:
    print('Unknown log file')

def mail_body(filename, lines):
  age =  check_file_age(filename, 'home')
  if age >= 24:
    con = f"The log file {filename} for {username} is {age} hours old check backup"
  else:
    con = last_n_lines(filename, lines,'home')
  return con

every().day.at(settings['runtime']).do(call_funtion)

if __name__ == "__main__":
  try:
    print('waiting on timer')
    while True:
      run_pending()
      sleep(1)
  except KeyboardInterrupt as e:
    print(e)
    print('Interrupted')